# Chase Reserve Points Deal Tracker — Implementation Plan

## Overview
A CLI tool that tracks potential flight and hotel deals redeemable with Chase Sapphire Reserve points. It only flags when good deals arrive (high cents-per-point value).

## Project Structure
```
chase-points-tracker/
├── pyproject.toml              # Standalone project config (Poetry)
├── README.md
├── .env.example                # Template for API keys / config
├── src/
│   ├── __init__.py
│   ├── cli.py                  # CLI entry point (Click-based)
│   ├── models.py               # Pydantic models (Deal, Alert, PointsBalance, etc.)
│   ├── config.py               # Config loading (.env, thresholds)
│   ├── deal_tracker.py         # Core logic: evaluate deals, flag good ones
│   ├── alerts.py               # Alert delivery (console output for now, extensible)
│   ├── store.py                # Local JSON-file persistence for deals & alerts
│   └── scrapers/
│       ├── __init__.py
│       ├── base.py             # Abstract scraper interface
│       ├── google_flights.py   # Stub: Google Flights scraper
│       ├── hotel_scraper.py    # Stub: Hotel deal scraper
│       └── points_guy.py       # Stub: The Points Guy deal scraper
└── tests/
    ├── __init__.py
    ├── test_deal_tracker.py
    └── test_models.py
```

## Key Components

### 1. Models (`models.py`)
- **Deal**: type (flight/hotel), origin, destination, dates, cash_price, points_price, source, scraped_at
- **DealAlert**: wraps a Deal + computed cents_per_point value + alert reason
- **PointsConfig**: user's points balance, minimum cpp threshold to flag (default: 1.5 cpp for Reserve)

### 2. Deal Tracker (`deal_tracker.py`)
- Takes a list of scraped deals
- Computes cents-per-point (cpp) = cash_price / points_price × 100
- Chase Reserve baseline: 1.5 cpp via portal. Only flag deals **above** a configurable threshold (e.g., 2.0+ cpp = great deal)
- Returns list of `DealAlert` objects for deals worth flagging

### 3. Scrapers (`scrapers/`)
- `BaseScraper` abstract class with `scrape() -> list[Deal]` interface
- Three stub implementations (Google Flights, Hotels, The Points Guy) that return sample/mock data
- Designed so real implementations can be dropped in later

### 4. Store (`store.py`)
- JSON file-based persistence (`~/.chase-points-tracker/deals.json`)
- Tracks seen deals to avoid duplicate alerts
- Stores alert history

### 5. CLI (`cli.py`) — Click-based commands
- `chase-points scan` — Run all scrapers, evaluate deals, print alerts
- `chase-points config` — Set/view points balance and cpp threshold
- `chase-points history` — View past alerts
- `chase-points deals` — List all tracked deals

### 6. Alerts (`alerts.py`)
- Console-based rich output (using `rich` library) showing flagged deals
- Formatted table with deal details, cpp value, and savings vs. portal redemption

## Dependencies
- Python ^3.11
- click (CLI framework)
- pydantic (data models)
- rich (terminal output)
- httpx (for future scraper HTTP calls)
- python-dotenv (config)
- pytest (testing)

## What Gets Built Now
- Full project scaffold with all files
- Working CLI with all commands
- Mock data from scraper stubs so the tool is demo-able immediately
- Deal evaluation logic with configurable thresholds
- JSON persistence
- Tests for deal tracker logic and models
