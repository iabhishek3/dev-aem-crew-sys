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
    name: str = "Design Image Analyzer"
    description: str = (
        "Analyzes design mockup images to identify visual components, layouts, colors, "
        "typography, spacing, and hierarchy. Provide the path to a design image file "
        "(PNG, JPG, etc.) and this tool will perform a complete visual analysis using "
        "Claude's vision capabilities and return the full analysis."
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

            # Create the analysis prompt
            analysis_prompt = """Analyze this web design mockup in EXTREME DETAIL as a professional UI/UX designer.
This analysis will be used to create pixel-perfect HTML/CSS components, so accuracy is CRITICAL.

1. OVERALL LAYOUT ANALYSIS:
   - Page structure and grid system
   - Content sections and their arrangement (top to bottom)
   - Responsive design considerations
   - Whitespace and spacing patterns (exact pixel values if possible)

2. COLOR SCHEME (CRITICAL - Extract EXACT colors):
   - Primary colors with hex codes (estimate as accurately as possible)
   - Secondary and accent colors with hex codes
   - SPECIFIC usage: Which color is used WHERE
   - Navbar background color (exact hex)
   - Button background colors (exact hex for each button type)
   - Text colors (exact hex for different text elements)
   - Background colors for sections
   - Be VERY specific about where each color appears

3. TYPOGRAPHY (EXACT SPECIFICATIONS):
   - Font families used (sans-serif, serif, etc.)
   - Heading hierarchy (H1, H2, H3, etc.) with EXACT font sizes
   - Font weights for each element (400, 500, 600, 700)
   - Text styles (uppercase, capitalize, normal)
   - Line heights
   - Letter spacing if noticeable

4. VISUAL COMPONENTS (List ALL with EXACT DETAILS):

   NAVBAR (ULTRA-CRITICAL - MAXIMUM DETAIL):
   This is THE MOST IMPORTANT component. Provide EXTREME detail:

   - Background color (hex) and any gradients
   - Exact height in pixels (measure carefully: 60px? 70px? 80px? 90px?)
   - Border or shadow: Describe exactly

   LOGO SECTION:
   - Position: LEFT side (measure distance from left edge)
   - Logo text/image: Write EXACT text visible
   - Logo size: width and height if visible
   - Logo color(s)

   NAVIGATION LINKS SECTION (CRITICAL):
   - List EVERY navigation link visible, left to right
   - EXACT text for each: "Who We Are", "What We Do", etc. (case-sensitive)
   - Positioning of nav group: Is it CENTER of navbar? Or LEFT next to logo?
   - If CENTER: Measure - is it truly centered or offset?
   - Gap between links: Estimate in pixels (20px? 30px? 40px?)
   - Font size: Estimate (14px? 16px? 18px?)
   - Font weight: Light/Regular/Medium/Bold?
   - Which links have dropdown indicators: Mark each with ▼
   - Text color and hover color

   RIGHT SECTION:
   - CTA button text: EXACT text
   - Button position: RIGHT edge (measure distance)
   - Button colors: background and text
   - Button size: padding and dimensions
   - Any icons (search, profile, cart, etc.): Describe each

   SPACING MEASUREMENTS (CRITICAL):
   - Logo-to-nav distance: Small/Medium/Large (estimate: 40px? 60px? 80px?)
   - Nav-to-button distance: Estimate
   - Left/right page margins: Estimate (24px? 40px? 60px?)
   - Gap between nav items: Consistent? (estimate each)

   BUTTONS:
   - List EACH button type separately
   - Exact text on each button
   - Background colors (hex)
   - Text colors (hex)
   - Padding values
   - Border radius
   - Font size and weight

   HERO SECTION:
   - Background: color or image (describe if image)
   - Text content (exact text visible, word-for-word)
   - Text colors and sizes
   - Text alignment (left/center/right)
   - Button text and styles
   - Layout and positioning
   - CRITICAL: Is this a carousel/slider? (Look for dots, arrows, multiple slides)
   - If carousel: How many slides/dots visible?
   - Navigation arrows: Position and style

   FOOTER:
   - Background color
   - Layout structure (columns)
   - Link text and colors
   - Section headings

   OTHER COMPONENTS:
   - Cards, forms, icons, etc. with exact styling details

   INTERACTIVE ELEMENTS (CRITICAL):
   - Carousels/Sliders: Identify any sliding content, dots, arrows
   - Dropdowns: Which menu items have dropdown indicators (▼)
   - Accordions: Expandable sections
   - Tabs: Tab navigation
   - Modals or popups
   - Hover states or transitions

5. LAYOUT AND POSITIONING (CRITICAL):
   - Logo position: LEFT, CENTER, or RIGHT
   - Navigation links position: LEFT, CENTER, or RIGHT
   - Buttons position: LEFT, CENTER, or RIGHT
   - Content alignment in sections
   - Flexbox/Grid layout details

6. ACTUAL CONTENT:
   - Extract EXACT text content visible in the design
   - Brand names, taglines, button labels
   - Navigation link labels
   - Heading text
   - Language used (English, Spanish, etc.)

7. SPACING AND MEASUREMENTS:
   - Padding values for components (estimate in pixels: 8px, 12px, 16px, 24px, etc.)
   - Margin values between sections
   - Gap between navigation items
   - Component heights and widths
   - Border radius values

Be EXTREMELY specific and accurate. This analysis will be used directly to create components that must look 90%+ identical to the design."""

            # Make API call with vision
            message = client.messages.create(
                model="claude-3-5-sonnet-20241022",
                max_tokens=4096,
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
