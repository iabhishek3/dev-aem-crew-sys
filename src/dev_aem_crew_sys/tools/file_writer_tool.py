from crewai.tools import BaseTool
from typing import Type
from pydantic import BaseModel, Field
import os


class FileWriterInput(BaseModel):
    """Input schema for FileWriterTool."""
    filename: str = Field(..., description="The filename for the file (e.g., 'navbar.html')")
    content: str = Field(..., description="The complete HTML content to write to the file")
    folder: str = Field(default="output-ui_architect", description="The folder to save the file in (default: 'output-ui_architect')")


class FileWriterTool(BaseTool):
    name: str = "File Writer"
    description: str = (
        "Writes HTML content to a file in the specified folder. "
        "Use this to create individual component HTML files. "
        "Provide the filename (e.g., 'navbar.html'), the complete HTML content, "
        "and optionally the folder name (defaults to 'output-ui_architect')."
    )
    args_schema: Type[BaseModel] = FileWriterInput

    def _run(self, filename: str, content: str, folder: str = "output-ui_architect") -> str:
        """
        Write content to a file in the specified folder.
        Creates the folder if it doesn't exist.
        """
        try:
            # Create the folder if it doesn't exist
            if not os.path.exists(folder):
                os.makedirs(folder)

            # Create the full file path
            filepath = os.path.join(folder, filename)

            # Write the content to the file
            with open(filepath, 'w', encoding='utf-8') as f:
                f.write(content)

            return f"Successfully created file: {filepath}\nFile can be opened in a browser to view the component."

        except Exception as e:
            return f"Error writing file {filename}: {str(e)}"
