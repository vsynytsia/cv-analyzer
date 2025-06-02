import langdetect

from app.core.exceptions import TextLanguageDetectionError
from app.core.interfaces import ITextLanguageDetector

__all__ = ["LangdetectITextLanguageDetector"]


class LangdetectITextLanguageDetector(ITextLanguageDetector):
    def detect_language(self, text: str) -> str:
        try:
            return langdetect.detect(text)
        except Exception as ex:
            raise TextLanguageDetectionError() from ex
