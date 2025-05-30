import abc
from dataclasses import dataclass
from typing import Iterable, TypeAlias

import googletrans

from app.core.exceptions import TextTranslationError

__all__ = ["TextTranslationConfig", "TextTranslator", "GoogletransTextTranslator"]

GoogletransTranslation: TypeAlias = googletrans.client.Translated | list[googletrans.client.Translated]


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


class GoogletransTextTranslator(TextTranslator):
    def __init__(self):
        self._client = googletrans.Translator()

    async def translate(self, text: str, translation_config: TextTranslationConfig) -> str:
        translation = await self._translate(text, translation_config)
        return translation.text

    async def batch_translate(self, texts: list[str], translation_config: TextTranslationConfig) -> list[str]:
        translations = await self._translate(texts, translation_config)
        return [t.text for t in translations]

    async def _translate(
        self, text: str | list[str], translation_config: TextTranslationConfig
    ) -> GoogletransTranslation:
        async with self._client:
            try:
                return await self._client.translate(
                    text, src=translation_config.source_language, dest=translation_config.target_language
                )
            except Exception as ex:
                raise TextTranslationError() from ex
