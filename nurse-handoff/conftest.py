"""Pytest configuration for importing the local package."""

from pathlib import Path
import sys


PACKAGE_ROOT = Path(__file__).resolve().parent
sys.path.insert(0, str(PACKAGE_ROOT))
