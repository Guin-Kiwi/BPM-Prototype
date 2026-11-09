import sqlite3
from contextlib import contextmanager
from dataclasses import fields
from pathlib import Path
from uuid import uuid4

from app.domain.reports import Report


COLUMNS = ', '.join(field.name for field in fields(Report))
SCHEMA = '''CREATE TABLE reports (
    id TEXT PRIMARY KEY, farm_id TEXT NOT NULL REFERENCES farms(id),
    field_id TEXT REFERENCES fields(id), observation_date TEXT NOT NULL,
    description TEXT NOT NULL, received_at TEXT NOT NULL, image BLOB, image_type TEXT, finding TEXT,
    observation_time TEXT, observation_source TEXT, observation_precision TEXT, photo_source TEXT,
    estimate_kind TEXT, estimate_value REAL, estimate_unit TEXT, estimate_source TEXT, area_cue TEXT,
    latitude REAL, longitude REAL, accuracy REAL, fix_time TEXT, location_source TEXT, farmer_id TEXT
)'''
LEGACY_COLUMNS = 'id, farm_id, field_id, observation_date, description, received_at, image, image_type, finding'


class SQLiteRepository:
    def __init__(self, path):
        self.path = Path(path)
        self.path.parent.mkdir(parents=True, exist_ok=True)
        with self.connect() as db:
            exists = db.execute("SELECT 1 FROM sqlite_master WHERE type='table' AND name='reports'").fetchone()
            version = db.execute('PRAGMA user_version').fetchone()[0]
            if version > 1:
                raise RuntimeError('Database version is newer than this application.')
            if exists and version == 0:
                self.migrate(db)
            elif not exists:
                self.initialize(db)

    def migrate(self, db):
        backup_path = self.path.with_name(self.path.name + '.' + uuid4().hex + '.backup')
        try:
            db.execute('BEGIN IMMEDIATE')
            if db.execute('PRAGMA user_version').fetchone()[0] == 1:
                db.rollback()
                return
            with sqlite3.connect(self.path) as source, sqlite3.connect(backup_path) as backup:
                source.backup(backup)
                if backup.execute('PRAGMA integrity_check').fetchall() != [('ok',)]:
                    raise RuntimeError('Backup integrity check failed')
            with sqlite3.connect(backup_path.resolve().as_uri() + '?mode=ro', uri=True) as backup:
                if backup.execute('PRAGMA integrity_check').fetchall() != [('ok',)]:
                    raise RuntimeError('Backup verification failed')
        except Exception as exc:
            db.rollback()
            raise RuntimeError(f'Could not verify SQLite backup at {backup_path}; database was not migrated. Check disk space and permissions.') from exc
        try:
            legacy_columns = [row[1] for row in db.execute('PRAGMA table_info(reports)')]
            if legacy_columns != LEGACY_COLUMNS.split(', '):
                raise RuntimeError('Unexpected legacy report schema needs manual migration')
            tables = db.execute("SELECT name FROM sqlite_master WHERE type='table' AND name NOT LIKE 'sqlite_%' AND name != 'reports'").fetchall()
            for table in tables:
                name = table[0].replace(chr(34), chr(34) * 2)
                if any(row[2] == 'reports' for row in db.execute(f'PRAGMA foreign_key_list("{name}")')):
                    raise RuntimeError('References to reports need manual migration')
            if db.execute("SELECT 1 FROM sqlite_master WHERE tbl_name='reports' AND type IN ('trigger', 'index') AND sql IS NOT NULL").fetchone():
                raise RuntimeError('Custom report indexes or triggers need manual migration')
            db.execute('ALTER TABLE reports RENAME TO reports_legacy')
            db.execute(SCHEMA)
            db.execute(f'INSERT INTO reports ({LEGACY_COLUMNS}) SELECT {LEGACY_COLUMNS} FROM reports_legacy')
            db.execute('DROP TABLE reports_legacy')
            if db.execute('PRAGMA foreign_key_check').fetchall():
                raise RuntimeError('Foreign key check failed')
            if db.execute('PRAGMA integrity_check').fetchone()[0] != 'ok':
                raise RuntimeError('Integrity check failed')
            db.execute('PRAGMA user_version = 1')
            db.commit()
        except Exception as exc:
            db.rollback()
            raise RuntimeError(f'Migration rolled back; verified backup retained at {backup_path}.') from exc

    def initialize(self, db):
        db.execute('BEGIN IMMEDIATE')
        db.execute('CREATE TABLE farms (id TEXT PRIMARY KEY, name TEXT NOT NULL)')
        db.execute('CREATE TABLE fields (id TEXT PRIMARY KEY, farm_id TEXT NOT NULL REFERENCES farms(id), name TEXT NOT NULL)')
        db.execute(SCHEMA)
        db.executemany('INSERT INTO farms VALUES (?, ?)', [('farm-1', 'Sunrise Farm'), ('farm-2', 'River Farm')])
        db.executemany('INSERT INTO fields VALUES (?, ?, ?)', [('field-1','farm-1','North Field'), ('field-2','farm-1','South Field'), ('field-3','farm-2','East Field'), ('field-4','farm-2','West Field')])
        db.executemany(f'INSERT INTO reports ({LEGACY_COLUMNS}) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)', [
            ('seed-1','farm-1','field-1','2024-01-01','Fictional leaf spots observed.','2024-01-01T12:00:00.000000+00:00',None,None,'Fictional leaf spot confirmed.'),
            ('seed-2','farm-1','field-1','2024-02-01','Fictional yellow leaves observed.','2024-02-01T12:00:00.000000+00:00',None,None,None),
            ('seed-3','farm-2','field-3','2024-03-01','Fictional wilting observed.','2024-03-01T12:00:00.000000+00:00',None,None,None)])
        db.execute('PRAGMA user_version = 1')

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

    def save(self, report):
        with self.connect() as db:
            db.execute(f'INSERT INTO reports ({COLUMNS}) VALUES ({", ".join("?" for _ in fields(Report))})', tuple(getattr(report, field.name) for field in fields(Report)))

    def get(self, report_id):
        with self.connect() as db:
            row = db.execute('SELECT * FROM reports WHERE id = ?', (report_id,)).fetchone()
            return Report(**dict(row)) if row else None

    def history(self, farm_id):
        with self.connect() as db:
            rows = db.execute('''SELECT * FROM reports WHERE farm_id = ? ORDER BY observation_date DESC,
                observation_time IS NOT NULL DESC, observation_time DESC, received_at DESC, id DESC''', (farm_id,))
            return [Report(**dict(row)) for row in rows]
