# Theater Scraper

A Python application that scrapes performance schedules from various Moscow theaters and provides the data through an API.

## Overview

Theater Scraper is designed to collect repertoire information from different theater websites, store it in a database, and make it available through a REST API. The system currently supports the following theaters:

- Fomenko Workshop Theater (Мастерская Петра Фоменко)
- Russian Academic Youth Theater (Российский Академический Театр)
- Studio of Theatrical Art (Студия Театрального Искусства)

## Features

- Asynchronous web scraping using httpx
- Database storage with SQLModel
- RESTful API using FastAPI
- Support for multiple theaters with different website structures
- Performance information including titles, dates, times, and venues

## Requirements

- Python 3.13+
- PostgreSQL database

## Installation

1. Clone the repository:

   ```bash
   git clone https://github.com/yourusername/theater-scraper.git
   cd theater-scraper
   ```

2. Create a virtual environment and install dependencies:

   ```bash
   python -m venv .venv
   source .venv/bin/activate  # On Windows: .venv\Scripts\activate
   pip install -e .
   ```

3. For development, install additional dependencies:

   ```bash
   pip install -e ".[dev,tests]"
   ```

## Configuration

1. Set up environment variables for database connection:

   ```bash
   DB_HOST=localhost
   DB_PORT=5432
   DB_USER=postgres
   DB_PASSWORD=yourpassword
   DB_NAME=theater_db
   ```

## Usage

### Running the API Server

```bash
fastapi dev src/main.py
```

The API will be available at `http://localhost:8000`.

### API Endpoints

- `GET /api/performances` - Get all performances
- `GET /api/theaters` - Get all theaters
- `GET /api/stages` - Get all stages
- `GET /api/performances/{theater_name}` - Get performances for a specific theater

## Project Structure

```text
theater-scraper/
├── src/
│   ├── api/                 # API endpoints
│   ├── scrapers/
│   │   ├── fomenki.py       # Fomenki theater scraper
│   │   ├── manager.py       # Scraper execution manager
│   │   ├── scraper.py       # Base scraper class
│   │   └── ...              # Other theater scrapers
│   ├── services/
│   │   ├── stage_service.py # Stage-related operations
│   │   ├── theater_service.py # Theater-related operations
│   │   └── ...              # Other services
│   ├── config.py            # Application configuration
│   ├── db.py                # Database connection
│   ├── db_init.py           # Database initialization
│   ├── main.py              # FastAPI application
│   └── models.py            # Database models and API response models
├── tests/                   # Test files
├── LICENSE                  # MIT License file
├── README.md                # This file
└── pyproject.toml           # Project metadata and dependencies
```

## Development

### Running Tests

```bash
pytest
```

## License

[MIT](LICENSE)
