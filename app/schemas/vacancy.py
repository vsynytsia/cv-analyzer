from enum import StrEnum

from pydantic import BaseModel, field_validator


class VacancyCategory(StrEnum):
    pass


class DouCategory(VacancyCategory):
    JAVA = "Java"
    PYTHON = "Python"
    DOTNET = ".NET"
    AIML = "AI/ML"
    PHP = "PHP"
    GOLANG = "Golang"
    CPP = "C++"
    IOS_MACOS = "iOS/macOS"
    QA = "QA"
    ANDROID = "Android"
    FRONTEND = "Frontend"
    PROJECT_MANAGER = "Project Manager"
    PRODUCT_MANAGER = "Product Manager"
    HR = "HR"
    NODE_JS = "Node.js"
    DESIGN = "Design"
    SALES = "Sales"
    MARKETING = "Marketing"
    ANALYST = "Analyst"
    DEVOPS = "DevOps"
    MILTECH = "Miltech"
    GOVTECH = "Govtech"
    ACCOUNT_MANAGER = "Account Manager"
    ANIMATOR = "Animator"
    ARCHITECT = "Architect"
    BIG_DATA = "Big Data"
    DATA_ENGINEER = "Data Engineer"
    EMBEDDED = "Embedded"
    FINANCE = "Finance"
    RUBY = "Ruby"
    SUPPORT = "Support"
    SYSADMIN = "SysAdmin"
    HARDWARE = "Hardware"
    DATA_SCIENCE = "Data Science"


class DjinniCategory(VacancyCategory):
    JAVASCRIPT = "JavaScript"
    ANGULAR = "Angular"
    REACTJS = "React.js"
    VUEJS = "Vue.js"
    SVELTE = "Svelte"
    FULLSTACK = "Fullstack"
    JAVA = "Java"
    DOTNET = ".NET"
    PHP = "PHP"
    PYTHON = "Python"
    NODE_JS = "Node.js"
    IOS = "iOS"
    ANDROID = "Android"
    REACT_NATIVE = "React Native"
    C = "C"
    FLUTTER = "Flutter"
    GOLANG = "Golang"
    RUBY = "Ruby"
    SCALA = "Scala"
    SALESFORCE = "Salesforce"
    RUST = "Rust"
    ELIXIR = "Elixir"
    KOTLIN = "Kotlin"
    ERP = "ERP"
    QA_MANUAL = "QA"
    QA_AUTOMATION = "QA Automation"
    DESIGN = "Design"
    GAMEDEV = "Unity"
    PROJECT_MANAGER = "Project Manager"
    PRODUCT_MANAGER = "Product Manager"
    DEVOPS = "DevOps"
    BUSINESS_ANALYST = "Business Analyst"
    DATA_SCIENCE = "Data Science"
    DATA_ANALYST = "Data Analyst"


class VacancySource(StrEnum):
    DOU = "dou"
    DJINNI = "djinni"


class VacancySearchFilter(BaseModel):
    source: VacancySource
    years_of_experience: int
    category: VacancyCategory


class Vacancy(BaseModel):
    url: str
    description: str
    job_title: str | None
    company_name: str | None
    salary: str | None


class ScoredVacancy(BaseModel):
    url: str
    job_title: str | None
    company_name: str | None
    salary: str | None
    relevancy_score: float
    reasoning: str

    @field_validator("relevancy_score")
    def round_float(cls, v: float) -> float:
        return round(v, 2)
