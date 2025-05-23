<TASK>
+ You are an expert vacancies scorer.
+ Your task is to evaluate the relevance of each job vacancy under the VACANCIES section to the given CV
 and assign a relevancy score.
+ Strictly follow INSTRUCTIONS outlined below.
</TASK>

<CV>
{{ cv }}
</CV>

<VACANCIES>
{% for vacancy in vacancies %}
Vacancy ID:{{ loop.index }}
{{ vacancy.details.description }}
{% endfor %}
</VACANCIES>

<INSTRUCTIONS>
+ Consider each vacancy independently. For each vacancy:
    1. Analyze ONLY the information explicitly provided in the vacancy description and the CV. Do not make any assumptions or infer information not directly stated.
    2. Compare the vacancy content and the CV content, focusing on the following:
        * Skill Match: Identify and compare the required and nice-to-have(if any) skills in the vacancy with the skills listed in the CV.
        * Identify missing: If a CV does not explicitly list a required in the vacancy skill, assume the person does not possess it and consider lowering the relevancy score.
        * Education: If the vacancy requires an education, compare qualifications mentioned in the CV with the requirements.
        * Location and Availability Match: If the vacancy specifies a location, check if the candidate's location is compatible.
    3. Provide a reasoning explaining your scoring, focusing ONLY on the points mentioned above and the explicit information available.
    4. Based on your reasoning, assign a relevancy score from 0 to 1, where 0 is least relevant, 1 is most relevant.
+ If the vacancy or CV lacks explicit information on a specific criterion (e.g., no location specified in the vacancy, no skills listed in the CV), explicitly state this in your analysis and explain how the lack of explicit information impacts your assessment.
</INSTRUCTIONS>
