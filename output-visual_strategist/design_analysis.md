DESIGN ANALYSIS COMPLETE:

# UI Component Analysis

## 1. COMPONENT
- **Type**: Two-panel informational section/card layout
- **Dimensions**: Full-width container with two rows
- **Complexity**: Medium - contains images, headings, body text, and structured layout

## 2. COLORS
- **Background**: #FFFFFF (white)
- **Primary text (headings)**: #1A1A1A or similar dark gray
- **Secondary text (tagline)**: #E91E63 or similar pink/red
- **Body text**: #666666 or similar medium gray
- **Divider lines**: #E0E0E0 or similar light gray

## 3. TYPOGRAPHY

### Top Section:
- **"Our Tagline"**: 
  - Size: ~12-14px
  - Weight: 400 (Regular)
  - Color: #E91E63 (pink/red)
  - Transform: None

- **"Making Our Healthcare Happen"**:
  - Size: ~24-28px
  - Weight: 600 (Semi-bold)
  - Color: #1A1A1A (dark gray/black)
  - Transform: None

### Bottom Section:
- **"Our Purpose"**:
  - Size: ~12-14px
  - Weight: 400 (Regular)
  - Color: #E91E63 (pink/red)
  - Transform: None

- **"A Singapore where everyone is assured of value-based healthcare."**:
  - Size: ~22-26px
  - Weight: 600 (Semi-bold)
  - Color: #1A1A1A (dark gray/black)
  - Transform: None

- **Lorem ipsum body text**:
  - Size: ~14-16px
  - Weight: 400 (Regular)
  - Color: #666666 (medium gray)
  - Transform: None

## 4. LAYOUT
- **Display**: Flex/Grid container, stacked vertically
- **Top row**: 
  - Display: Flex
  - Justify-content: space-between
  - Align-items: center
  - Image on left, text on right

- **Bottom row**:
  - Display: Flex
  - Justify-content: space-between
  - Align-items: center
  - Text on left, image on right

## 5. CHILD ELEMENTS

### Row 1 (Top):
1. **Image** (left)
   - Type: Photograph
   - Content: Healthcare worker with elderly patient outdoors
   - Dimensions: ~225px × ~127px
   - Border-radius: 4-6px

2. **Text block** (right)
   - Contains tagline and heading
   - Aligned left within its container

### Row 2 (Bottom):
1. **Text block** (left)
   - Contains "Our Purpose" label, heading, and body text
   - Max-width: ~50-60% of container

2. **Image** (right)
   - Type: Photograph (same as top)
   - Content: Same healthcare scene
   - Dimensions: ~225px × ~127px
   - Border-radius: 4-6px

### Divider:
- Horizontal line between sections
- Color: #E0E0E0
- Height: 1px

## 6. SPACING
- **Container padding**: 40-60px horizontal, 40-50px vertical
- **Gap between image and text**: 60-80px
- **Margin between rows**: 60-80px
- **Text block internal spacing**:
  - Tagline to heading: 8-12px
  - Heading to body: 16-20px
- **Border-radius on images**: 4-6px
- **Divider margin**: 30-40px top and bottom

## 7. INTERACTIONS
- **No visible hover states** in static image
- **No dropdown indicators (▼)** present
- **No carousel indicators** visible
- **Potential interactions**:
  - Images may have subtle hover effects (not visible in static)
  - Text may be clickable/linked (not indicated in design)
  - No animation indicators present