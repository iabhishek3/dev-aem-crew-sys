from crewai.tools import BaseTool
from typing import Type
from pydantic import BaseModel, Field
import os


class AEMFileWriterInput(BaseModel):
    """Input schema for AEMFileWriterTool."""
    file_path: str = Field(..., description="The full relative path from AEM project root (e.g., 'ui.apps/src/main/content/jcr_root/apps/myapp/components/navbar/navbar.html')")
    content: str = Field(..., description="The complete file content to write")
    aem_project_path: str = Field(..., description="The absolute path to the AEM project root")


class AEMFileWriterTool(BaseTool):
    name: str = "AEM File Writer"
    description: str = (
        "Writes files to the AEM project structure. "
        "Use this to create AEM component files including HTL templates, Java classes, "
        "dialogs, and clientlib files. Provide the relative path from AEM project root, "
        "the content, and the AEM project base path. Creates parent directories if needed."
    )
    args_schema: Type[BaseModel] = AEMFileWriterInput

    def _run(self, file_path: str, content: str, aem_project_path: str) -> str:
        """
        Write content to a file in the AEM project structure.
        Creates all parent directories if they don't exist.
        """
        try:
            # Create the full absolute path
            full_path = os.path.join(aem_project_path, file_path)

            # Get the directory path
            directory = os.path.dirname(full_path)

            # Create all parent directories if they don't exist
            if not os.path.exists(directory):
                os.makedirs(directory)
                print(f"Created directories: {directory}")

            # Write the content to the file
            with open(full_path, 'w', encoding='utf-8') as f:
                f.write(content)

            # Get just the filename for display
            filename = os.path.basename(full_path)

            return f"Successfully created file: {file_path}\nFull path: {full_path}"

        except Exception as e:
            return f"Error writing file {file_path}: {str(e)}"
