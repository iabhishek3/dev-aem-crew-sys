# MOHH Project Standards

Official standards and conventions for MOHH Websites AEM project.

---

## Project Configuration

### AEM Project Details
- **Project Name:** MOHH Websites
- **AEM App ID:** `mohhwebsites`
- **Component Group:** "MOHH Websites - Content"
- **Base Path:** `/Users/abhishekkumar/Temus-space/aem-projects/mohh-websites-revamp`

### Package Structure
```
com.mohhwebsites.core.models     // Sling Models
com.mohhwebsites.core.services   // Services
com.mohhwebsites.core.utils      // Utilities
```

### Project Structure
```
mohh-websites-revamp/
├── core/
│   └── src/main/java/com/mohhwebsites/core/
│       └── models/              # Sling Models here
├── ui.apps/
│   └── src/main/content/jcr_root/apps/mohhwebsites/
│       └── components/          # Component definitions & HTL
├── ui.frontend/
│   └── src/main/webpack/
│       ├── components/          # SCSS & JS files
│       └── resources/           # Images, fonts
└── ui.content/
    └── src/main/content/jcr_root/content/
```

---

## Color Palette

### Primary Colors
```scss
$mohh-primary-blue: #5EA6DB;        // Primary CTA, active states
$mohh-primary-blue-light: #7ba7d6;  // Subtitles, secondary text
$mohh-primary-blue-dark: #6AACDB;   // Hover states
```

### Secondary Colors
```scss
$mohh-secondary-orange: #E85C23;    // Accents, highlights
```

### Text Colors
```scss
$mohh-text-primary: #6b6b6b;        // Main headings, body text
$mohh-text-secondary: #7ba7d6;      // Subtitles, captions
$mohh-text-light: #666666;          // Light text, metadata
$mohh-text-dark: #3C3C3C;           // Dark headings
```

### Background Colors
```scss
$mohh-background-light: #F5F5F5;    // Page background
$mohh-background-beige: #D4C4B0;    // Alternate sections
$mohh-background-white: #FFFFFF;    // Cards, modals
```

### UI Colors
```scss
$mohh-border: #ddd;                 // Borders, dividers
$mohh-border-light: rgba(0, 0, 0, 0.1);  // Subtle borders
$mohh-shadow: rgba(0, 0, 0, 0.1);   // Box shadows
```

### Usage Examples
```scss
// Buttons
.cmp-button--primary {
  background-color: $mohh-primary-blue;
  color: #FFFFFF;

  &:hover {
    background-color: $mohh-primary-blue-dark;
  }
}

// Links
.cmp-link {
  color: $mohh-primary-blue;

  &:hover {
    color: $mohh-primary-blue-dark;
  }
}

// Headings
.cmp-heading {
  color: $mohh-text-primary;
}

// Subtitles
.cmp-subtitle {
  color: $mohh-text-secondary;
}
```

---

## Typography

### Font Families
```scss
$mohh-font-primary: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Arial, sans-serif;
```

### Font Sizes
```scss
// Headings
$mohh-font-size-h1: 48px;      // Hero headings (mobile: 36px)
$mohh-font-size-h2: 36px;      // Section headings (mobile: 28px)
$mohh-font-size-h3: 24px;      // Card titles (mobile: 20px)
$mohh-font-size-h4: 20px;      // Subheadings
$mohh-font-size-h5: 18px;      // Small headings

// Body
$mohh-font-size-body: 16px;    // Body text (mobile: 14px)
$mohh-font-size-small: 14px;   // Small text, captions
$mohh-font-size-tiny: 12px;    // Metadata, legal text
```

### Font Weights
```scss
$mohh-font-weight-normal: 400;  // Body text
$mohh-font-weight-medium: 500;  // Emphasized text
$mohh-font-weight-bold: 700;    // Headings, buttons
```

### Line Heights
```scss
$mohh-line-height-tight: 1.2;   // Headings
$mohh-line-height-normal: 1.5;  // Body text
$mohh-line-height-relaxed: 1.8; // Large paragraphs
```

---

## Spacing System

### Base Unit: 4px

```scss
// Spacing scale
$space-1: 4px;      // 0.25rem
$space-2: 8px;      // 0.5rem
$space-3: 12px;     // 0.75rem
$space-4: 16px;     // 1rem
$space-5: 20px;     // 1.25rem
$space-6: 24px;     // 1.5rem
$space-8: 32px;     // 2rem
$space-10: 40px;    // 2.5rem
$space-12: 48px;    // 3rem
$space-16: 64px;    // 4rem
$space-20: 80px;    // 5rem
```

### Component Spacing
```scss
// Card padding
$card-padding-mobile: $space-4;   // 16px
$card-padding-tablet: $space-6;   // 24px
$card-padding-desktop: $space-8;  // 32px

// Section padding
$section-padding-mobile: $space-8;   // 32px
$section-padding-tablet: $space-10;  // 40px
$section-padding-desktop: $space-12; // 48px

// Element gaps
$gap-small: $space-2;   // 8px
$gap-medium: $space-4;  // 16px
$gap-large: $space-8;   // 32px
```

---

## Responsive Breakpoints

### Standard Breakpoints
```scss
$breakpoint-mobile: 480px;   // Small phones
$breakpoint-tablet: 768px;   // Tablets, large phones
$breakpoint-desktop: 1024px; // Desktops
$breakpoint-wide: 1440px;    // Wide screens
```

### Usage Pattern (Mobile-First)
```scss
.component {
  // Mobile styles (default)
  padding: $space-4;
  font-size: 14px;

  // Tablet
  @media (min-width: $breakpoint-tablet) {
    padding: $space-6;
    font-size: 15px;
  }

  // Desktop
  @media (min-width: $breakpoint-desktop) {
    padding: $space-8;
    font-size: 16px;
  }
}
```

### Visible Cards by Breakpoint
```javascript
// Carousel/Grid components
if (width < 768) {
    visibleCards = 1;  // Mobile
} else if (width < 1024) {
    visibleCards = 2;  // Tablet
} else {
    visibleCards = 3;  // Desktop
}
```

---

## Component Sizing Standards

### Card Heights
```scss
$card-height-mobile: 420px;
$card-height-tablet: 480px;
$card-height-desktop: 541px;
```

### Container Widths
```scss
$container-max-width: 1440px;
$container-padding-mobile: 16px;
$container-padding-desktop: 32px;
```

### Button Sizes
```scss
// Primary button
$button-height: 48px;
$button-padding-x: 32px;
$button-font-size: 16px;

// Secondary button
$button-height-small: 40px;
$button-padding-x-small: 24px;
$button-font-size-small: 14px;
```

### Icon Sizes
```scss
$icon-size-small: 20px;   // Inline icons
$icon-size-medium: 28px;  // Social icons (default)
$icon-size-large: 48px;   // Navigation arrows
```

---

## Animation & Transitions

### Timing Functions
```scss
$ease-standard: cubic-bezier(0.4, 0, 0.2, 1);  // Default
$ease-in: cubic-bezier(0.4, 0, 1, 1);          // Enter
$ease-out: cubic-bezier(0, 0, 0.2, 1);         // Exit
$ease-in-out: cubic-bezier(0.4, 0, 0.6, 1);    // Both
```

### Durations
```scss
$duration-fast: 150ms;    // Hover effects
$duration-normal: 300ms;  // Most transitions
$duration-slow: 500ms;    // Carousels, slides
```

### Standard Transition
```scss
.component {
  transition: transform $duration-normal $ease-standard,
              box-shadow $duration-normal $ease-standard;
}
```

### Always Include Reduced Motion
```scss
@media (prefers-reduced-motion: reduce) {
  * {
    animation-duration: 0.01ms !important;
    animation-iteration-count: 1 !important;
    transition-duration: 0.01ms !important;
  }
}
```

---

## Z-Index Scale

```scss
$z-index-dropdown: 1000;
$z-index-sticky: 1020;
$z-index-fixed: 1030;
$z-index-modal-backdrop: 1040;
$z-index-modal: 1050;
$z-index-popover: 1060;
$z-index-tooltip: 1070;
```

---

## Border Radius Standards

```scss
$border-radius-small: 4px;   // Small elements
$border-radius-medium: 8px;  // Cards, buttons
$border-radius-large: 12px;  // Large containers
$border-radius-pill: 50px;   // Pills, tags
$border-radius-circle: 50%;  // Circular elements
```

---

## Shadow Standards

```scss
// Cards, containers
$shadow-small: 0 2px 4px rgba(0, 0, 0, 0.1);
$shadow-medium: 0 4px 12px rgba(0, 0, 0, 0.1);
$shadow-large: 0 8px 24px rgba(0, 0, 0, 0.15);

// Hover states
$shadow-hover: 0 8px 24px rgba(0, 0, 0, 0.15);

// Focus states
$shadow-focus: 0 0 0 3px rgba(94, 166, 219, 0.25);
```

---

## Validation Rules

### Text Field Limits
```java
MAX_HEADER_TITLE_LENGTH = 100
MAX_HEADER_SUBTITLE_LENGTH = 100
MAX_CARD_TITLE_LENGTH = 100
MAX_CARD_DESCRIPTION_LENGTH = 200
MAX_CTA_TEXT_LENGTH = 50
```

### Collection Limits
```java
MIN_CARDS_REQUIRED = 1
MAX_CARDS_ALLOWED = 6
MAX_NAV_ITEMS = 10
MAX_SOCIAL_ICONS = 10
```

---

## Accessibility Requirements

### WCAG 2.1 AA Compliance

**Color Contrast:**
- Normal text: Minimum 4.5:1
- Large text (18pt+): Minimum 3:1
- UI components: Minimum 3:1

**Required ARIA Attributes:**
```html
<section role="region" aria-label="Description">
<article role="article" aria-labelledby="title-id">
<button aria-label="Action description">
<nav role="navigation" aria-label="Navigation name">
```

**Keyboard Navigation:**
- All interactive elements focusable
- Focus indicators visible
- Logical tab order
- Enter/Space activate buttons

**Screen Reader Support:**
- Meaningful alt text on images
- ARIA live regions for dynamic content
- Proper heading hierarchy
- Skip links for navigation

---

## Analytics Integration

### Data Layer Events
```javascript
window.dataLayer.push({
  event: 'componentInteraction',
  componentName: 'teaser-grid-card',
  componentType: 'content',
  action: 'cardClick',
  label: cardTitle,
  url: ctaUrl,
  position: cardIndex
});
```

### Tracking Attributes
```html
<a href="..."
   data-track-event="click"
   data-track-component="teaser-grid-card"
   data-track-label="card-cta">
```

---

## Browser Support

### Supported Browsers
- Chrome: Last 2 versions
- Firefox: Last 2 versions
- Safari: Last 2 versions
- Edge: Last 2 versions
- Mobile Safari: iOS 12+
- Chrome Mobile: Android 8+

### Polyfills Not Needed (AEM provides)
- ES5 features
- Flexbox
- CSS Grid
- IntersectionObserver (use with feature detection)

---

## Performance Standards

### JavaScript
- ES5 syntax only (AEM requirement)
- IIFE pattern with strict mode
- Event delegation where possible
- Debounce scroll/resize handlers (150ms)
- Lazy load images

### CSS
- Mobile-first responsive design
- Use `will-change` for animations
- Minimize repaints/reflows
- Use transform over top/left
- Lazy load non-critical CSS

### Images
- Use lazy loading: `loading="lazy"`
- Provide alt text (required)
- WebP with JPEG fallback
- Responsive images with srcset
- Optimize file sizes

---

## Naming Conventions

### Component Names
- Use kebab-case: `teaser-grid-card`
- Descriptive but concise
- Group related: `card-`, `banner-`, `nav-`

### CSS Classes
- BEM with cmp- prefix: `.cmp-teaser-grid__card`
- No camelCase in CSS
- Use semantic names

### Java Classes
- PascalCase: `TeaserGridCardModel`
- Suffix: `Model`, `Service`, `Servlet`
- Package: `com.mohhwebsites.core.models`

### JavaScript
- camelCase for variables: `visibleCards`
- PascalCase for constructors: `TeaserGridCard`
- UPPERCASE for constants: `MAX_CARDS`

---

## Git Commit Standards

### Commit Message Format
```
type(scope): subject

body

footer
```

### Types
- `feat`: New feature
- `fix`: Bug fix
- `docs`: Documentation
- `style`: Formatting, no code change
- `refactor`: Code restructuring
- `test`: Adding tests
- `chore`: Maintenance

### Example
```
feat(teaser-grid): add responsive carousel navigation

- Added prev/next arrows for desktop
- Added pagination dots
- Implemented circular infinite scroll
- Added keyboard navigation support

Resolves: #123
```

---

## Component Checklist

Before marking component complete:

**Functionality:**
- [ ] Component renders correctly
- [ ] All fields editable in dialog
- [ ] Validation works (min/max items)
- [ ] Responsive (mobile, tablet, desktop)
- [ ] JavaScript works (if applicable)

**Code Quality:**
- [ ] HTL follows BEM with cmp- prefix
- [ ] SCSS matches HTL classes exactly
- [ ] JavaScript uses ES5 only
- [ ] Sling Model has validation
- [ ] Dialog XML is complete

**Accessibility:**
- [ ] ARIA attributes present
- [ ] Alt text on images
- [ ] Keyboard navigable
- [ ] Color contrast meets WCAG AA
- [ ] Reduced motion support

**Performance:**
- [ ] Images lazy loaded
- [ ] No render-blocking resources
- [ ] Debounced scroll/resize handlers
- [ ] Optimized animations

**Testing:**
- [ ] Works in all supported browsers
- [ ] Works on mobile devices
- [ ] Works in AEM author mode
- [ ] Analytics tracking works
- [ ] No console errors

---

## Component Template

Use the MOHH Teaser Grid Card as reference template for:
- File structure
- Naming conventions
- Code patterns
- Best practices

Location: `/apps/mohhwebsites/components/teasergridcard/`
