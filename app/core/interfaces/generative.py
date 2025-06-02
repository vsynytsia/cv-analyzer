from dataclasses import dataclass
from typing import Any, Generic, Protocol, Type, TypeVar

from pydantic import BaseModel

__all__ = ["GenerationConfig", "IContentGenerator", "IPromptManager"]

TResponseModel = TypeVar("TResponseModel", bound=BaseModel)


@dataclass
class GenerationConfig(Generic[TResponseModel]):
    temperature: float | None = None
    top_p: float | None = None
    top_k: int | None = None
    response_model: Type[TResponseModel] | None = None


class IContentGenerator(Protocol):
    async def generate_structured_content(
        self, prompt: str, generation_config: GenerationConfig[TResponseModel]
    ) -> TResponseModel:
        pass


class IPromptManager(Protocol):
    def render_prompt_template(self, prompt_template_path: str, **prompt_params) -> str:
        pass

    def get_prompt_template(self, prompt_template_path: str) -> Any:
        pass
