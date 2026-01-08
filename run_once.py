#!/usr/bin/env python3
"""
Script to run the daily pipeline once and exit.
Used by Railway cron jobs.
"""
import sys
from main import main

if __name__ == "__main__":
    result = main(hours=24, top_n=10)
    sys.exit(0 if result["success"] else 1)
