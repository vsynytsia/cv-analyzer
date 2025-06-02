from typing import TypeVar

from google import generativeai as genai
from google.api_core.exceptions import InternalServerError, ServiceUnavailable
from google.generativeai.types import AsyncGenerateContentResponse
from pydantic import BaseModel, ValidationError
from tenacity import retry, retry_if_exception_type, stop_after_attempt, wait_exponential

from app.core.exceptions import ContentGenerationError, GenerativeResponseModelConversionError
from app.core.interfaces import ContentGenerator, GenerationConfig

__all__ = ["GoogleGenaiContentGenerator"]


TResponseModel = TypeVar("TResponseModel", bound=BaseModel)


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

    async def generate_structured_content(
        self, prompt: str, generation_config: GenerationConfig[TResponseModel]
    ) -> TResponseModel:
        try:
            response = await self._generate_structured_content(prompt, generation_config)
            text_response = response.text
        except Exception as ex:
            raise ContentGenerationError(prompt) from ex

        try:
            return generation_config.response_model.model_validate_json(text_response)
        except ValidationError as ex:
            raise GenerativeResponseModelConversionError(text_response, generation_config.response_model) from ex

    @retry(
        retry=retry_if_exception_type((InternalServerError, ServiceUnavailable)),
        wait=wait_exponential(),
        stop=stop_after_attempt(3),
        reraise=True,
    )
    async def _generate_structured_content(
        self, prompt: str, generation_config: GenerationConfig[TResponseModel]
    ) -> AsyncGenerateContentResponse:
        response = await self._model.generate_content_async(
            contents=prompt,
            safety_settings=self.DEFAULT_SAFETY_SETTINGS,
            generation_config=genai.GenerationConfig(
                temperature=generation_config.temperature,
                top_p=generation_config.top_p,
                top_k=generation_config.top_k,
                response_mime_type=self.RESPONSE_MIME_TYPE_JSON,
                response_schema=generation_config.response_model,
            ),
        )

        return response
