import io
import sqlite3
from datetime import date, timedelta

import pytest
from fastapi.testclient import TestClient
from PIL import Image

from app.infrastructure.web import create_app


@pytest.fixture
def client(tmp_path):
    return TestClient(create_app(tmp_path / 'demo.sqlite3'))


def image_bytes(fmt='PNG'):
    image = Image.new('RGB', (2, 2), 'green')
    out = io.BytesIO()
    image.save(out, format=fmt)
    return out.getvalue()


def submit(client, **kwargs):
    data = {'farm_id': 'farm-1', 'field_id': 'field-1',
            'observation_date': '2025-01-01', 'description': 'Leaves observed'}
    data.update(kwargs.pop('data', {}))
    return client.post('/reports', data=data, follow_redirects=False, **kwargs)


def test_form_seed_and_restart(tmp_path):
    db = tmp_path / 'demo.sqlite3'
    first = TestClient(create_app(db))
    form = first.get('/')
    assert form.status_code == 200
    assert all(x in form.text for x in ['Synthetic', 'farm-1', 'farm-2', 'field-1', 'field-4'])
    response = submit(first, data={'description': '<script>unsafe</script>'},
                      files={'image': ('diagnosis.png', image_bytes(), 'text/plain')})
    assert response.status_code == 303
    location = response.headers['location']
    second = TestClient(create_app(db))
    detail = second.get(location)
    assert detail.status_code == 200
    assert '&lt;script&gt;unsafe&lt;/script&gt;' in detail.text
    assert '<script>unsafe</script>' not in detail.text
    assert 'diagnosis.png' not in detail.text
    assert 'Confirmed finding' in detail.text
    assert second.get(location + '/image').content == image_bytes()
    with sqlite3.connect(db) as conn:
        assert conn.execute('select count(*) from reports').fetchone()[0] == 4


@pytest.mark.parametrize('changes', [
    {'farm_id': 'missing'}, {'field_id': 'field-3'}, {'description': '  '},
    {'observation_date': '2025-02-30'}, {'observation_date': '20250101'},
    {'observation_date': (date.today() + timedelta(days=1)).isoformat()},
])
def test_invalid_inputs_do_not_save(client, changes):
    assert submit(client, data=changes).status_code == 400
    with sqlite3.connect(client.app.state.db_path) as conn:
        assert conn.execute('select count(*) from reports').fetchone()[0] == 3


@pytest.mark.parametrize('payload', [b'not an image', b'\x89PNG\r\n\x1a\ninvalid', image_bytes() + b'x' * (10 * 1024 * 1024)])
def test_invalid_images_do_not_save(client, payload):
    assert submit(client, files={'image': ('safe.png', payload, 'image/png')}).status_code == 400
    with sqlite3.connect(client.app.state.db_path) as conn:
        assert conn.execute('select count(*) from reports').fetchone()[0] == 3


@pytest.mark.parametrize('fmt', ['PNG', 'JPEG'])
def test_image_content_and_exact_size(client, fmt):
    content = image_bytes(fmt)
    content += b'\0' * (10 * 1024 * 1024 - len(content))
    response = submit(client, files={'image': ('anything', content, 'application/octet-stream')})
    assert response.status_code == 303
    assert client.get(response.headers['location'] + '/image').content == content


def test_history_backdating_and_field_isolation(client):
    current = submit(client, data={'field_id': 'field-2', 'observation_date': '2025-04-01', 'description': 'Current'})
    path = current.headers['location']
    assert 'No earlier reports' in client.get(path).text
    submit(client, data={'field_id': 'field-2', 'observation_date': '2025-02-01', 'description': 'Earlier'})
    submit(client, data={'field_id': 'field-2', 'observation_date': '2025-03-01', 'description': 'More recent'})
    submit(client, data={'field_id': 'field-1', 'observation_date': '2025-03-01', 'description': 'Other field'})
    text = client.get(path).text
    assert text.index('More recent') < text.index('Earlier')
    assert 'Other field' not in text
    assert client.get('/reports/unknown').status_code == 404


def test_storage_failure_does_not_confirm_or_persist(client):
    with sqlite3.connect(client.app.state.db_path) as conn:
        conn.execute("CREATE TRIGGER reject_insert BEFORE INSERT ON reports BEGIN SELECT RAISE(ABORT, 'secret failure'); END")
    response = submit(client, files={'image': ('a.png', image_bytes(), 'image/png')})
    assert response.status_code == 500
    assert 'secret failure' not in response.text
    assert 'confirmed' not in response.text.lower()
    with sqlite3.connect(client.app.state.db_path) as conn:
        assert conn.execute('select count(*) from reports').fetchone()[0] == 3
