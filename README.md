# CV Analyzer

A platform for analyzing CVs and matching them with relevant job vacancies.

## Overview

This project provides an API for processing CVs, extracting key information, and matching them against job vacancies from popular Ukrainian job boards (DOU and Djinni). It leverages large language models (LLMs) via Google's Gemini API for text analysis and scoring.

## Features

-   **CV Processing:** Extracts text from PDF CVs.
-   **Language Support:** Detects and translates CVs to English for consistent processing.
-   **Search Filter Extraction:** Uses LLMs to extract relevant search filters (experience, job category) from CVs.
-   **Vacancy Fetching:** Fetches job vacancies from DOU and Djinni based on extracted filters.
-   **Vacancy Scoring:** Scores fetched vacancies based on their relevance to the CV using LLMs.
-   **API:** Provides a RESTful API built with FastAPI.
-   **Dockerized:** Easily deployable using Docker.
-   **Automated Code Quality:** Uses `ruff` for linting and formatting, and `pre-commit` for code quality checks.

## Getting Started

### Prerequisites

-   Python 3.11
-   Docker
-   A Google Generative AI API key

### Installation

1.  **Clone the repository:**

    ```bash
    git clone <your_repo_url>
    cd <your_repo_directory>
    ```

2.  **Create a `.env` file:**
    Copy the contents of `.env.example` to a new file named `.env` and fill in your Google Generative AI API key.

    ```
    GOOGLE_GENAI_API_KEY="YOUR_API_KEY"
    ```

3.  **Build the Docker image:**

    ```bash
    docker build -t cv-analyzer .
    ```

4.  **Run the Docker container:**

    ```bash
    docker run -p 8080:8080 cv-analyzer
    ```

    The API will now be accessible at `http://localhost:8080`.

## API Usage

The API documentation is available at `http://localhost:8080/docs` when the application is running.

### Endpoints

-   **`POST /cv-operations/match-vacancies`**: Upload a PDF CV to process and get scored vacancies.
    -   **Request Body:** `multipart/form-data` with a file named `cv`.
    -   **Response:** A JSON array of `ScoredVacancy` objects.
-   **`GET /`**: Redirects to the API documentation.
-   **`GET /v1/utils/healthcheck`**: Returns `true` if the API is healthy.

### Example Request

```bash
curl -X POST \
  -H "Content-Type: multipart/form-data" \
  -F "cv=@/path/to/your/cv.pdf" \
  http://localhost:8080/cv-operations/match-vacancies
