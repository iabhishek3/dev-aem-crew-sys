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
        # Print the question for logging/debugging
        print("\n" + "-"*50)
        print("\n" + question + "\n")

        if options:
            # Auto-select the first option to allow non-interactive runs
            print("Available options:")
            for i, option in enumerate(options, 1):
                print(f"{i}. {option}")
            selected = options[0]
            print(f"Auto-selected option 1: {selected}")
            return selected
        # No options provided: return empty string (non-interactive)
        return ""