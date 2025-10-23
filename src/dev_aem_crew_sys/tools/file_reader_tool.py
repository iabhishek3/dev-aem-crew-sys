from crewai.tools import BaseTool
from typing import Type
from pydantic import BaseModel, Field
import os


class FileReaderInput(BaseModel):
    """Input schema for FileReaderTool."""
    filename: str = Field(..., description="The filename to read (e.g., 'navbar.html')")
    folder: str = Field(default="output", description="The folder where the file is located (default: 'output')")


class FileReaderTool(BaseTool):
    name: str = "File Reader"
    description: str = (
        "Reads the contents of a file from the specified folder. "
        "Use this to read HTML component files or any other files. "
        "Provide the filename (e.g., 'navbar.html') and optionally "
        "the folder name (defaults to 'output')."
    )
    args_schema: Type[BaseModel] = FileReaderInput

    def _run(self, filename: str, folder: str = "output") -> str:
        """
        Read the contents of a file from the specified folder.
        """
        try:
            # Create the full file path
            filepath = os.path.join(folder, filename)

            # Check if file exists
            if not os.path.exists(filepath):
                return f"Error: File not found at {filepath}"

            # Read the file contents
            with open(filepath, 'r', encoding='utf-8') as f:
                content = f.read()

            return content

        except Exception as e:
            return f"Error reading file {filename}: {str(e)}"
