from crewai.tools import BaseTool
from typing import Type
from pydantic import BaseModel, Field


class UserInteractionInput(BaseModel):
    """Input schema for UserInteractionTool."""
    question: str = Field(..., description="The question to ask the user")
    options: list = Field(default=None, description="Optional list of choices for the user to select from")


class UserInteractionTool(BaseTool):
    name: str = "User Interaction Tool"
    description: str = (
        "Asks the user questions and gets their input. "
        "Can be used for component selection, configuration choices, "
        "and other interactive decisions."
    )
    args_schema: Type[BaseModel] = UserInteractionInput

    def _run(self, question: str, options: list = None) -> str:
        """
        Ask the user a question and get their response.
        If options are provided, user must select from the list.
        """
        if options:
            # Auto-select the first option to allow non-interactive runs
            options_str = ", ".join([f"'{opt}'" for opt in options])
            selected = options[0]
            print(f"[Tool: User Interaction] {question} → Auto-selected: '{selected}' from [{options_str}]")
            return selected
        # No options provided: return empty string (non-interactive)
        return ""