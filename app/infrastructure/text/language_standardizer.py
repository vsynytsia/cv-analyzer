import logging
from collections import defaultdict
from collections.abc import Sequence
from dataclasses import dataclass

from app.core.interfaces import ITextLanguageDetector, ITextTranslator, TextTranslationConfig

__all__ = ["TextLanguageStandardizer", "TextLanguageStandardizationConfig"]


@dataclass
class TextLanguageStandardizationConfig:
    primary_language: str
    secondary_languages: Sequence[str]


class TextLanguageStandardizer:
    def __init__(self, text_language_detector: ITextLanguageDetector, text_translator: ITextTranslator) -> None:
        self._text_language_detector = text_language_detector
        self._text_translator = text_translator
        self._logger = logging.getLogger(self.__class__.__name__)

    async def standardize_text_language(
        self, texts: Sequence[str], standardization_config: TextLanguageStandardizationConfig
    ) -> list[str]:
        standardized_texts = [None] * len(texts)
        translation_needed: dict[str, list[tuple[int, str]]] = defaultdict(list)

        for i, text in enumerate(texts):
            text_language = self._text_language_detector.detect_language(text)

            if text_language == standardization_config.primary_language:
                standardized_texts[i] = text
                continue

            if text_language in standardization_config.secondary_languages:
                translation_needed[text_language].append((i, text))
            else:
                self._logger.warning("Encountered unknown language while standardizing: %s", text_language)
                standardized_texts[i] = text
                continue

        for source_language, items in translation_needed.items():
            original_indices_this_batch = [item[0] for item in items]
            texts_this_batch = [item[1] for item in items]

            translated_texts_this_batch = await self._text_translator.batch_translate(
                texts_this_batch,
                translation_config=TextTranslationConfig(
                    source_language=source_language, target_language=standardization_config.primary_language
                ),
            )

            self._logger.info(
                "Translated %d texts from '%s' to '%s'",
                len(translated_texts_this_batch),
                source_language,
                standardization_config.primary_language,
            )

            for i, translated_text in zip(original_indices_this_batch, translated_texts_this_batch, strict=False):
                standardized_texts[i] = translated_text

        return standardized_texts
