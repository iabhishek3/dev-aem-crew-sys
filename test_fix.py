#!/usr/bin/env python
"""Quick test to verify the Rich FileProxy fix works"""

# Apply the patch
from src.dev_aem_crew_sys.fix_rich import apply_patch
apply_patch()

# Test that it works
from rich.console import Console
import sys

try:
    console = Console()

    # This should work without recursion error
    print("Testing Rich Console output...")
    console.print("[green]✓ Rich is working correctly![/green]")

    print("\n✓ Test passed! The fix works correctly.")
    sys.exit(0)

except RecursionError as e:
    print(f"\n✗ Test failed with RecursionError: {e}")
    sys.exit(1)
except Exception as e:
    print(f"\n✗ Test failed with error: {e}")
    sys.exit(1)
