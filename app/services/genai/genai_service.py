import logging
from typing import Type, TypeVar

from google.api_core.exceptions import InternalServerError, ResourceExhausted, ServiceUnavailable
from google.generativeai import GenerationConfig, GenerativeModel
from google.generativeai.types import HarmBlockThreshold, HarmCategory
from pydantic import BaseModel
from tenacity import retry, retry_if_exception_type, stop_after_attempt, wait_exponential

from app.core.exceptions import GeminiAPIError
from app.services.genai.converters import convert_gemini_response_to_pydantic_model

logger = logging.getLogger(__name__)

NONE_SAFETY_SETTINGS = {
    HarmCategory.HARM_CATEGORY_DANGEROUS_CONTENT: HarmBlockThreshold.BLOCK_NONE,
    HarmCategory.HARM_CATEGORY_HARASSMENT: HarmBlockThreshold.BLOCK_NONE,
    HarmCategory.HARM_CATEGORY_HATE_SPEECH: HarmBlockThreshold.BLOCK_NONE,
    HarmCategory.HARM_CATEGORY_SEXUALLY_EXPLICIT: HarmBlockThreshold.BLOCK_NONE,
}


ModelType = TypeVar("ModelType", bound=BaseModel)


async def generate_content_async_with_response_schema(
    gemini_client: GenerativeModel,
    contents: list[str],
    response_schema: Type[ModelType],
    temperature: float = 0.2,
    top_k: int = 40,
) -> ModelType:
    try:
        return await _generate_content_async_with_response_schema(
            gemini_client, contents, response_schema, temperature, top_k
        )
    except ResourceExhausted:
        logger.exception("Gemini quota has been exhausted.")
        raise GeminiAPIError("Gemini quota exhausted")
    except (InternalServerError, ServiceUnavailable):
        logger.exception("Internal Gemini error")
        raise GeminiAPIError("Internal Gemini Error")
    except Exception as ex:
        logger.exception(f"Unknown Gemini error: {str(ex)}")
        raise GeminiAPIError("Unknown Gemini error") from ex


@retry(
    retry=retry_if_exception_type((InternalServerError, ServiceUnavailable)),
    wait=wait_exponential(),
    stop=stop_after_attempt(5),
    reraise=True,
)
async def _generate_content_async_with_response_schema(
    gemini_client: GenerativeModel,
    contents: list[str],
    response_schema: Type[ModelType],
    temperature: float = 0.2,
    top_k: int = 40,
) -> ModelType:
    generation_config = GenerationConfig(
        temperature=temperature, top_k=top_k, response_mime_type="application/json", response_schema=response_schema
    )
    llm_response = await gemini_client.generate_content_async(
        contents=contents, generation_config=generation_config, safety_settings=NONE_SAFETY_SETTINGS
    )
    return convert_gemini_response_to_pydantic_model(llm_response, response_schema)
