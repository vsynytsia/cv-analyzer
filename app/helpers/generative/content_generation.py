import abc
from dataclasses import dataclass
from typing import Generic, Type, TypeVar

from google import generativeai as genai
from google.api_core.exceptions import InternalServerError, ServiceUnavailable
from pydantic import BaseModel
from tenacity import retry, retry_if_exception_type, stop_after_attempt, wait_exponential

__all__ = ["GenerationConfig", "ContentGenerator", "GoogleGenaiContentGenerator"]

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


class GoogleGenaiContentGenerator(ContentGenerator):
    DEFAULT_SAFETY_SETTINGS = {
        genai.types.HarmCategory.HARM_CATEGORY_DANGEROUS_CONTENT: genai.types.HarmBlockThreshold.BLOCK_NONE,
        genai.types.HarmCategory.HARM_CATEGORY_HARASSMENT: genai.types.HarmBlockThreshold.BLOCK_NONE,
        genai.types.HarmCategory.HARM_CATEGORY_HATE_SPEECH: genai.types.HarmBlockThreshold.BLOCK_NONE,
        genai.types.HarmCategory.HARM_CATEGORY_SEXUALLY_EXPLICIT: genai.types.HarmBlockThreshold.BLOCK_NONE,
    }
    RESPONSE_MIME_TYPE_JSON = "application/json"

    def __init__(self, model_name: str = "gemini-2.5-flash-preview-04-17") -> None:
        self._model = genai.GenerativeModel(model_name=model_name)

    @retry(
        retry=retry_if_exception_type((InternalServerError, ServiceUnavailable)),
        wait=wait_exponential(),
        stop=stop_after_attempt(3),
        reraise=True,
    )
    async def generate_structured_content(
        self, prompt: str, generation_config: GenerationConfig[TResponseModel]
    ) -> TResponseModel:
        response_model = generation_config.response_model

        response = await self._model.generate_content_async(
            contents=prompt,
            safety_settings=self.DEFAULT_SAFETY_SETTINGS,
            generation_config=genai.GenerationConfig(
                temperature=generation_config.temperature,
                top_p=generation_config.top_p,
                top_k=generation_config.top_k,
                response_mime_type=self.RESPONSE_MIME_TYPE_JSON,
                response_schema=response_model,
            ),
        )

        return response_model.model_validate_json(response.text)
