# AEM Component Validation Checklist

Use this checklist to ensure every AEM component meets quality and production standards before deployment.

## Pre-Development Checklist

- [ ] **Context7 Query Complete**: Queried Context7 for relevant AEM patterns and syntax
- [ ] **Component Purpose Clear**: Understand what the component does and who will use it
- [ ] **Design Analysis Complete**: Have all visual specifications and requirements
- [ ] **Reusability Considered**: Check if similar component exists that could be extended

## HTL Template Validation

### Security & XSS Protection
- [ ] **XSS Contexts Applied**: All expressions use appropriate @ context
  - `@ context='uri'` for href and src attributes
  - `@ context='scriptString'` for JavaScript strings
  - `@ context='styleString'` for CSS values
  - `@ context='html'` only when absolutely necessary and source is trusted
- [ ] **No context='unsafe'**: Never use unsafe context
- [ ] **Event Handlers Safe**: No HTL expressions in onclick, onload, etc.
- [ ] **User Input Escaped**: All user-provided content properly escaped

### HTL Syntax & Best Practices
- [ ] **data-sly-use Declared**: Sling Model loaded with data-sly-use
- [ ] **Null Checks Present**: All properties checked before use (data-sly-test or || operator)
- [ ] **Clean Markup**: Use data-sly-unwrap or <sly> for conditionals
- [ ] **Proper Iteration**: Use data-sly-list with meaningful variable names
- [ ] **No Inline Styles**: Dynamic styles use CSS classes, not style="" attributes
- [ ] **Templates Defined Correctly**: data-sly-template with proper parameters
- [ ] **Templates Called**: All templates actually used with data-sly-call

### Accessibility (WCAG 2.1)
- [ ] **Alt Attributes**: All <img> tags have meaningful alt text
- [ ] **Semantic HTML**: Use proper elements (nav, article, section, header, footer)
- [ ] **ARIA Labels**: Interactive elements have appropriate ARIA attributes
- [ ] **Keyboard Navigation**: Component usable without mouse
- [ ] **Color Contrast**: Text meets WCAG AA standards (4.5:1 ratio minimum)
- [ ] **Focus Indicators**: Visible focus states for interactive elements
- [ ] **Heading Hierarchy**: Proper h1-h6 structure

### Responsive Design
- [ ] **Mobile Tested**: Component works on mobile screens (320px+)
- [ ] **Tablet Tested**: Component works on tablet screens (768px+)
- [ ] **Desktop Tested**: Component works on desktop screens (1024px+)
- [ ] **No Horizontal Scroll**: Content fits viewport on all sizes
- [ ] **Touch-Friendly**: Tap targets at least 44x44px on mobile

## Sling Model Validation

### Structure & Annotations
- [ ] **@Model Annotation**: Class properly annotated with adaptables and defaultInjectionStrategy
- [ ] **DefaultInjectionStrategy**: Set to OPTIONAL to prevent errors
- [ ] **Proper Injections**: Use correct annotations (@ValueMapValue, @ChildResource, etc.)
- [ ] **@PostConstruct Method**: Initialization logic in @PostConstruct if needed
- [ ] **Null Safety**: All getters return non-null values (empty strings, empty lists, etc.)
- [ ] **No Business Logic**: Complex logic delegated to OSGi services
- [ ] **Serializable**: Model can be serialized if used in SPA/headless

### Code Quality
- [ ] **Package Naming**: Follows convention (com.company.core.models)
- [ ] **Class Naming**: Clear, descriptive name ending with "Model"
- [ ] **Getters Only**: No setters (models are read-only)
- [ ] **JavaDoc Present**: Class and public methods documented
- [ ] **No Hardcoded Values**: Use OSGi configs or resource properties

## Dialog Configuration

### Field Validation
- [ ] **All Content Editable**: Every visible element configurable in dialog
- [ ] **Field Labels Clear**: Descriptive fieldLabel for each field
- [ ] **Required Fields Marked**: Use required="{Boolean}true" where appropriate
- [ ] **Field Names Correct**: name="./propertyName" format
- [ ] **Resource Types Valid**: sling:resourceType points to valid Granite UI components
- [ ] **Default Values**: Provide sensible defaults where applicable

### Dialog Structure
- [ ] **Organized Tabs**: Use tabs if more than 5-6 fields
- [ ] **Logical Grouping**: Related fields grouped together
- [ ] **Multifield Config**: Composite multifields for complex items
- [ ] **Select Options**: Dropdown values clear and useful
- [ ] **Path Fields**: Use pathbrowser or fileupload for assets/pages
- [ ] **RTE Config**: Rich text editor configured with appropriate plugins

### Author Experience
- [ ] **Help Text**: Complex fields have description or tooltips
- [ ] **Validation Messages**: Clear error messages for invalid input
- [ ] **Preview Works**: Component appearance updates in edit mode
- [ ] **No Console Errors**: No JavaScript errors in author mode

## Component Metadata

- [ ] **_.content.xml Present**: Component metadata file exists
- [ ] **Component Title**: Clear, descriptive jcr:title
- [ ] **Component Description**: Helpful jcr:description
- [ ] **Component Group**: Logical componentGroup (e.g., "MyProject - Content")
- [ ] **Component Icon**: Appropriate cq:icon
- [ ] **Resource Super Type**: Set if extending another component

## Client Libraries

- [ ] **Clientlib Configured**: .content.xml in clientlibs folder
- [ ] **Categories Set**: Unique clientlib category
- [ ] **CSS Organized**: Component styles in dedicated CSS file
- [ ] **CSS BEM Naming**: Classes follow BEM (cmp-componentname__element)
- [ ] **JavaScript Modular**: JS code in separate file if needed
- [ ] **Dependencies Listed**: embed or dependencies configured correctly
- [ ] **Minified for Prod**: Production clientlibs minified

## Testing Checklist

### Author Mode Testing
- [ ] **Component Adds**: Can be added to page from sidebar
- [ ] **Dialog Opens**: Dialog opens without errors
- [ ] **Fields Save**: All dialog fields save correctly
- [ ] **Component Renders**: Displays correctly after save
- [ ] **Copy/Paste Works**: Component can be copied and pasted
- [ ] **Delete Works**: Component can be deleted
- [ ] **Undo/Redo Works**: Edit operations can be undone/redone

### Publish Mode Testing
- [ ] **Renders Correctly**: Component displays as expected
- [ ] **No Author Markup**: No edit/config dialogs visible
- [ ] **Styles Applied**: CSS loaded correctly
- [ ] **Scripts Execute**: JavaScript works as expected
- [ ] **Links Work**: All links resolve correctly
- [ ] **Images Load**: All images display properly

### Cross-Browser Testing
- [ ] **Chrome Tested**: Works in latest Chrome
- [ ] **Firefox Tested**: Works in latest Firefox
- [ ] **Safari Tested**: Works in latest Safari
- [ ] **Edge Tested**: Works in latest Edge

### Performance
- [ ] **Fast Render**: Component renders in <500ms
- [ ] **Images Optimized**: Images compressed and sized appropriately
- [ ] **No Memory Leaks**: JavaScript properly cleaned up
- [ ] **Lazy Loading**: Images/content lazy-loaded if below fold

## Build & Deployment

- [ ] **Maven Build Succeeds**: mvn clean install completes without errors
- [ ] **No Checkstyle Errors**: Code passes style checks
- [ ] **Unit Tests Pass**: JUnit tests pass (if present)
- [ ] **Package Deploys**: Component package installs on AEM
- [ ] **Component Available**: Appears in component browser
- [ ] **No Conflicts**: Doesn't break existing components

## Documentation

- [ ] **README.md Created**: Component documentation exists
- [ ] **Usage Examples**: Shows how to use component
- [ ] **Dialog Fields Documented**: All fields explained
- [ ] **Dependencies Listed**: Any required configs or services noted
- [ ] **Screenshots Included**: Visual examples of component

## Security & Compliance

- [ ] **XSS Prevention**: HTL Validator shows no critical issues
- [ ] **CSRF Protection**: Forms use granite:csrf token
- [ ] **No Sensitive Data**: No passwords or keys in code
- [ ] **Permissions Checked**: ACLs configured if needed
- [ ] **GDPR Compliant**: No PII without consent

## Final Checklist

- [ ] **HTL Validator Passed**: No critical issues or warnings
- [ ] **Code Review Complete**: Another developer reviewed code
- [ ] **QA Tested**: QA team verified functionality
- [ ] **Stakeholder Approved**: Component meets requirements
- [ ] **Production Ready**: All above checks complete

---

## Component Status

**Component Name**: _______________________

**Developer**: _______________________

**Date**: _______________________

**Status**: ☐ Draft | ☐ In Review | ☐ Approved | ☐ Production

**Notes**:
