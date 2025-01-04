import logging
from typing import Type, TypeVar

from google.api_core.exceptions import InternalServerError, ResourceExhausted, ServiceUnavailable
from google.generativeai import GenerationConfig, GenerativeModel
from google.generativeai.types import AsyncGenerateContentResponse, HarmBlockThreshold, HarmCategory
from pydantic import BaseModel
from tenacity import retry, retry_if_exception_type, stop_after_attempt, wait_exponential

from app.core.exceptions import GeminiAPIError

logger = logging.getLogger(__name__)

NONE_SAFETY_SETTINGS = {
    HarmCategory.HARM_CATEGORY_DANGEROUS_CONTENT: HarmBlockThreshold.BLOCK_NONE,
    HarmCategory.HARM_CATEGORY_HARASSMENT: HarmBlockThreshold.BLOCK_NONE,
    HarmCategory.HARM_CATEGORY_HATE_SPEECH: HarmBlockThreshold.BLOCK_NONE,
    HarmCategory.HARM_CATEGORY_SEXUALLY_EXPLICIT: HarmBlockThreshold.BLOCK_NONE,
}


ModelType = TypeVar("ModelType", bound=BaseModel)


async def generate_content_async_with_response_schema(
    model: GenerativeModel,
    contents: list[str],
    response_schema: Type[ModelType],
    temperature: float = 0.2,
    top_k: int = 40,
) -> ModelType:
    try:
        return await _generate_content_async_with_response_schema(model, contents, response_schema, temperature, top_k)
    except ResourceExhausted as ex:
        logger.exception(f"Gemini quota has been exhausted: {ex.message}")
        raise GeminiAPIError("Gemini quota exhausted")
    except (InternalServerError, ServiceUnavailable) as ex:
        logger.exception(f"Internal Gemini error: {ex.message}")
        raise GeminiAPIError("Internal Gemini Error")
    except Exception as ex:
        logger.exception(f"Unknown Gemini error: {str(ex)}")
        raise GeminiAPIError("Unknown Gemini error")


@retry(
    retry=retry_if_exception_type((InternalServerError, ServiceUnavailable)),
    wait=wait_exponential(),
    stop=stop_after_attempt(3),
    reraise=True,
)
async def _generate_content_async_with_response_schema(
    model: GenerativeModel,
    contents: list[str],
    response_schema: Type[ModelType],
    temperature: float = 0.2,
    top_k: int = 40,
) -> ModelType:
    generation_config = GenerationConfig(
        temperature=temperature, top_k=top_k, response_mime_type="application/json", response_schema=response_schema
    )
    llm_response = await model.generate_content_async(
        contents=contents, generation_config=generation_config, safety_settings=NONE_SAFETY_SETTINGS
    )
    return to_pydantic_model(llm_response, response_schema)


def to_pydantic_model(gemini_response: AsyncGenerateContentResponse, pydantic_model: Type[ModelType]) -> ModelType:
    return pydantic_model.model_validate_json(gemini_response.text)
