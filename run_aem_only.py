#!/usr/bin/env python
"""
Test script to run ONLY the AEM Alchemist agent.

This skips the Visual Strategist (design analysis) and runs only the AEM component generation.
Perfect for testing the second agent when you already have design_analysis.json.

Usage:
    python run_aem_only.py

Prerequisites:
    - output-visual_strategist/design_analysis.json must exist
    - Run the full crew at least once first, or create the design_analysis.json manually
"""

if __name__ == "__main__":
    import sys
    import os

    # Add src to path
    sys.path.insert(0, 'src')

    # Import and run
    from dev_aem_crew_sys.main import run_aem_only

    print("=" * 80)
    print("🧪 TEST MODE: Running AEM Alchemist Only")
    print("=" * 80)
    print()

    run_aem_only()
