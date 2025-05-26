import logging
from collections.abc import Sequence

import jinja2

from app.helpers import utils
from app.helpers.generative import ContentGenerator, GenerationConfig
from app.models.domain import ScoredVacancy, Vacancy, VacancyScore
from app.models.generative import ScoredVacanciesLlmResponse, VacancyScoringPromptParams

__all__ = ["VacancyScoringService"]


class VacancyScoringService:
    def __init__(self, content_generator: ContentGenerator, jinja_env: jinja2.Environment) -> None:
        self._content_generator = content_generator
        self._jinja_env = jinja_env
        self._logger = logging.getLogger(self.__class__.__name__)

    async def score_vacancies(self, cv: str, vacancies: Sequence[Vacancy]) -> list[ScoredVacancy]:
        chunked_vacancies = utils.chunk(vacancies)
        scored_vacancies = await utils.gather(
            items=chunked_vacancies,
            coro_factory=lambda chunk: self._score_vacancies(cv, chunk),
            post_processor=lambda x: utils.flatten_list(utils.filter_exceptions(x)),
        )
        sorted_vacancies = self._sort_vacancies_by_relevancy_score(scored_vacancies)

        self._logger.info("Scored & sorted %d vacancies", len(sorted_vacancies))
        return sorted_vacancies

    async def _score_vacancies(self, cv: str, vacancies: Sequence[Vacancy]) -> list[ScoredVacancy]:
        prompt = self._get_vacancies_scoring_prompt(cv, vacancies)
        response = await self._content_generator.generate_structured_content(
            prompt=prompt,
            generation_config=GenerationConfig(temperature=0, top_k=1, response_model=ScoredVacanciesLlmResponse),
        )
        return self._enrich_vacancies_with_scored_vacancies_llm_response(response, vacancies)

    def _get_vacancies_scoring_prompt(self, cv: str, vacancies: Sequence[Vacancy]) -> str:
        return utils.get_rendered_template(
            env=self._jinja_env,
            template_path="vacancy_scoring.tpl",
            **VacancyScoringPromptParams(cv=cv, vacancies=vacancies),
        )

    @staticmethod
    def _enrich_vacancies_with_scored_vacancies_llm_response(
        r: ScoredVacanciesLlmResponse, vacancies: Sequence[Vacancy]
    ) -> list[ScoredVacancy]:
        return [
            ScoredVacancy(
                **vacancy.model_dump(),
                score=VacancyScore(score=llm_response.relevance_score, reasoning=llm_response.reasoning),
            )
            for vacancy, llm_response in zip(vacancies, r.scored_vacancies, strict=False)
        ]

    @staticmethod
    def _sort_vacancies_by_relevancy_score(vacancies: list[ScoredVacancy]) -> list[ScoredVacancy]:
        return sorted(vacancies, key=lambda v: v.score.score, reverse=True)
