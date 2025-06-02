import abc

__all__ = ["IFileTextExtractor"]


class IFileTextExtractor(abc.ABC):
    @abc.abstractmethod
    def extract_text(self, file: bytes) -> str:
        raise NotImplementedError
