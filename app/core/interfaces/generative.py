import abc
from dataclasses import dataclass
from typing import Any, Generic, Type, TypeVar

from pydantic import BaseModel

__all__ = ["GenerationConfig", "ContentGenerator", "PromptManager"]

TResponseModel = TypeVar("TResponseModel", bound=BaseModel)


@dataclass
class GenerationConfig(Generic[TResponseModel]):
    temperature: float | None = None
    top_p: float | None = None
    top_k: int | None = None
    response_model: Type[TResponseModel] | None = None


class ContentGenerator(abc.ABC):
    @abc.abstractmethod
    async def generate_structured_content(
        self, prompt: str, generation_config: GenerationConfig[TResponseModel]
    ) -> TResponseModel:
        pass


class PromptManager(abc.ABC):
    @abc.abstractmethod
    def render_prompt_template(self, prompt_template_path: str, **prompt_params) -> str:
        raise NotImplementedError

    @abc.abstractmethod
    def get_prompt_template(self, prompt_template_path: str) -> Any:
        raise NotImplementedError
