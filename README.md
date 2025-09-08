# Seorchestra

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![PRs Welcome](https://img.shields.io/badge/PRs-welcome-brightgreen.svg)](https://github.com/AJakif/SEOrchestra/pulls)

**Seorchestra** is an open-source, Docker-powered multi-agent system designed to automate and orchestrate comprehensive SEO audits. Think of it as a conductor, seamlessly coordinating a symphony of specialized AI agents to deliver clear, actionable, and client-ready SEO reports.

## 🚀 Vision

To become the most powerful and flexible open-source platform for automated SEO analysis, built on a modular agent architecture that the community can extend and improve.

## ⚡️ Current Capabilities

The initial orchestra consists of two core agents working in concert:

*   **Audit Agent:** A technical SEO crawler that scans websites for critical issues (broken links, missing meta tags, title tags, H1 headings, image alt text, etc.).
*   **Reporting Agent:** An insight generator that transforms raw audit data into reports (currently with placeholder implementation).
*   **Orchestrator:** Coordinates the workflow between agents and provides a unified API endpoint.

**Current SEO checks implemented:**
- Title tag presence and length validation
- Meta description presence and length validation
- H1 heading presence and count validation
- Image alt text validation
- Internal link crawling and analysis

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

## Repository Structure

```
seorchestra/
├── .github/
│   └── workflows/          # GitHub Actions CI/CD pipelines (e.g.,testing, Docker builds)
├── orchestrator/           # The main controller service
│   ├── src/
│   │   └── app.py         # FastAPI application code
│   ├── requirements.txt
│   ├── Dockerfile
│   └── __init__.py
├── audit_agent/            # Agent 1: Technical SEO Auditor
│   ├── src/
│   │   └── app.py
│   ├── requirements.txt
│   ├── Dockerfile
│   └── __init__.py
├── reporting_agent/        # Agent 2: Reporting & Insights Agent
│   ├── src/
│   │   └── app.py
│   ├── requirements.txt
│   ├── Dockerfile
│   └── __init__.py
├── shared/                 # For common code, schemas, and models
│   ├── src/
│   │   └── schemas.py     # Pydantic models for inter-agent communication
│   └── __init__.py
├── docker-compose.yml      # Defines and runs the entire multi-container application
├── .env.example           # Template for environment variables
├── .gitignore
├── LICENSE                # Important for open source (MIT)
└── README.md
```
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

## 🗺 Roadmap

- [ ] Integrate Google PageSpeed Insights API
- [ ] Add a Keyword Research Agent
- [ ] Build a simple web front-end
- [ ] Add database persistence for historical reports
- [ ] Create a library of pre-built report templates

---

This README will be updated as the project progresses.


