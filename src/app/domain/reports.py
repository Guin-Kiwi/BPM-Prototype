from dataclasses import dataclass


@dataclass(frozen=True)
class Report:
    id: str
    farm_id: str
    field_id: str | None
    observation_date: str
    description: str
    received_at: str
    image: bytes | None = None
    image_type: str | None = None
    finding: str | None = None
    observation_time: str | None = None
    observation_source: str | None = None
    observation_precision: str | None = None
    photo_source: str | None = None
    estimate_kind: str | None = None
    estimate_value: float | None = None
    estimate_unit: str | None = None
    estimate_source: str | None = None
    area_cue: str | None = None
    latitude: float | None = None
    longitude: float | None = None
    accuracy: float | None = None
    fix_time: str | None = None
    location_source: str | None = None
    farmer_id: str | None = None
