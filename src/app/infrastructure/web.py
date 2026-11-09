import io
import os
import warnings
from html import escape
from pathlib import Path

from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse, RedirectResponse, Response
from PIL import Image, UnidentifiedImageError
from starlette.datastructures import UploadFile
from starlette.requests import Request as FormRequest
from starlette.formparsers import MultiPartException, MultiPartParser

from app.application.intake import Intake, InvalidInput
from app.infrastructure.sqlite import SQLiteRepository

MAX_IMAGE = 10 * 1024 * 1024
MAX_REQUEST = MAX_IMAGE + 128 * 1024


class BoundedMultipartParser(MultiPartParser):
    spool_max_size = MAX_REQUEST


def page(title, content, status=200):
    return HTMLResponse(f'''<!doctype html><html lang="en"><head><meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1"><title>{escape(title)}</title>
<style>body{{font:1rem system-ui;max-width:50rem;margin:2rem auto;padding:0 1rem;line-height:1.5}}
label{{display:block;margin-top:1rem}}input,select,textarea,button{{font:inherit;max-width:100%}}
textarea{{width:100%;min-height:7rem}}img{{max-width:100%;max-height:30rem}}.error{{color:#9a1b1b}}</style>
</head><body><header><strong>Synthetic demonstration data</strong> · <a href="/">New report</a></header>
<main><h1>{escape(title)}</h1>{content}</main></body></html>''', status_code=status)


def verify_image(data):
    if len(data) > MAX_IMAGE:
        raise InvalidInput('Image must be at most 10 MiB.')
    try:
        with warnings.catch_warnings():
            warnings.simplefilter('error', Image.DecompressionBombWarning)
            with Image.open(io.BytesIO(data)) as image:
                if image.format not in ('JPEG', 'PNG'):
                    raise InvalidInput('Choose a JPEG or PNG image.')
                kind = image.format
                image.verify()
            with Image.open(io.BytesIO(data)) as image:
                image.load()
        return {'JPEG': 'image/jpeg', 'PNG': 'image/png'}[kind]
    except (UnidentifiedImageError, OSError, ValueError, SyntaxError, Image.DecompressionBombError, Image.DecompressionBombWarning):
        raise InvalidInput('Choose a valid, undamaged JPEG or PNG image.') from None


def form(repo, error='', status=200):
    farms = ''.join(f'<option value="{escape(f["id"], quote=True)}">{escape(f["name"])}</option>' for f in repo.farms())
    fields = ''.join(f'<option value="{escape(f["id"], quote=True)}" data-farm="{escape(f["farm_id"], quote=True)}">{escape(f["name"])}</option>' for f in repo.fields())
    error_html = f'<p class="error" role="alert">{escape(error)}</p>' if error else ''
    return page('Record an observation', f'''{error_html}<p>All farms and seeded history are fictional.</p>
<form action="/reports" method="post" enctype="multipart/form-data">
<label>Farm <select id="farm" name="farm_id" required><option value="">Choose a farm</option>{farms}</select></label>
<label>Field <select id="field" name="field_id" required><option value="">Choose a field</option>{fields}</select></label>
<label>Observation date <input type="date" name="observation_date" required></label>
<label>Description <textarea name="description" required></textarea></label>
<label>Optional JPEG or PNG (up to 10 MiB) <input type="file" name="image" accept="image/jpeg,image/png"></label>
<button type="submit">Save report</button></form>
<script>const farm=document.getElementById('farm'), field=document.getElementById('field');
function filterFields() {{ for (const o of field.options) if(o.value) {{o.hidden=o.dataset.farm!==farm.value; o.disabled=o.hidden;}} if(field.selectedOptions[0]?.disabled) field.value=''; }}
farm.addEventListener('change',filterFields); filterFields();</script>''', status)


def create_app(db_path=None):
    path = Path(db_path or os.environ.get('BPM_DB_PATH', 'data/bpm.sqlite3'))
    repo = SQLiteRepository(path)
    service = Intake(repo)
    app = FastAPI(docs_url=None, redoc_url=None, openapi_url=None)
    app.state.db_path = path

    @app.get('/', response_class=HTMLResponse)
    async def index():
        return form(repo)

    @app.post('/reports')
    async def submit(request: Request):
        body = bytearray()
        try:
            async for chunk in request.stream():
                if len(body) + len(chunk) > MAX_REQUEST:
                    raise InvalidInput('Upload is too large; the image limit is 10 MiB.')
                body.extend(chunk)
            async def receive():
                return {'type': 'http.request', 'body': bytes(body), 'more_body': False}
            if request.headers.get('content-type', '').lower().startswith('multipart/form-data'):
                async def chunks():
                    yield bytes(body)
                parsed = await BoundedMultipartParser(request.headers, chunks(), max_files=1, max_fields=8, max_part_size=128 * 1024).parse()
            else:
                parsed = await FormRequest(request.scope, receive).form(max_files=1, max_fields=8, max_part_size=128 * 1024)
            try:
                if any(len(parsed.getlist(key)) != 1 for key in ('farm_id', 'field_id', 'observation_date', 'description')) or len(parsed.getlist('image')) > 1:
                    raise InvalidInput('Provide one value for each field and at most one image.')
                values = [parsed.get(k) for k in ('farm_id', 'field_id', 'observation_date', 'description')]
                if not all(isinstance(value, str) for value in values):
                    raise InvalidInput('Complete all required fields.')
                upload = parsed.get('image')
                data = None
                kind = None
                if isinstance(upload, UploadFile):
                    data = await upload.read(MAX_IMAGE + 1)
                    if data:
                        kind = verify_image(data)
                    elif upload.filename:
                        raise InvalidInput('Choose a valid, undamaged JPEG or PNG image.')
                    else:
                        data = None
                elif upload not in (None, ''):
                    raise InvalidInput('Choose a JPEG or PNG image.')
                report = service.submit(*values, data, kind)
            finally:
                await parsed.close()
            return RedirectResponse('/reports/' + report.id, status_code=303)
        except MultiPartException:
            return form(repo, 'Invalid form or too many attachments. Please check the form and try again.', 400)
        except InvalidInput as exc:
            return form(repo, str(exc), 400)
        except Exception:
            return page('Report not saved', '<p>Unable to save the report. Please try again.</p>', 500)

    @app.get('/reports/{report_id}')
    async def detail(report_id: str):
        try:
            result = service.detail(report_id)
            if not result:
                return page('Report not found', '<p>No report exists with this ID.</p>', 404)
            report, history = result
            fields = {f['id']: f for f in repo.fields()}
            farms = {f['id']: f for f in repo.farms()}
            def evidence(item):
                finding = f'<p><strong>Confirmed finding (fictional):</strong> {escape(item.finding)}</p>' if item.finding else ''
                return f'<p><strong>Observation:</strong> {escape(item.description)}</p>{finding}'
            image = f'<p><a href="/reports/{escape(report.id, quote=True)}/image">Open attachment</a></p><img src="/reports/{escape(report.id, quote=True)}/image" alt="Submitted attachment">' if report.image else ''
            entries = ''.join(f'<li><a href="/reports/{escape(item.id, quote=True)}">{escape(item.observation_date)}</a> · received {escape(item.received_at)}{evidence(item)}</li>' for item in history)
            history_html = f'<ul>{entries}</ul>' if entries else '<p>No earlier reports. This does not mean there was no disease.</p>'
            return page('Report saved', f'''<p>Report received. ID: {escape(report.id)}</p>
<p>Farm: {escape(farms[report.farm_id]['name'])} · Field: {escape(fields[report.field_id]['name'])}</p>
<p>Observation date: {escape(report.observation_date)} · Received (UTC): {escape(report.received_at)}</p>
{evidence(report)}{image}<h2>Earlier reports for this field</h2>{history_html}''')
        except Exception:
            return page('Report unavailable', '<p>Unable to retrieve the report. Please try again.</p>', 500)

    @app.get('/reports/{report_id}/image')
    async def image(report_id: str):
        try:
            report = repo.get(report_id)
            if not report or report.image is None:
                return page('Attachment not found', '<p>No attachment exists for this report.</p>', 404)
            return Response(report.image, media_type=report.image_type, headers={'Content-Disposition': 'inline; filename="attachment"', 'X-Content-Type-Options': 'nosniff'})
        except Exception:
            return page('Attachment unavailable', '<p>Unable to retrieve the attachment.</p>', 500)

    return app


app = create_app()
