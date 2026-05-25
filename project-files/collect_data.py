#!/usr/bin/env python
"""
Standalone script to collect game market data
Run this script to scrape and store trending games from all platforms
"""

import os
import sys
import django
import subprocess
from pathlib import Path

# Setup Django
project_root = Path(__file__).resolve().parent
backend_dir = project_root / 'backend'
sys.path.insert(0, str(backend_dir))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'greatest_game_agent.settings')
django.setup()

from django.core.management import call_command


def main():
    print("\n" + "="*60)
    print("  GREATEST GAME AGENT - DATA COLLECTION")
    print("="*60 + "\n")
    
    print("Starting data collection from game marketplaces...")
    print("-" * 60)
    
    try:
        # Run the collection management command
        call_command('collect_trends', '--all')
        
        print("\n" + "-" * 60)
        print("✓ Data collection completed successfully!")
        print("\nData has been collected from:")
        print("  • Steam")
        print("  • Itch.io")
        print("  • Epic Games Store")
        print("\nYou can now view the results in your dashboard at:")
        print("  http://localhost:3000")
        print("\n" + "="*60 + "\n")
        
    except Exception as e:
        print(f"\n✗ Error during data collection: {str(e)}")
        print("\nTroubleshooting tips:")
        print("  1. Ensure backend is properly configured")
        print("  2. Check that database is accessible")
        print("  3. Verify Bright Data API key in .env")
        sys.exit(1)


if __name__ == '__main__':
    main()
