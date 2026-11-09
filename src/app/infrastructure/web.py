import io
import os
import warnings
from html import escape
from pathlib import Path

from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse, RedirectResponse, Response
from PIL import Image, UnidentifiedImageError
from python_multipart.exceptions import MultipartParseError
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
    error_html = f'<p class="error" role="alert">{escape(error)}</p>' if error else ''
    return page('Record an observation', f'''{error_html}
<p>Simulated farmer · Sunrise Farm (farm-1). This is not a login.</p>
<p>Upload represents a new photo. Its selection time is simulated, not verified capture time.</p>
<form action="/reports" method="post" enctype="multipart/form-data">
<label>New JPEG or PNG photo (up to 10 MiB) <input id="photo" type="file" name="image" accept="image/jpeg,image/png" capture="environment" required></label>
<input type="hidden" name="observation_time" id="observation_time">
<label>About how many plants are affected in the area observed? <input name="estimate_value" type="number" min="0" step="any" required></label>
<label>Estimate type <select name="estimate_kind"><option value="count">Approximate plant count</option><option value="percentage">Percentage of plants</option></select></label>
<label>Optional area cue <input name="area_cue"></label>
<label>Optional description <textarea name="description"></textarea></label>
<input type="hidden" name="latitude" id="latitude"><input type="hidden" name="longitude" id="longitude">
<input type="hidden" name="accuracy" id="accuracy"><input type="hidden" name="fix_time" id="fix_time">
<p id="gps_status" role="status">Location required. Obtain a browser GPS fix.</p>
<p>Map fallback is unavailable: no field boundaries are supplied. If GPS fails, retry; no draft is saved.</p>
<button type="button" id="gps">Get or retry GPS</button> <button type="submit">Save report</button></form>
<script>
const photo = document.getElementById('photo');
photo.addEventListener('change', () => {{ document.getElementById('observation_time').value = photo.files.length ? new Date().toISOString() : ''; }});
document.getElementById('gps').addEventListener('click', () => {{
  for (const key of ['latitude','longitude','accuracy','fix_time']) document.getElementById(key).value = '';
  const status = document.getElementById('gps_status');
  if (!navigator.geolocation) {{ status.textContent = 'GPS unavailable. Retry on a supported device; map fallback is unavailable.'; return; }}
  status.textContent = 'Obtaining GPS fix…';
  navigator.geolocation.getCurrentPosition(pos => {{
    for (const key of ['latitude','longitude','accuracy']) document.getElementById(key).value = pos.coords[key];
    document.getElementById('fix_time').value = new Date(pos.timestamp).toISOString();
    status.textContent = `GPS fix obtained: accuracy ${{pos.coords.accuracy}} m. A fix at most 100 m and at most five minutes old is required.`;
  }}, () => {{ status.textContent = 'GPS denied or unavailable. Retry GPS; map fallback is unavailable.'; }}, {{enableHighAccuracy:true, maximumAge:0, timeout:15000}});
}});
</script>''', status)


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
                parsed = await BoundedMultipartParser(request.headers, chunks(), max_files=1, max_fields=10, max_part_size=128 * 1024).parse()
            else:
                parsed = await FormRequest(request.scope, receive).form(max_files=1, max_fields=10, max_part_size=128 * 1024)
            try:
                keys = ('observation_time', 'estimate_kind', 'estimate_value', 'area_cue', 'description', 'latitude', 'longitude', 'accuracy', 'fix_time')
                if any(len(parsed.getlist(key)) > 1 for key in (*keys, 'image')):
                    raise InvalidInput('Provide one value for each field and one photo.')
                values = {key: parsed.get(key, '') for key in keys}
                if not all(isinstance(value, str) for value in values.values()):
                    raise InvalidInput('Complete the form with valid values.')
                upload = parsed.get('image')
                data, kind = None, None
                if isinstance(upload, UploadFile):
                    data = await upload.read(MAX_IMAGE + 1)
                    if data:
                        kind = verify_image(data)
                elif upload not in (None, ''):
                    raise InvalidInput('Choose a JPEG or PNG photo.')
                report = service.submit(values, data, kind)
            finally:
                await parsed.close()
            return RedirectResponse('/reports/' + report.id, status_code=303)
        except (MultiPartException, MultipartParseError):
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
            def evidence(item):
                finding = f'<p>Legacy finding (confirmation provenance unknown): {escape(item.finding)}</p>' if item.finding else ''
                estimate = f'{item.estimate_value:g} {escape(item.estimate_unit)} ({escape(item.estimate_source)})' if item.estimate_value is not None else 'unavailable'
                observed = f'{escape(item.observation_time)} (simulated photo-selection time)' if item.observation_time else f'{escape(item.observation_date)} (date only; time unavailable)'
                location = f'browser GPS: {item.latitude}, {item.longitude}; accuracy {item.accuracy} m; fix time {escape(item.fix_time)}' if item.location_source else 'unavailable (legacy field association is not a location)'
                cue = escape(item.area_cue) if item.area_cue else 'unavailable'
                return f'<p>Observation: {escape(item.description) or "unavailable"} · Time: {observed} · Received (UTC): {escape(item.received_at)}</p><p>Estimate: {estimate} · Area cue: {cue} · Location: {location}</p>{finding}'
            image = f'<p>Photo source: {escape(report.photo_source) if report.photo_source else "unavailable"}.</p><p><a href="/reports/{escape(report.id, quote=True)}/image">Open photo</a></p><img src="/reports/{escape(report.id, quote=True)}/image" alt="Submitted photo">' if report.image else '<p>Photo unavailable.</p>'
            entries = ''.join(f'<li><a href="/reports/{escape(item.id, quote=True)}">{escape(item.id)}</a>{evidence(item)}</li>' for item in history)
            return page('Report detail', f'''<p>Report ID: {escape(report.id)} · Farm: {escape(report.farm_id)} · Farmer: {escape(report.farmer_id) if report.farmer_id else 'unavailable'}</p>
{evidence(report)}{image}<p>Nearby context and field grouping are unavailable.</p>
<h2>Farm report history</h2><ul>{entries}</ul>''')
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
