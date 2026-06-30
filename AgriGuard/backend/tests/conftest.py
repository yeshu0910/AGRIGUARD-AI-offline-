"""Pytest configuration for AgriGuard backend tests."""

import os
import sys

# Add backend directory to sys.path for source module imports
sys.path.insert(0, os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
