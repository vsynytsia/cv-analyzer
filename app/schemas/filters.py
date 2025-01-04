from abc import ABC, abstractmethod
from enum import StrEnum
from typing import Any

from app.core.settings import settings


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
    FRONTEND = "Front End"
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


class JobSearchFilter(ABC):
    @property
    @abstractmethod
    def website_url(self) -> str:
        pass

    @abstractmethod
    def to_http_request_params(self) -> dict[str, Any]:
        pass

    @abstractmethod
    def normalize_experience(self) -> str:
        pass


class DjinniSearchFilter(JobSearchFilter):
    def __init__(self, experience_years: int, category: DjinniCategory):
        self.experience_years = experience_years
        self.category = category

    @property
    def website_url(self) -> str:
        return settings.DJINNI_VACANCIES_BASE_URL

    def to_http_request_params(self) -> dict[str, Any]:
        normalized_experience = self.normalize_experience()
        return {"primary_keyword": self.category.value, "exp_level": normalized_experience}

    def normalize_experience(self) -> str:
        if self.experience_years <= 0:
            return "no_exp"
        else:
            return f"{min(self.experience_years, 10)}y"


class DouSearchFilter(JobSearchFilter):
    def __init__(self, experience_years: int, category: DouCategory):
        self.experience_years = experience_years
        self.category = category

    @property
    def website_url(self) -> str:
        return settings.DOU_VACANCIES_BASE_URL

    def to_http_request_params(self) -> dict[str, Any]:
        normalized_experience = self.normalize_experience()
        return {"category": self.category.value, "exp": normalized_experience}

    def normalize_experience(self) -> str:
        if 0 <= self.experience_years < 1:
            return "0-1"
        elif 1 <= self.experience_years < 3:
            return "1-3"
        elif 3 <= self.experience_years < 5:
            return "3-5"
        else:
            return "5plus"
