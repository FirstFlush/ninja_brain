from dataclasses import dataclass
from .enums import LocationType

@dataclass
class ResolvedLocation:
    location_text: str
    location_type: LocationType