from .base import UpstreamServiceError

__all__ = ["TextLanguageDetectionError"]


class TextLanguageDetectionError(UpstreamServiceError):
    code = "text_language_detection_error"

    def __init__(self) -> None:
        super().__init__("Failed to detect text language")
