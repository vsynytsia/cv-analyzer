from dataclasses import dataclass
from typing import Iterable, Protocol

__all__ = ["ITextLanguageDetector", "TextTranslationConfig", "ITextTranslator"]


class ITextLanguageDetector(Protocol):
    def detect_language(self, text: str) -> str:
        pass


@dataclass
class TextTranslationConfig:
    source_language: str
    target_language: str


class ITextTranslator(Protocol):
    async def translate(self, text: str, translation_config: TextTranslationConfig) -> str:
        pass

    async def batch_translate(self, texts: Iterable[str], translation_config: TextTranslationConfig) -> list[str]:
        pass
