import os
from pathlib import Path

from dotenv import load_dotenv

from src.models import PointsConfig

# Load .env from the project root
_project_root = Path(__file__).parent.parent
load_dotenv(_project_root / ".env")

DATA_DIR = Path.home() / ".chase-points-tracker"


def get_config() -> PointsConfig:
    """Load points config from environment or defaults."""
    balance = int(os.getenv("POINTS_BALANCE", "100000"))
    threshold = float(os.getenv("CPP_THRESHOLD", "2.0"))
    return PointsConfig(points_balance=balance, cpp_threshold=threshold)
