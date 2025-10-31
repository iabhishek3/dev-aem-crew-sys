from crewai.tools import BaseTool
from typing import Type
from pydantic import BaseModel, Field
import base64
import os
from anthropic import Anthropic


class VisionToolInput(BaseModel):
    """Input schema for VisionTool."""
    image_path: str = Field(..., description="Path to the image file to analyze.")


class VisionTool(BaseTool):
    name: str = "Component Image Analyzer"
    description: str = (
        "Analyzes SINGLE UI component images (not full page designs). Identifies component type, "
        "extracts exact text content, colors, typography, spacing, layout structure, and all child "
        "elements. Works with component images like: navbar, button, card, hero section, footer, "
        "form, sidebar, modal, etc. Provide the path to a component image file (PNG, JPG, etc.) "
        "and this tool will perform a complete component analysis using Claude's vision capabilities."
    )
    args_schema: Type[BaseModel] = VisionToolInput

    def _run(self, image_path: str) -> str:
        """
        Load the image and analyze it directly using Claude's vision API.
        Returns a comprehensive design analysis.
        """
        try:
            # Check if file exists
            if not os.path.exists(image_path):
                return f"Error: Image file not found at path: {image_path}. Please ensure the design.png file exists in the project root directory."

            # Read and encode the image
            with open(image_path, "rb") as image_file:
                image_data = image_file.read()
                base64_image = base64.b64encode(image_data).decode('utf-8')

            # Get file extension to determine image type
            file_extension = os.path.splitext(image_path)[1].lower()
            mime_types = {
                '.png': 'image/png',
                '.jpg': 'image/jpeg',
                '.jpeg': 'image/jpeg',
                '.gif': 'image/gif',
                '.webp': 'image/webp'
            }
            mime_type = mime_types.get(file_extension, 'image/png')

            # Initialize Anthropic client
            api_key = os.getenv("ANTHROPIC_API_KEY")
            if not api_key:
                return "Error: ANTHROPIC_API_KEY not found in environment variables."

            client = Anthropic(api_key=api_key)

            # Get model from environment or use latest Sonnet 4.5 (September 2025)
            model_name = os.getenv("MODEL", "claude-sonnet-4-5-20250929")
            # Remove anthropic/ prefix if present (API expects just the model name)
            if model_name.startswith("anthropic/"):
                model_name = model_name.replace("anthropic/", "")

            # Create the analysis prompt for SINGLE COMPONENT (OPTIMIZED for speed)
            analysis_prompt = """Analyze this UI component image with precision. Extract:

1. COMPONENT: Type, dimensions, complexity
2. COLORS: All hex codes (background, text, buttons, borders, shadows)
3. TYPOGRAPHY: For each text element - exact content, size, weight, color, transform
4. LAYOUT: Display type (flex/grid/block), justify-content, align-items, positioning
5. CHILD ELEMENTS: List all (type, position, content, styles, hover states)
6. SPACING: Padding, margin, gap, border-radius
7. INTERACTIONS: Hover effects, dropdowns (▼), carousels, animations

Extract ONLY what you see. Be pixel-accurate with colors, text, and measurements."""

            # Make API call with vision using Claude Sonnet 4.5
            message = client.messages.create(
                model=model_name,
                max_tokens=8192,  # Increased to ensure complete output
                messages=[
                    {
                        "role": "user",
                        "content": [
                            {
                                "type": "image",
                                "source": {
                                    "type": "base64",
                                    "media_type": mime_type,
                                    "data": base64_image,
                                },
                            },
                            {
                                "type": "text",
                                "text": analysis_prompt
                            }
                        ],
                    }
                ],
            )

            # Extract the analysis from the response
            analysis = message.content[0].text

            return f"DESIGN ANALYSIS COMPLETE:\n\n{analysis}"

        except Exception as e:
            return f"Error analyzing image: {str(e)}"
