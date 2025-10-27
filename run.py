#!/usr/bin/env python3
"""Run script for the weather app."""

import sys
from pathlib import Path

# Add the project root to Python path
project_root = Path(__file__).parent
sys.path.insert(0, str(project_root))

# Now import and run the app
from backend.app import main

if __name__ == "__main__":
    main()
