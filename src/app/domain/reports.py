from dataclasses import dataclass


@dataclass(frozen=True)
class Report:
    id: str
    farm_id: str
    field_id: str
    observation_date: str
    description: str
    received_at: str
    image: bytes | None = None
    image_type: str | None = None
    finding: str | None = None
