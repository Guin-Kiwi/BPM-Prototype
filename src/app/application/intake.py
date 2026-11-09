from datetime import date, datetime, timezone
from typing import Protocol
from uuid import uuid4

from app.domain.reports import Report


class Repository(Protocol):
    def farms(self) -> list: ...
    def fields(self) -> list: ...
    def save(self, report: Report) -> None: ...
    def get(self, report_id: str) -> Report | None: ...
    def history(self, report: Report) -> list[Report]: ...


class InvalidInput(ValueError):
    pass


class Intake:
    def __init__(self, repository: Repository):
        self.repository = repository

    def submit(self, farm_id: str, field_id: str, observation_date: str,
               description: str, image: bytes | None, image_type: str | None) -> Report:
        if not any(f['id'] == field_id and f['farm_id'] == farm_id for f in self.repository.fields()):
            raise InvalidInput('Choose a valid farm and one of its fields.')
        try:
            parsed = date.fromisoformat(observation_date)
            if parsed.isoformat() != observation_date or parsed > date.today():
                raise ValueError
        except ValueError:
            raise InvalidInput('Enter a valid observation date in YYYY-MM-DD format, not in the future.') from None
        if not description.strip():
            raise InvalidInput('Enter a description of your observation.')
        report = Report(str(uuid4()), farm_id, field_id, observation_date, description,
                        datetime.now(timezone.utc).isoformat(timespec='microseconds'), image, image_type)
        self.repository.save(report)
        return report

    def detail(self, report_id: str):
        report = self.repository.get(report_id)
        return (report, self.repository.history(report)) if report else None
