import json
from typing import Type, TypeVar

from google.generativeai.types import AsyncGenerateContentResponse
from pydantic import BaseModel

ModelType = TypeVar("ModelType", bound=BaseModel)


def convert_gemini_response_to_pydantic_model(
    gemini_response: AsyncGenerateContentResponse, pydantic_model: Type[ModelType]
) -> ModelType:
    gemini_response_dict = json.loads(gemini_response.text)
    return pydantic_model.model_validate(gemini_response_dict)
