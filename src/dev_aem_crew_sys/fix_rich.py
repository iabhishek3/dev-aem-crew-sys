"""
Monkey patch for Rich library to fix FileProxy recursion bug.
This must be imported before any CrewAI imports.
"""
import io
from typing import IO, Any


def patched_getattr(self, name: str) -> Any:
    """
    Fixed __getattr__ that prevents infinite recursion.
    Properly handles both private FileProxy attributes and delegated file attributes.
    """
    # First, try to get the attribute from the FileProxy instance itself
    # Use object.__getattribute__ to avoid triggering __getattr__ recursion
    try:
        return object.__getattribute__(self, name)
    except AttributeError:
        pass

    # If not found in FileProxy, delegate to the wrapped file object
    try:
        file = object.__getattribute__(self, '_FileProxy__file')
        return getattr(file, name)
    except AttributeError:
        raise AttributeError(f"'{type(self).__name__}' object has no attribute '{name}'")


def apply_patch():
    """Apply the monkey patch to Rich's FileProxy class."""
    try:
        from rich.file_proxy import FileProxy

        # Replace the problematic __getattr__ method
        FileProxy.__getattr__ = patched_getattr

        print("✓ Applied Rich FileProxy patch to fix recursion bug")
        return True
    except ImportError:
        print("⚠ Warning: Could not import Rich FileProxy. Patch not applied.")
        return False
    except Exception as e:
        print(f"⚠ Warning: Failed to apply Rich patch: {e}")
        return False
