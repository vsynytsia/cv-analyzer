from .base import UpstreamServiceError

__all__ = ["TextTranslationError"]


class TextTranslationError(UpstreamServiceError):
    code = "text_translation_error"

    def __init__(self) -> None:
        super().__init__("Error translating text")
