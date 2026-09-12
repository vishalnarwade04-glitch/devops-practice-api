# devops-practice-api

A small Flask REST API built as a hands-on exercise in CI/CD fundamentals — from writing tests through to a fully automated pipeline that builds, tests, and publishes a container image on every push.

## What it does

A simple task-list API with four endpoints:

| Method | Endpoint          | Description                  |
|--------|-------------------|-------------------------------|
| GET    | `/health`         | Health check                  |
| GET    | `/tasks`          | List all tasks                |
| POST   | `/tasks`          | Create a new task              |
| DELETE | `/tasks/<id>`     | Delete a task by ID            |

## Stack

- **Flask** — the API itself
- **pytest** — unit tests (health check, list, create, validation, delete-not-found)
- **Docker** — containerized, multi-stage-friendly `Dockerfile`
- **GitHub Actions** — CI/CD pipeline
- **GitHub Container Registry (GHCR)** — image hosting

## CI/CD pipeline

Every push to `main` (and every pull request) runs three sequential jobs:

1. **`test`** — installs dependencies, runs the full `pytest` suite directly on the runner
2. **`docker-test`** — builds the Docker image, then runs the *same* test suite again **inside the container** — this catches environment-specific bugs that only show up in the containerized runtime, not just on the CI runner
3. **`push`** *(main branch only)* — builds and pushes the image to GHCR, tagged both `:latest` and with the commit SHA (`:<sha>`) for traceability

If any job fails, the ones after it don't run — broken code never reaches the registry.

## Run it locally

\`\`\`bash
git clone https://github.com/vishalnarwade04-glitch/devops-practice-api.git
cd devops-practice-api
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
python app.py
\`\`\`

## Run the published image

No source code or local build required — pull the image straight from the registry:

\`\`\`bash
docker pull ghcr.io/vishalnarwade04-glitch/devops-practice-api:latest
docker run -d -p 5000:5000 ghcr.io/vishalnarwade04-glitch/devops-practice-api:latest
curl http://localhost:5000/health
\`\`\`

## Run tests

\`\`\`bash
pytest -v
\`\`\`

Or inside a container, matching exactly what CI does:

\`\`\`bash
docker build -t devops-practice-api .
docker run --rm devops-practice-api pytest -v
\`\`\`

## What this project demonstrates

- Writing meaningful unit tests (not just happy-path — includes validation and not-found cases)
- A multi-stage CI pipeline with job dependencies (`needs:`) and conditional execution (`if:`)
- Testing inside the actual deployment artifact (the container), not just the source code
- Automated, tagged image publishing to a container registry
- Image portability — verified by pulling and running the published image independently of the build environment
