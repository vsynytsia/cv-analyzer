from collections.abc import Sequence

import jinja2

from app.helpers import concurrency, genai, utils
from app.schemas.vacancies import ScoredVacancy, Vacancy
from app.services.score.schemas import ScoredVacanciesLlmResponse


async def score_vacancies(
    gemini_client: genai.GenerativeModel, jinja_env: jinja2.Environment, cv: str, vacancies: Sequence[Vacancy]
) -> list[ScoredVacancy]:
    chunked_vacancies = _chunk_vacancies(vacancies)
    scored_vacancies_llm_responses = await concurrency.gather(
        items=chunked_vacancies,
        coro_factory=lambda chunk: _score_chunk(jinja_env, gemini_client, cv, chunk),
        post_processor=lambda x: utils.flatten_list(utils.filter_exceptions([result.scored_vacancies for result in x])),
    )

    scored_vacancies = [
        ScoredVacancy(**vacancy.model_dump(), relevance=llm_response.relevance_score, reasoning=llm_response.reasoning)
        for vacancy, llm_response in zip(vacancies, scored_vacancies_llm_responses, strict=False)
    ]
    return sort_vacancies_by_relevancy_score(scored_vacancies)


def sort_vacancies_by_relevancy_score(vacancies: list[ScoredVacancy]) -> list[ScoredVacancy]:
    return sorted(vacancies, key=lambda v: v.relevance, reverse=True)


def _chunk_vacancies(vacancies: Sequence[Vacancy], chunk_size: int = 5) -> list[Sequence[Vacancy]]:
    return [vacancies[i : i + chunk_size] for i in range(0, len(vacancies), chunk_size)]


async def _score_chunk(
    jinja_env: jinja2.Environment, gemini_client: genai.GenerativeModel, cv: str, chunk: Sequence[Vacancy]
) -> ScoredVacanciesLlmResponse:
    prompt = _get_vacancies_scoring_prompt(jinja_env, cv, chunk)
    return await genai.generate_content_async_with_response_schema(
        model=gemini_client,
        contents=[prompt],
        response_schema=ScoredVacanciesLlmResponse,
        top_k=1,
        temperature=0,
    )


def _get_vacancies_scoring_prompt(jinja_env: jinja2.Environment, cv: str, vacancies: Sequence[Vacancy]) -> str:
    prompt_template = jinja_env.get_template("score/prompts/score.j2")
    return prompt_template.render(cv=cv, vacancies=vacancies)
