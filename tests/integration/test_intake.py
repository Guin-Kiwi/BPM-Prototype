import asyncio
import io
import sqlite3
from datetime import datetime, timedelta, timezone

import httpx
import pytest
from PIL import Image

from app.infrastructure.web import create_app


class HttpClient:
    def __init__(self, app):
        self.app = app

    def request(self, method, path, **kwargs):
        async def run():
            async with httpx.AsyncClient(transport=httpx.ASGITransport(app=self.app), base_url='http://test') as client:
                return await client.request(method, path, **kwargs)
        return asyncio.run(run())

    def get(self, path):
        return self.request('GET', path)


@pytest.fixture
def client(tmp_path):
    return HttpClient(create_app(tmp_path / 'demo.sqlite3'))


def image_bytes(fmt='PNG'):
    out = io.BytesIO()
    Image.new('RGB', (2, 2), 'green').save(out, format=fmt)
    return out.getvalue()


def submit(client, changes=None, image=True):
    now = datetime.now(timezone.utc).isoformat()
    data = {'observation_time': now, 'estimate_kind': 'count', 'estimate_value': '3',
            'area_cue': '', 'description': '', 'latitude': '-21', 'longitude': '-46',
            'accuracy': '100', 'fix_time': now}
    data.update(changes or {})
    files = {'image': ('photo.png', image_bytes(), 'image/png')} if image else None
    return client.request('POST', '/reports', data=data, files=files, follow_redirects=False)


def test_new_intake_history_and_restart(client):
    form = client.get('/').text
    assert 'simulated' in form.lower() and 'fallback' in form.lower()
    assert 'name="farm_id"' not in form and 'name="field_id"' not in form
    response = submit(client, {'estimate_kind': 'percentage', 'estimate_value': '25', 'area_cue': '<shed>'})
    assert response.status_code == 303
    page = client.get(response.headers['location']).text
    assert '25' in page and '&lt;shed&gt;' in page and 'simulated' in page.lower()
    assert 'fix' in page.lower() and 'unavailable' in page.lower()
    assert 'confirmation provenance unknown' in page.lower()
    assert 'Fictional wilting' not in page
    assert client.get(response.headers['location'] + '/image').content == image_bytes()
    again = HttpClient(create_app(client.app.state.db_path))
    assert again.get(response.headers['location']).status_code == 200


@pytest.mark.parametrize('changes', [
    {'estimate_kind': 'count', 'estimate_value': '-1'},
    {'estimate_kind': 'count', 'estimate_value': '1.5'},
    {'estimate_kind': 'percentage', 'estimate_value': '101'},
    {'estimate_kind': 'percentage', 'estimate_value': 'nan'},
    {'estimate_kind': 'other'}, {'estimate_value': ''},
    {'latitude': '91'}, {'longitude': 'nan'}, {'accuracy': '101'}, {'accuracy': '-1'},
    {'fix_time': 'bad'}, {'fix_time': (datetime.now(timezone.utc) - timedelta(minutes=6)).isoformat()},
    {'fix_time': (datetime.now(timezone.utc) + timedelta(days=1)).isoformat()},
    {'observation_time': 'bad'}, {'observation_time': (datetime.now(timezone.utc) + timedelta(days=1)).isoformat()},
])
def test_invalid_intake_never_saves(client, changes):
    assert submit(client, changes).status_code == 400
    with sqlite3.connect(client.app.state.db_path) as db:
        assert db.execute('SELECT count(*) FROM reports').fetchone()[0] == 3


def test_photo_required_and_invalid_image(client):
    assert submit(client, image=False).status_code == 400
    assert client.request('POST', '/reports', data={}, files={'image': ('x', b'bad', 'image/png')}).status_code == 400


def test_farm_history_includes_later_and_other_field(client):
    response = submit(client, {'description': 'Current'})
    later = submit(client, {'description': 'Later'})
    text = client.get(response.headers['location']).text
    assert later.status_code == 303 and 'Later' in text and 'Fictional leaf spots' in text
    assert 'Fictional wilting' not in text


def test_storage_failure_does_not_confirm(client):
    with sqlite3.connect(client.app.state.db_path) as db:
        db.execute("CREATE TRIGGER reject_insert AFTER INSERT ON reports BEGIN SELECT RAISE(ABORT, 'secret failure'); END")
    response = submit(client)
    assert response.status_code == 500 and 'secret failure' not in response.text
    with sqlite3.connect(client.app.state.db_path) as db:
        assert db.execute('SELECT count(*) FROM reports').fetchone()[0] == 3


def test_legacy_migration_backup_and_restart(tmp_path):
    path = tmp_path / 'legacy.sqlite3'
    with sqlite3.connect(path) as db:
        db.executescript('''CREATE TABLE farms (id TEXT PRIMARY KEY, name TEXT NOT NULL);
        CREATE TABLE fields (id TEXT PRIMARY KEY, farm_id TEXT NOT NULL REFERENCES farms(id), name TEXT NOT NULL);
        CREATE TABLE reports (id TEXT PRIMARY KEY, farm_id TEXT NOT NULL REFERENCES farms(id), field_id TEXT NOT NULL REFERENCES fields(id), observation_date TEXT NOT NULL, description TEXT NOT NULL, received_at TEXT NOT NULL, image BLOB, image_type TEXT, finding TEXT);
        INSERT INTO farms VALUES ('farm-1','Sunrise Farm'),('farm-2','River Farm');
        INSERT INTO fields VALUES ('field-1','farm-1','North'),('field-3','farm-2','East');''')
        db.executemany('INSERT INTO reports VALUES (?,?,?,?,?,?,?,?,?)', [
            ('custom-1','farm-1','field-1','2023-01-01','private text','2023-01-02T00:00:00+00:00',b'original','image/png','finding'),
            ('custom-2','farm-2','field-3','2023-01-02','second farm','2023-01-03T00:00:00+00:00',None,None,None)])
        original = db.execute('SELECT * FROM reports ORDER BY id').fetchall()
    app = create_app(path)
    with sqlite3.connect(path) as db:
        assert db.execute('SELECT id,farm_id,field_id,observation_date,description,received_at,image,image_type,finding FROM reports WHERE id LIKE "custom-%" ORDER BY id').fetchall() == original
        assert db.execute('PRAGMA integrity_check').fetchone()[0] == 'ok'
        assert db.execute('PRAGMA foreign_key_check').fetchall() == []
        assert db.execute('SELECT observation_time,estimate_value,latitude FROM reports WHERE id="custom-1"').fetchone() == (None,None,None)
    backups = list(tmp_path.glob('legacy.sqlite3*.backup'))
    assert len(backups) == 1
    with sqlite3.connect(backups[0]) as db:
        assert db.execute('SELECT * FROM reports ORDER BY id').fetchall() == original
        assert db.execute('PRAGMA integrity_check').fetchone()[0] == 'ok'
    create_app(path)
    assert len(list(tmp_path.glob('legacy.sqlite3*.backup'))) == 1
    assert HttpClient(app).get('/reports/custom-1').status_code == 200
