# Seorchestra

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![PRs Welcome](https://img.shields.io/badge/PRs-welcome-brightgreen.svg)](https://github.com/AJakif/SEOrchestra/pulls)

Seorchestra is an open‑source, Docker‑powered **multi‑agent SEO audit platform**.

Give it a URL and it will crawl, analyze, and generate a **clear, prioritized SEO report** that a developer or SEO specialist can act on immediately.

---

## What Seorchestra does

- **Automated technical SEO audits**
  - Crawls your site, following internal links within sensible limits.
  - Detects issues with status codes, redirects, indexability, canonicalization, meta tags, headings, and links.
- **Insightful reporting**
  - Groups findings by theme (technical, on‑page, internal linking, etc.).
  - Prioritizes issues by severity and potential impact.
  - Produces client‑ready reports (e.g. Markdown/HTML) that are easy to share.
- **Modular agent architecture**
  - Each responsibility (crawling, reporting, future keyword research, performance analysis, etc.) lives in its own **agent**.
  - A central **orchestrator** coordinates work across agents.

Seorchestra is designed to be both **developer‑friendly** (API‑first, containerized) and **SEO‑friendly** (concrete checks, actionable wording).

---

## Who this is for

- **SEO specialists & agencies**
  - Run repeatable audits on client sites.
  - Export reports and integrate them into your existing workflow.
- **Developers & platform teams**
  - Integrate automated SEO checks into CI/CD or monitoring.
  - Expose audit results in internal dashboards.
- **Tool builders**
  - Use the orchestrator API as a backend for your own SEO products.

---

## High‑level architecture

Seorchestra is built as a set of independent, containerized **FastAPI** services:

- **Orchestrator** – main controller and public API.
- **Audit Agent** – crawls a site and runs technical/on‑page checks.
- **Reporting Agent** – turns raw audit data into a human‑readable report.
- **Shared** – common Pydantic schemas used by all services.

Data flow for a single audit:

1. A client (web app or API user) sends a request with a URL to the **Orchestrator**.
2. The Orchestrator calls the **Audit Agent**, which crawls the site and returns a structured `AuditResult`.
3. The Orchestrator passes that `AuditResult` to the **Reporting Agent**, which returns a `ReportResponse` (e.g. Markdown).
4. The Orchestrator returns the job status and report to the client and (in future phases) persists everything.

For a deeper architecture description, see `docs/agent/ARCHITECTURE.md`.

---

## Repository layout

```text
seorchestra/
├── orchestrator/           # Main controller service (public API & job orchestration)
│   ├── src/
│   │   └── app.py          # FastAPI application code (planned / WIP)
│   ├── requirements.txt
│   ├── Dockerfile
│   └── __init__.py
├── audit_agent/            # Agent 1: technical SEO auditor
│   ├── src/
│   │   └── app.py          # FastAPI app for crawling & checks (planned / WIP)
│   ├── requirements.txt
│   ├── Dockerfile
│   └── __init__.py
├── reporting_agent/        # Agent 2: reporting & insights
│   ├── src/
│   │   └── app.py          # FastAPI app for report generation (planned / WIP)
│   ├── requirements.txt
│   ├── Dockerfile
│   └── __init__.py
├── shared/                 # Shared models and contracts
│   ├── src/
│   │   └── schemas.py      # Pydantic models for inter‑agent communication
│   └── __init__.py
├── docs/
│   └── agent/              # Context for coding agents (project, architecture, tasks, standards)
│       ├── README.md
│       ├── PROJECT-CONTEXT.md
│       ├── ARCHITECTURE.md
│       ├── TASKS-AND-ROADMAP.md
│       └── CODING-STANDARDS.md
├── docker-compose.yml      # Runs the multi‑container stack
├── .env.example            # Template for environment variables
├── .gitignore
├── LICENSE                 # MIT license
└── README.md
```

If you are an AI coding agent working in this repo, start with `docs/agent/README.md`.

---

## Tech stack

- **Language**: Python
- **Frameworks**: FastAPI (for all services)
- **Orchestration**: Docker and Docker Compose
- **Communication**: RESTful HTTP/JSON using shared Pydantic models
- **Planned infrastructure**:
  - PostgreSQL for users, sites, audit jobs, and reports
  - Redis for caching and rate limiting
  - A separate web frontend (e.g. Next.js) consuming the orchestrator API

For an engineering‑focused overview and roadmap, see `docs/agent/TASKS-AND-ROADMAP.md` and `docs/agent/CODING-STANDARDS.md`.

---

## Quick start (local, with Docker)

### Prerequisites

- Docker
- Docker Compose

### 1. Clone the repository

```bash
git clone https://github.com/AJakif/SEOrchestra.git
cd SEOrchestra
```

### 2. Configure environment

Copy the example environment file and adjust as needed:

```bash
cp .env.example .env
```

For the current MVP, only basic settings are needed. As the project evolves, `.env` will include:

- Service ports
- Database and Redis URLs (when persistence is added)
- Auth and rate‑limiting parameters

### 3. Build and run the stack

This will build images for the orchestrator and agents and start them in the background:

```bash
docker-compose up --build -d
```

To see logs from all services:

```bash
docker-compose logs -f
```

### 4. Call the API

Once the stack is running, the Orchestrator will be available on `http://localhost:8000` (default).

In the current design, you’ll be able to start an audit with a POST request (exact paths may evolve as implementation progresses):

```bash
curl -X POST "http://localhost:8000/api/v1/audits" \
  -H "Content-Type: application/json" \
  -d '{"url": "https://example.com"}'
```

Then, you’ll query the job status and report with something like:

```bash
curl "http://localhost:8000/api/v1/audits/{job_id}"
```

Refer to the OpenAPI docs (FastAPI’s `/docs` endpoint) once the services are fully wired up.

---

## For developers

- Start with the **agent docs**:
  - `docs/agent/PROJECT-CONTEXT.md` – high‑level product context and goals.
  - `docs/agent/ARCHITECTURE.md` – service responsibilities and data flow.
  - `docs/agent/TASKS-AND-ROADMAP.md` – phased tasks and current priorities.
  - `docs/agent/CODING-STANDARDS.md` – conventions for structure, style, security, and testing.
- Focus on:
  - **Backend orchestration and agents** in Python/FastAPI.
  - Best practices: auth, rate limiting, safe crawling, caching, observability, and tests.

If you are contributing a new feature, please align it with the phases and guidelines in the docs above.

---

## For SEO specialists and clients

At a high level, Seorchestra aims to give you:

- A **repeatable SEO audit** you can run any time on any site.
- A **prioritized list of issues**, not just raw data.
- Clear **recommendations** that developers can implement.

A typical workflow will look like:

1. Enter your website URL (and, in the future, options like depth, device type, or language).
2. Wait for the audit to complete.
3. Review the report, which includes:
   - Overall SEO health summary.
   - Lists of critical, major, and minor issues.
   - A checklist of recommended fixes.
4. Share the report with your development team or clients.

As the platform matures, you’ll also be able to:

- Track historical audits and improvements over time.
- Add more specialized analyses (keywords, PageSpeed, Core Web Vitals, etc.).

---

## Contributing

We are building this in the open and welcome contributions from:

- Developers (Python, FastAPI, frontend)
- SEO specialists and agencies
- Technical writers and documentation contributors

To contribute:

1. Fork the repository.
2. Create a feature branch: `git checkout -b feature/your-feature-name`.
3. Make your changes following `docs/agent/CODING-STANDARDS.md`.
4. Add or update tests where appropriate.
5. Open a Pull Request with a clear description of what you changed and why.

Please note that a dedicated `CONTRIBUTING.md` will be added as the project evolves.

---

## License

This project is licensed under the MIT License – see the [`LICENSE`](LICENSE) file for details.

---

## Roadmap (high level)

Planned directions include:

- Integrate Google PageSpeed Insights / Core Web Vitals.
- Add a Keyword Research Agent.
- Build a user‑facing web frontend for the SaaS experience.
- Add database persistence for historical reports.
- Create a library of report templates and export options (Markdown, HTML, PDF).

For a more detailed and up‑to‑date task list, see `docs/agent/TASKS-AND-ROADMAP.md`.

# Seorchestra

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![PRs Welcome](https://img.shields.io/badge/PRs-welcome-brightgreen.svg)](https://github.com/AJakif/SEOrchestra/pulls)

**Seorchestra** is an open-source, Docker-powered multi-agent system designed to automate and orchestrate comprehensive SEO audits. Think of it as a conductor, seamlessly coordinating a symphony of specialized AI agents to deliver clear, actionable, and client-ready SEO reports.

## 🚀 Vision

To become the most powerful and flexible open-source platform for automated SEO analysis, built on a modular agent architecture that the community can extend and improve.

## ⚡️ Current Capabilities (MVP)

The initial orchestra consists of two core agents working in concert:

*   **Audit Agent:** A technical SEO crawler that scans websites for critical issues (broken links, missing meta tags, etc.).
*   **Reporting Agent:** An insight generator that transforms raw audit data into a prioritized, human-readable report.

---

## 🛠 Tech Stack

*   **Language:** Python
*   **Frameworks:** FastAPI (for agent APIs)
*   **Orchestration:** Docker, Docker Compose
*   **Communication:** RESTful HTTP/JSON

---

## 🏗 Architecture

Seorchestra is built as a collection of independent, containerized microservices (agents). This makes it incredibly scalable and easy to contribute to.

+----------------+      +----------------+      +-------------------+
|                |      |                |      |                   |
|   Orchestrator |----->|  Audit Agent   |----->|   Reporting Agent |
|    (Controller)|      | (Dockerized)   |      |   (Dockerized)    |
|                |      |                |      |                   |
+----------------+      +----------------+      +-------------------+
        ^                                                     |
        |                                                     v
        |                                              +---------------+
        |                                              |               |
        +----------------------------------------------+   Client/User |
                                                       |               |
                                                       +---------------+

---

## 🚦 Getting Started

### Prerequisites

- Docker
- Docker Compose

### Installation

1.  **Clone the repository**
    ```bash
    git clone https://github.com/AJakif/SEOrchestra.git
    cd seorchestra
    ```

2.  **Copy the environment template**
    ```bash
    cp .env.example .env
    ```
    (Edit `.env` to add any required settings in the future)

3.  **Build and run the entire stack**
    This command builds the images and starts all three services (orchestrator, audit_agent, reporting_agent) in detached mode.
    ```bash
    docker-compose up --build -d
    ```

4.  **Watch the logs (Optional)**
    To see the log output from all running services:
    ```bash
    docker-compose logs -f
    ```

5.  **Use the API**
    The Orchestrator service will be running on `http://localhost:8000`.
    Send a POST request to the `/audit` endpoint with a JSON body:
    ```bash
    curl -X POST "http://localhost:8000/audit" -H "Content-Type: application/json" -d '{"url": "https://example.com"}'
    ```

6.  **Stopping the services**
    To stop and remove the running containers:
    ```bash
    docker-compose down
    ```

---

## 🤝 How to Contribute

We are building this in the open and welcome all contributions! Whether you're a developer, SEO specialist, or technical writer, there's a place for you here.

1.  Fork the Project
2.  Create your Feature Branch (`git checkout -b feature/AmazingFeature`)
3.  Commit your Changes (`git commit -m 'Add some AmazingFeature'`)
4.  Push to the Branch (`git push origin feature/AmazingFeature`)
5.  Open a Pull Request

Please read `CONTRIBUTING.md` (to be created) for details on our code of conduct and the process for submitting pull requests.

---

## 📜 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

---

This README will be updated as the project progresses.


