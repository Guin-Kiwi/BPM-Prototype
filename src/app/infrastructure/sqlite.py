import sqlite3
from contextlib import contextmanager
from pathlib import Path

from app.domain.reports import Report


class SQLiteRepository:
    def __init__(self, path):
        self.path = Path(path)
        self.path.parent.mkdir(parents=True, exist_ok=True)
        with self.connect() as db:
            db.executescript('''
                CREATE TABLE IF NOT EXISTS farms (id TEXT PRIMARY KEY, name TEXT NOT NULL);
                CREATE TABLE IF NOT EXISTS fields (id TEXT PRIMARY KEY, farm_id TEXT NOT NULL REFERENCES farms(id), name TEXT NOT NULL);
                CREATE TABLE IF NOT EXISTS reports (
                    id TEXT PRIMARY KEY, farm_id TEXT NOT NULL REFERENCES farms(id),
                    field_id TEXT NOT NULL REFERENCES fields(id), observation_date TEXT NOT NULL,
                    description TEXT NOT NULL, received_at TEXT NOT NULL, image BLOB,
                    image_type TEXT, finding TEXT
                );
            ''')
            db.executemany('INSERT OR IGNORE INTO farms VALUES (?, ?)', [
                ('farm-1', 'Sunrise Farm'), ('farm-2', 'River Farm')])
            db.executemany('INSERT OR IGNORE INTO fields VALUES (?, ?, ?)', [
                ('field-1', 'farm-1', 'North Field'), ('field-2', 'farm-1', 'South Field'),
                ('field-3', 'farm-2', 'East Field'), ('field-4', 'farm-2', 'West Field')])
            db.executemany('INSERT OR IGNORE INTO reports VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)', [
                ('seed-1', 'farm-1', 'field-1', '2024-01-01', 'Fictional leaf spots observed.', '2024-01-01T12:00:00.000000+00:00', None, None, 'Fictional leaf spot confirmed.'),
                ('seed-2', 'farm-1', 'field-1', '2024-02-01', 'Fictional yellow leaves observed.', '2024-02-01T12:00:00.000000+00:00', None, None, None),
                ('seed-3', 'farm-2', 'field-3', '2024-03-01', 'Fictional wilting observed.', '2024-03-01T12:00:00.000000+00:00', None, None, None),
            ])

    @contextmanager
    def connect(self):
        db = sqlite3.connect(self.path)
        db.row_factory = sqlite3.Row
        try:
            db.execute('PRAGMA foreign_keys = ON')
            with db:
                yield db
        finally:
            db.close()

    def farms(self):
        with self.connect() as db:
            return [dict(row) for row in db.execute('SELECT * FROM farms ORDER BY id')]

    def fields(self):
        with self.connect() as db:
            return [dict(row) for row in db.execute('SELECT * FROM fields ORDER BY id')]

    def save(self, report):
        with self.connect() as db:
            db.execute('INSERT INTO reports VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)',
                       (report.id, report.farm_id, report.field_id, report.observation_date,
                        report.description, report.received_at, report.image, report.image_type, report.finding))

    def get(self, report_id):
        with self.connect() as db:
            row = db.execute('SELECT * FROM reports WHERE id = ?', (report_id,)).fetchone()
            return Report(**dict(row)) if row else None

    def history(self, report):
        with self.connect() as db:
            rows = db.execute('''SELECT * FROM reports WHERE field_id = ?
                AND (observation_date, received_at, id) < (?, ?, ?)
                ORDER BY observation_date DESC, received_at DESC, id DESC''',
                (report.field_id, report.observation_date, report.received_at, report.id))
            return [Report(**dict(row)) for row in rows]
