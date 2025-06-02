import abc

__all__ = ["TextLanguageDetector", "TextTranslationConfig", "TextTranslator"]

from dataclasses import dataclass
from typing import Iterable


class TextLanguageDetector(abc.ABC):
    @abc.abstractmethod
    def detect_language(self, text: str) -> str:
        raise NotImplementedError


@dataclass
class TextTranslationConfig:
    source_language: str
    target_language: str


class TextTranslator(abc.ABC):
    @abc.abstractmethod
    async def translate(self, text: str, translation_config: TextTranslationConfig) -> str:
        raise NotImplementedError

    @abc.abstractmethod
    async def batch_translate(self, texts: Iterable[str], translation_config: TextTranslationConfig) -> list[str]:
        raise NotImplementedError
