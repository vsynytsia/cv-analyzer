import abc

import langdetect

from app.core.exceptions import TextLanguageDetectionError

__all__ = ["TextLanguageDetector", "LangdetectTextLanguageDetector"]


class TextLanguageDetector(abc.ABC):
    @abc.abstractmethod
    def detect_language(self, text: str) -> str:
        raise NotImplementedError


class LangdetectTextLanguageDetector(TextLanguageDetector):
    def detect_language(self, text: str) -> str:
        try:
            return langdetect.detect(text)
        except Exception as ex:
            raise TextLanguageDetectionError() from ex
