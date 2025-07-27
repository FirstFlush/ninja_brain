from dataclasses import dataclass, field
from typing import Any, Optional
from ..resource.dataclasses import ResolvedResource
from ..language.dataclasses import ResolvedLanguage
from ..location.datalasses import ResolvedLocation
from ..qualifier.dataclasses import ParamDict


@dataclass
class ResolvedSmsInquiry:
    msg: str
    language: ResolvedLanguage
    resource: ResolvedResource
    location: ResolvedLocation
    params: Optional[ParamDict] = field(default=None)
