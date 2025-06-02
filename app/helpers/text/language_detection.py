import langdetect

from app.core.exceptions import TextLanguageDetectionError
from app.core.interfaces import TextLanguageDetector

__all__ = ["LangdetectTextLanguageDetector"]


class LangdetectTextLanguageDetector(TextLanguageDetector):
    def detect_language(self, text: str) -> str:
        try:
            return langdetect.detect(text)
        except Exception as ex:
            raise TextLanguageDetectionError() from ex
