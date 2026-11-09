from datetime import datetime, timedelta, timezone
from decimal import Decimal, InvalidOperation
from typing import Protocol
from uuid import uuid4

from app.domain.reports import Report


class Repository(Protocol):
    def save(self, report: Report) -> None: ...
    def get(self, report_id: str) -> Report | None: ...
    def history(self, farm_id: str) -> list[Report]: ...


class BoundaryProvider(Protocol):
    def boundaries(self, farm_id: str) -> list: ...


class InvalidInput(ValueError):
    pass


def timestamp(value):
    try:
        parsed = datetime.fromisoformat(value.replace('Z', '+00:00'))
        if parsed.tzinfo is None or parsed.utcoffset() is None:
            raise ValueError
        return parsed.astimezone(timezone.utc)
    except (ValueError, TypeError, AttributeError, OverflowError):
        raise InvalidInput('A valid timestamp with timezone is required; select the photo or retry GPS.') from None


def number(value):
    try:
        parsed = Decimal(value)
        if not parsed.is_finite():
            raise ValueError
        return parsed
    except (InvalidOperation, ValueError, TypeError):
        raise InvalidInput('Enter a valid estimate and obtain a usable GPS fix.') from None


class Intake:
    FARM_ID = 'farm-1'

    def __init__(self, repository: Repository):
        self.repository = repository

    def submit(self, values, image: bytes | None, image_type: str | None) -> Report:
        now = datetime.now(timezone.utc)
        if not image or image_type not in ('image/jpeg', 'image/png'):
            raise InvalidInput('Choose a new JPEG or PNG photo.')
        observed = timestamp(values.get('observation_time'))
        fix = timestamp(values.get('fix_time'))
        if observed > now:
            raise InvalidInput('Observation time cannot be in the future; select the photo again.')
        lat, lon, accuracy = (number(values.get(key)) for key in ('latitude', 'longitude', 'accuracy'))
        if not (-90 <= lat <= 90 and -180 <= lon <= 180 and 0 <= accuracy <= 100 and now - timedelta(minutes=5) <= fix <= now):
            raise InvalidInput('A recent GPS fix with accuracy at most 100 metres is required; retry GPS. Map fallback is unavailable.')
        kind = values.get('estimate_kind')
        estimate = number(values.get('estimate_value'))
        if kind not in ('count', 'percentage') or estimate < 0 or (kind == 'count' and (estimate != estimate.to_integral_value() or estimate > Decimal('1e308'))) or (kind == 'percentage' and estimate > 100):
            raise InvalidInput('Enter a nonnegative whole plant count or a percentage from 0 to 100.')
        report = Report(id=str(uuid4()), farm_id=self.FARM_ID, field_id=None,
                        observation_date=observed.date().isoformat(), description=values.get('description', '').strip(),
                        received_at=now.isoformat(timespec='microseconds'), image=image, image_type=image_type,
                        observation_time=observed.isoformat(), observation_source='simulated_upload_selection',
                        observation_precision='timestamp', photo_source='uploaded', estimate_kind=kind,
                        estimate_value=float(estimate), estimate_unit='plants' if kind == 'count' else 'percent',
                        estimate_source='farmer_reported', area_cue=values.get('area_cue', '').strip() or None,
                        latitude=float(lat), longitude=float(lon), accuracy=float(accuracy),
                        fix_time=fix.isoformat(), location_source='browser_geolocation', farmer_id='simulated-farmer-1')
        self.repository.save(report)
        return report

    def detail(self, report_id: str):
        report = self.repository.get(report_id)
        return (report, self.repository.history(report.farm_id)) if report else None
