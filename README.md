# Ethiopian Medical Data Pipeline

## Overview
The **Ethiopian Medical Data Pipeline** is a comprehensive, end-to-end data engineering platform designed to automate the collection, processing, analysis, and serving of medical-related data from public Telegram channels. The system is built to support public health monitoring, research, and analytics in the Ethiopian context, but is extensible to other domains and regions.

This project leverages modern open-source technologies—**FastAPI**, **Dagster**, **dbt**, **Docker**, and more—to provide a robust, scalable, and reproducible data workflow. It is suitable for data engineers, researchers, and organizations seeking to build reliable data pipelines for social media and medical data.

---

## Motivation
- **Public Health Surveillance:** Track and analyze health-related discussions and trends in Ethiopian Telegram channels.
- **Research Enablement:** Provide clean, structured, and queryable data for academic and clinical research.
- **Automation:** Eliminate manual data collection and processing, ensuring up-to-date datasets.
- **Extensibility:** Easily adapt the pipeline to new data sources, models, or analytics needs.

---

## Use Cases
- Monitoring the spread of medical misinformation or disease outbreaks.
- Collecting and analyzing pharmaceutical or clinical discussions.
- Building dashboards for health authorities or NGOs.
- Training machine learning models on real-world medical conversations and images.

---

## Technology Stack
- **Python 3.10+** — Core programming language
- **Docker & Docker Compose** — Containerization and orchestration
- **PostgreSQL** — Relational database for structured data
- **FastAPI** — High-performance API for serving data
- **Dagster** — Data pipeline orchestration and scheduling
- **dbt** — Data transformation and analytics modeling
- **Telethon** — Telegram scraping
- **OpenCV** — Image processing and object detection
- **Pandas, SQLAlchemy** — Data wrangling and database interaction

---

## Architecture Overview

```mermaid
graph TD
    A[Telegram Channels] -->|Scrape| B[Data Collection (Telethon)]
    B -->|Raw Messages/Images| C[Data Lake (data/raw)]
    C -->|Process| D[Data Processing (Pandas, OpenCV)]
    D -->|Load| E[PostgreSQL Database]
    E -->|Transform| F[dbt Models]
    F -->|Serve| G[FastAPI]
    D -->|Orchestrate| H[Dagster]
```

---

## Project Structure
```
ethiopian_medical_data_pipeline/
├── data/                  # Raw and processed data storage
├── dbt_project/           # dbt models and configuration
├── docker/                # Docker and docker-compose files
├── pipelines/
│   ├── data_collection/   # Telegram scraping and image downloading
│   ├── data_processing/   # Database loading and object detection
│   └── orchestration/     # Dagster pipeline definitions
├── src/
│   ├── api/               # FastAPI application
│   └── common/            # Shared config and logging
├── requirements.txt       # Python dependencies
└── README.md              # Project documentation
```

---

## Getting Started

### Prerequisites
- Python 3.10+
- Docker & Docker Compose
- Git
- Telegram API credentials (get from [my.telegram.org](https://my.telegram.org/))

### 1. Clone the Repository
```bash
git clone https://github.com/YOUR-USERNAME/ethiopian_medical_data_pipeline.git
cd ethiopian_medical_data_pipeline
```

### 2. Set Up Environment Variables
Create a `.env` file in the project root:
```
POSTGRES_USER=postgres
POSTGRES_PASSWORD=supersecretpassword
POSTGRES_DB=ethiopian_medical_data
POSTGRES_HOST=db
```
Add your Telegram API credentials to `src/common/config.py` or as environment variables as needed.

### 3. Build and Start Services with Docker
```bash
cd docker
docker compose up --build
```
- FastAPI: [http://localhost:8000](http://localhost:8000)
- Dagster UI: [http://localhost:3000](http://localhost:3000)
- PostgreSQL: localhost:5432

### 4. Run Data Pipelines

#### Scrape Telegram Messages
Collects messages from configured Telegram channels and stores them as JSON files.
```bash
python pipelines/data_collection/telegram_scraper.py
```

#### Download Images
Downloads images from Telegram messages and stores them in the data lake.
```bash
python pipelines/data_collection/image_downloader.py
```

#### Load Data to Database
Loads the scraped messages and image metadata into the PostgreSQL database.
```bash
python pipelines/data_processing/database_loader.py
```

#### Run dbt Transformations
Transforms raw data into analytics-ready tables and marts.
```bash
cd dbt_project
dbt run
cd ..
```

#### Orchestrate with Dagster
Manages and schedules the entire pipeline.
```bash
dagster dev -f pipelines/orchestration/dagster_pipeline.py
```

---

## API Usage
- Start the API:
  ```bash
  uvicorn src.api.main:app --reload
  ```
- Visit [http://localhost:8000/docs](http://localhost:8000/docs) for interactive API documentation and testing endpoints.

---

## Example Data Flow
1. **Telegram Scraper** collects messages and images → stores in `data/raw/telegram_messages/` and `data/raw/telegram_images/`.
2. **Image Downloader** fetches and saves images from messages.
3. **Database Loader** ingests JSON and image metadata into PostgreSQL.
4. **dbt** transforms raw tables into analytics-ready models.
5. **FastAPI** serves the data via REST endpoints.
6. **Dagster** orchestrates and schedules the above steps.

---

## Troubleshooting
- **Postgres container fails to start:** Ensure `.env` file is present and all variables are set.
- **ModuleNotFoundError:** Run commands from the project root and ensure all `__init__.py` files exist in package folders.
- **OpenCV DLL errors:** Install the [Microsoft Visual C++ Redistributable](https://aka.ms/vs/17/release/vc_redist.x64.exe) and ensure you are using 64-bit Python.
- **dbt source not found:** Ensure `sources.yml` is defined in `dbt_project/models/`.
- **Docker build fails:** Check for missing dependencies in `requirements.txt` and ensure all files are present.

---

## Development & Contribution
1. Fork the repository and create your feature branch:
   ```bash
   git checkout -b feature/YourFeature
   ```
2. Commit your changes and push:
   ```bash
   git add .
   git commit -m "Add YourFeature"
   git push origin feature/YourFeature
   ```
3. Open a Pull Request on GitHub.

---

## License
This project is licensed under the MIT License.

---

## Acknowledgements
- [Dagster](https://dagster.io/)
- [dbt](https://www.getdbt.com/)
- [FastAPI](https://fastapi.tiangolo.com/)
- [Telethon](https://github.com/LonamiWebs/Telethon)
- [OpenCV](https://opencv.org/) 