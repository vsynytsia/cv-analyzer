from collections.abc import Sequence

import jinja2
from google import generativeai as genai

from app.schemas.vacancy import ScoredVacancy, Vacancy
from app.services import genai_service
from app.services.score.converters import convert_vacancy_to_scored_vacancy
from app.services.score.schemas import ScoredVacanciesLlmResponse
from app.utils import execute_tasks_async, filter_out_exceptions, flatten_2d_list


async def score_vacancies(
    gemini_client: genai.GenerativeModel, jinja_env: jinja2.Environment, cv: str, vacancies: Sequence[Vacancy]
) -> list[ScoredVacancy]:
    chunked_vacancies = _chunk_vacancies(vacancies)
    scored_vacancies_llm_responses = await execute_tasks_async(
        items=chunked_vacancies,
        coro_factory=lambda chunk: _score_chunk(jinja_env, gemini_client, cv, chunk),
        post_processor=lambda x: flatten_2d_list(filter_out_exceptions([result.scored_vacancies for result in x])),
    )

    scored_vacancies = [
        convert_vacancy_to_scored_vacancy(vacancy, llm_response.relevancy_score, llm_response.reasoning)
        for vacancy, llm_response in zip(vacancies, scored_vacancies_llm_responses, strict=False)
    ]
    return sort_vacancies_by_relevancy_score(scored_vacancies)


def sort_vacancies_by_relevancy_score(vacancies: list[ScoredVacancy]) -> list[ScoredVacancy]:
    return sorted(vacancies, key=lambda v: v.relevancy_score, reverse=True)


def _chunk_vacancies(vacancies: Sequence[Vacancy], chunk_size: int = 5) -> list[Sequence[Vacancy]]:
    return [vacancies[i : i + chunk_size] for i in range(0, len(vacancies), chunk_size)]


async def _score_chunk(
    jinja_env: jinja2.Environment, gemini_client: genai.GenerativeModel, cv: str, chunk: Sequence[Vacancy]
) -> ScoredVacanciesLlmResponse:
    prompt = _get_vacancies_scoring_prompt(jinja_env, cv, chunk)
    return await genai_service.generate_content_async_with_response_schema(
        gemini_client=gemini_client,
        contents=[prompt],
        response_schema=ScoredVacanciesLlmResponse,
        top_k=1,
        temperature=0,
    )


def _get_vacancies_scoring_prompt(jinja_env: jinja2.Environment, cv: str, vacancies: Sequence[Vacancy]) -> str:
    prompt_template = jinja_env.get_template("score.j2")
    return prompt_template.render(cv=cv, vacancies=vacancies)
