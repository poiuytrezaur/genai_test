#!/usr/bin/env python3
"""Run script for the weather app."""

import sys
from pathlib import Path

# Add the project root to Python path
project_root = Path(__file__).parent
sys.path.insert(0, str(project_root))

from backend.app import main  # noqa: E402

if __name__ == "__main__":
    main()
