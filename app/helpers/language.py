from collections.abc import Iterable

import googletrans
import langdetect

from app.core.exceptions import TranslationAPIError


def detect_text_language(text: str) -> str:
    return langdetect.detect(text)


async def translate_text(text: str, source_language: str, target_language: str) -> str:
    translation = await _translate_safe(text, source_language, target_language)
    return translation.text


async def translate_texts(texts: Iterable[str], source_language: str, target_language: str) -> list[str]:
    translations = await _translate_safe(texts, source_language, target_language)
    return [translation.text for translation in translations]


async def _translate_safe(
    text: str | Iterable[str], source_language: str, target_language: str
) -> googletrans.client.Translated | list[googletrans.client.Translated]:
    try:
        return await _translate(text, source_language, target_language)
    except Exception as ex:
        raise TranslationAPIError(f"Upstream translation API error: {str(ex)}")


async def _translate(
    text: str | Iterable[str], source_language: str, target_language: str
) -> googletrans.client.Translated | list[googletrans.client.Translated]:
    async with googletrans.Translator() as translator:
        translation = await translator.translate(text, source_language, target_language)
    return translation
