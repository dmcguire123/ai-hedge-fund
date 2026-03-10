# Chase Reserve Points Deal Tracker

A CLI tool that monitors flight and hotel deals and flags when you can get outsized value from your Chase Sapphire Reserve points.

## How It Works

Chase Sapphire Reserve points are worth 1.5 cents per point (cpp) when redeemed through the Chase travel portal. This tool scrapes deal sources and flags opportunities where your points are worth **more** than the portal baseline — meaning transfer partners, special promotions, or underpriced award flights.

## Installation

```bash
cd chase-points-tracker
pip install -e .
```

## Usage

```bash
# Scan for deals and show alerts
chase-points scan

# Configure your points balance and alert threshold
chase-points config --balance 150000 --threshold 2.0

# View past alerts
chase-points history

# List all tracked deals
chase-points deals
```

## Configuration

Copy `.env.example` to `.env` and configure:

```bash
cp .env.example .env
```

Settings:
- `POINTS_BALANCE`: Your current Chase UR points balance
- `CPP_THRESHOLD`: Minimum cents-per-point to trigger an alert (default: 2.0)

## Adding Scrapers

The scraper interface is in `src/scrapers/base.py`. Implement the `BaseScraper` abstract class to add new deal sources. Current stubs:

- Google Flights (transfer partner award flights)
- Hotel deals (Hyatt, IHG, Marriott transfers)
- The Points Guy (curated deal posts)
