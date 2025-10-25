from crewai.tools import BaseTool
from typing import Type
from pydantic import BaseModel, Field
import os


class DirectoryListInput(BaseModel):
    """Input schema for DirectoryListTool."""
    folder: str = Field(..., description="The folder path to list files from (e.g., 'output', './output')")
    pattern: str = Field(default="*.html", description="File pattern to match (e.g., '*.html', '*.js', '*')")


class DirectoryListTool(BaseTool):
    name: str = "Directory List Tool"
    description: str = (
        "Lists all files in a directory matching a pattern. "
        "Use this to scan folders for HTML files or other file types. "
        "Provide the folder path and optionally a file pattern (defaults to '*.html')."
    )
    args_schema: Type[BaseModel] = DirectoryListInput

    def _run(self, folder: str, pattern: str = "*.html") -> str:
        """
        List all files in a directory matching the pattern.
        """
        try:
            # Normalize the folder path
            folder_path = os.path.normpath(folder)

            # Check if folder exists
            if not os.path.exists(folder_path):
                return f"Error: Folder not found at {folder_path}"

            if not os.path.isdir(folder_path):
                return f"Error: {folder_path} is not a directory"

            # List all files in the directory
            all_files = os.listdir(folder_path)

            # Filter by pattern
            import fnmatch
            if pattern == "*":
                matching_files = all_files
            else:
                matching_files = [f for f in all_files if fnmatch.fnmatch(f, pattern)]

            if not matching_files:
                return f"No files matching pattern '{pattern}' found in {folder_path}"

            # Format the output
            file_list = "\n".join([f"- {f}" for f in sorted(matching_files)])
            return f"Files found in {folder_path} (pattern: {pattern}):\n{file_list}"

        except Exception as e:
            return f"Error listing directory {folder}: {str(e)}"
