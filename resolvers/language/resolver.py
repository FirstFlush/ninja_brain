from ..base_resolver import BaseResolver
from .dataclasses import ResolvedLanguage
from .enums import LanguageEnum

class LanguageResolver(BaseResolver):

    def resolve(self) -> ResolvedLanguage:
        """Currently only support for English language """
        return ResolvedLanguage(
            language=LanguageEnum.ENGLISH,
        )    
    