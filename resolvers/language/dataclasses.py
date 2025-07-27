from dataclasses import dataclass
from .enums import LanguageEnum


@dataclass
class ResolvedLanguage:
    language: LanguageEnum