# Ethiopian Medical Data Pipeline

## 📌 Overview
The **Ethiopian Medical Data Pipeline** is a modular, end-to-end data engineering platform for collecting, processing, and analyzing health-related content from Telegram channels in Ethiopia. It supports real-time public health surveillance, research data collection, and automated analytics workflows.

Built with modern open-source tools—**FastAPI**, **dbt**, **Dagster**, **Docker**, and more—the pipeline offers scalable and reproducible workflows for medical data projects.

---

## 🎯 Key Goals
- ✅ **Public Health Surveillance:** Monitor disease trends and misinformation.
- ✅ **Automation:** Eliminate manual data collection.
- ✅ **Data Quality:** Ensure structured, clean, and queryable datasets.
- ✅ **Research Support:** Enable downstream analysis and ML training.
- ✅ **Extensibility:** Easily plug into other channels or domains.

---

## 🧠 Use Cases
- Detect and analyze COVID-19 trends from public groups.
- Extract pharmaceutical mentions from chat messages.
- Power analytics dashboards for NGOs and health agencies.
- Train ML models on annotated medical messages or images.

---

## ⚙️ Tech Stack
| Component     | Tool/Library                |
|--------------|-----------------------------|
| Language      | Python 3.10+                |
| API           | FastAPI                     |
| Pipeline      | Dagster                     |
| ETL           | Pandas, SQLAlchemy          |
| Database      | PostgreSQL                  |
| Transformation| dbt                         |
| Scraping      | Telethon                    |
| CV/Image Proc | OpenCV                      |
| Containerization | Docker & Docker Compose  |

---

## 🧭 Architecture

```mermaid
graph TD
    A[Telegram Channels] -->|Scrape| B[Scraper (Telethon)]
    B -->|Raw Data| C[data/raw/]
    C -->|Preprocess| D[Pandas & OpenCV]
    D -->|Load| E[PostgreSQL]
    E -->|Transform| F[dbt]
    F -->|Serve| G[FastAPI]
    D -->|Orchestrate| H[Dagster]
```

---

## 📁 Project Structure
```
ethiopian_medical_data_pipeline/
├── data/                    # Raw and processed data
│   └── raw/                 # Stored as YYYY-MM-DD/channelname.json
├── dbt_project/             # dbt models and tests
├── docker/                  # Docker config files
├── pipelines/               # Data pipeline scripts
│   ├── data_collection/     # Scraping & image downloading
│   ├── data_processing/     # Database loading
│   └── orchestration/       # Dagster definitions
├── src/
│   ├── api/                 # FastAPI app
│   └── common/              # Shared configs, logging
├── tests/                   # Unit & integration tests
├── .env.example             # Template for environment variables
├── .gitignore               # Ensures secrets are not committed
├── requirements.txt         # Python dependencies
└── README.md                # Project documentation
```

---

## 🚀 Getting Started

### ✅ Prerequisites
- Python 3.10+
- Docker & Docker Compose
- Git
- Telegram API credentials ([my.telegram.org](https://my.telegram.org))

### 🔐 1. Setup Environment Variables

Copy the example:
```bash
cp .env.example .env
```

Edit `.env`:
```
POSTGRES_USER=postgres
POSTGRES_PASSWORD=supersecretpassword
POSTGRES_DB=ethiopian_medical_data
POSTGRES_HOST=db
```

> ✅ **Note:** The `.env` file is excluded from version control via `.gitignore` to protect secrets.

---

### 🛠 2. Build and Start with Docker

```bash
cd docker
docker compose up --build
```

**Service URLs:**
- FastAPI: [http://localhost:8000](http://localhost:8000)
- Dagster UI: [http://localhost:3000](http://localhost:3000)
- PostgreSQL: `localhost:5432`

---

## 📡 Data Pipeline Usage

### 🔍 Scrape Telegram Messages
```bash
python pipelines/data_collection/telegram_scraper.py
```

### 🖼 Download Images from Messages
```bash
python pipelines/data_collection/image_downloader.py
```

### 🗃 Load JSON and Image Data to PostgreSQL
```bash
python pipelines/data_processing/database_loader.py
```

### 🧮 Run dbt Transformations
```bash
cd dbt_project
dbt run
cd ..
```

### 🧭 Orchestrate with Dagster
```bash
dagster dev -f pipelines/orchestration/dagster_pipeline.py
```

---

## 🌐 API Usage

### Start the FastAPI Server
```bash
uvicorn src.api.main:app --reload
```

### Explore API Documentation
- Swagger UI: [http://localhost:8000/docs](http://localhost:8000/docs)

---

## 🔄 Example Workflow Summary
1. Scraper → JSON in `data/raw/telegram_messages/`
2. Image downloader → files in `data/raw/telegram_images/`
3. Loader → data into PostgreSQL
4. dbt → analytics tables
5. FastAPI → RESTful API layer
6. Dagster → automation & scheduling

---

## 🧪 Testing

```bash
pip install pytest pytest-cov
pytest --cov=src tests/
```

✅ Ensure new functions have test coverage.
✅ Tests run on push via GitHub Actions CI.

---

## 💡 Troubleshooting

| Issue                          | Solution |
|-------------------------------|----------|
| PostgreSQL container fails     | Check `.env` is present and configured |
| ModuleNotFoundError            | Run scripts from root, verify `__init__.py` |
| OpenCV DLL errors (Windows)    | Install [VC++ Redistributable](https://aka.ms/vs/17/release/vc_redist.x64.exe) |
| dbt error: source not found    | Check `sources.yml` in `dbt_project/models/` |
| Docker fails                   | Rebuild image and check `requirements.txt` |

---

## 📚 Contributing

### 🛠 Fork & Clone
```bash
git clone https://github.com/wondifraw/ethiopian_medical_data_pipeline.git
cd ethiopian_medical_data_pipeline

```

---

## 🙏 Acknowledgements
- [FastAPI](https://fastapi.tiangolo.com/)
- [Dagster](https://dagster.io/)
- [dbt](https://www.getdbt.com/)
- [Telethon](https://github.com/LonamiWebs/Telethon)
- [OpenCV](https://opencv.org/)

---

## 📜 License
MIT License. 