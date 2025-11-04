"""
Fix for Rich library FileProxy issues with CrewAI.
This must be imported before any CrewAI imports.

The issue: Rich's FileProxy has bugs when accessing internal attributes (__file, __buffer).
The solution: Completely replace Rich's console file handling to avoid FileProxy altogether.
"""
import sys
import os


def apply_patch():
    """
    Disable Rich's FileProxy by preventing Rich from wrapping stdout/stderr.
    This is safer than trying to patch FileProxy's broken __getattr__.
    """
    try:
        # Set environment variable to disable Rich features that use FileProxy
        os.environ['TERM'] = 'dumb'  # Makes Rich use simpler output without FileProxy

        # Import Rich and disable its file wrapping
        from rich import console

        # Store original Console.__init__
        original_console_init = console.Console.__init__

        def patched_console_init(self, *args, **kwargs):
            """
            Patched Console.__init__ that prevents Rich from wrapping stdout/stderr with FileProxy.
            """
            # Force Rich to use plain file objects, not FileProxy
            kwargs['force_terminal'] = False
            kwargs['force_interactive'] = False
            kwargs['legacy_windows'] = False

            # Call original init
            original_console_init(self, *args, **kwargs)

            # Replace any FileProxy instances with the raw file objects
            try:
                if hasattr(self, '_file'):
                    file_obj = self._file
                    if hasattr(file_obj, 'rich_proxied_file'):
                        # FileProxy detected - replace with raw file
                        self._file = file_obj.rich_proxied_file
                    elif hasattr(file_obj, '_FileProxy__file'):
                        # Old-style FileProxy - replace with raw file
                        self._file = object.__getattribute__(file_obj, '_FileProxy__file')
            except Exception:
                # If we can't unwrap, just use stdout directly
                self._file = sys.stdout

        # Apply the patch
        console.Console.__init__ = patched_console_init

        print("✓ Applied Rich Console patch to prevent FileProxy issues")
        return True

    except ImportError:
        print("⚠ Warning: Could not import Rich. Patch not applied.")
        return False
    except Exception as e:
        print(f"⚠ Warning: Failed to apply Rich patch: {e}")
        return False
