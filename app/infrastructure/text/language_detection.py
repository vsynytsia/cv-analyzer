import langdetect

from app.core.exceptions import TextLanguageDetectionError

__all__ = ["LangdetectTextLanguageDetector"]


class LangdetectTextLanguageDetector:
    def detect_language(self, text: str) -> str:
        try:
            return langdetect.detect(text)
        except Exception as ex:
            raise TextLanguageDetectionError() from ex
