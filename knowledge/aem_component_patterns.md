# AEM Component Best Practices - MOHH Project

## BEM Naming Convention (from Teaser Grid Card)

### Standard Pattern
- **Block**: `.cmp-componentname` (always use "cmp-" prefix)
- **Element**: `.cmp-componentname__element`
- **Modifier**: `.cmp-componentname__element--modifier`

### Real Example from MOHH Teaser Grid Card:
```css
.cmp-teaser-grid                          /* Block */
.cmp-teaser-grid__header                  /* Element */
.cmp-teaser-grid__card                    /* Element */
.cmp-teaser-grid__card-title              /* Nested element */
.cmp-teaser-grid__dot--active             /* Modifier */
.cmp-teaser-grid__arrow--prev             /* Modifier */
```

### Rules:
1. ✅ Always use "cmp-" prefix (Adobe standard)
2. ✅ Use double underscore (__) for elements
3. ✅ Use double dash (--) for modifiers
4. ✅ Keep names descriptive but concise
5. ✅ HTL classes MUST match SCSS exactly

---

## HTL Template Patterns

### 1. Model Binding (Always First Line)
```html
<sly data-sly-use.model="com.mohhwebsites.core.models.ComponentNameModel"/>
```

### 2. Main Container Structure
```html
<section class="cmp-component-name"
         data-sly-test="${model.valid}"
         data-cmp-is="component-name"
         role="region"
         aria-label="Component description">
```

**Required Attributes:**
- `data-sly-test="${model.valid}"` - Only render if model validates
- `data-cmp-is="component-name"` - JavaScript hook identifier
- `role` and `aria-label` - Accessibility

### 3. Conditional Rendering with data-sly-test
```html
<!-- Optional header -->
<header data-sly-test="${model.headerTitle}">
    ${model.headerTitle}
</header>

<!-- Show controls only if needed -->
<div class="controls" data-sly-test="${model.cardsCount > 3}">
    <!-- Navigation arrows -->
</div>
```

### 4. Dynamic Lists with data-sly-list
```html
<!-- ❌ WRONG: Hardcoded -->
<article>Card 1</article>
<article>Card 2</article>
<article>Card 3</article>

<!-- ✅ CORRECT: Dynamic -->
<sly data-sly-list.card="${model.cards}">
    <article class="cmp-teaser-grid__card">
        <img src="${card.image @ context='uri'}"
             alt="${card.imageAlt @ context='attribute'}"/>
        <h3>${card.title}</h3>
        <p>${card.description}</p>
    </article>
</sly>
```

### 5. Context Hints (Security)
```html
${model.text}                                    <!-- Default: text -->
${model.url @ context='uri'}                     <!-- URLs -->
${model.html @ context='html'}                   <!-- Safe HTML -->
${model.svg @ context='unsafe'}                  <!-- SVG/trusted HTML -->
${model.color @ context='styleString'}           <!-- CSS values -->
${model.alt @ context='attribute'}               <!-- HTML attributes -->
```

### 6. Inline Styles (When Needed)
```html
<!-- Use styleString context for safety -->
<h2 style="color: ${model.headerTitleColor @ context='styleString'};">
    ${model.headerTitle}
</h2>
```

### 7. Empty State Placeholder (Author Mode)
```html
<sly data-sly-test="${!model.valid && wcmmode.edit}">
    <div class="cmp-teaser-grid--empty">
        <svg><!-- Icon --></svg>
        <p>Please configure the component</p>
    </div>
</sly>
```

---

## Sling Model Patterns

### 1. Model Annotation
```java
@Model(adaptables = {SlingHttpServletRequest.class, Resource.class},
       adapters = TeaserGridCardModel.class,
       defaultInjectionStrategy = DefaultInjectionStrategy.OPTIONAL)
public class ComponentNameModel {
    // ...
}
```

**Key Points:**
- `adaptables` - Support both Request and Resource
- `adapters` - Specify model class
- `defaultInjectionStrategy.OPTIONAL` - Prevent errors on missing properties

### 2. Package Structure
```
com.mohhwebsites.core.models.ComponentNameModel
```

### 3. Property Definitions

**Simple Properties:**
```java
@ValueMapValue
private String heading;

@ValueMapValue
private String description;

@ValueMapValue
@Default(values = "#6b6b6b")
private String headerTitleColor;
```

**Collections (Multifields):**
```java
@ChildResource
private List<Resource> cards;

private List<CardItem> validatedCards;
```

### 4. Inner Class for Child Resources
```java
@Model(adaptables = Resource.class,
       defaultInjectionStrategy = DefaultInjectionStrategy.OPTIONAL)
public static class CardItem {
    @ValueMapValue
    private String title;

    @ValueMapValue
    private String image;

    @ValueMapValue
    @Default(values = "_self")
    private String ctaTarget;

    // Getters with JavaDoc
    public String getTitle() {
        return title;
    }

    // Validation method
    public boolean isValid() {
        return StringUtils.isNotBlank(title) &&
               StringUtils.isNotBlank(image);
    }
}
```

### 5. Validation Pattern
```java
// Constants at top of class
private static final int MAX_TITLE_LENGTH = 100;
private static final int MIN_CARDS_REQUIRED = 1;
private static final int MAX_CARDS_ALLOWED = 6;

@PostConstruct
protected void init() {
    if (cards != null && !cards.isEmpty()) {
        validatedCards = cards.stream()
            .map(resource -> resource.adaptTo(CardItem.class))
            .filter(Objects::nonNull)
            .filter(CardItem::isValid)
            .limit(MAX_CARDS_ALLOWED)
            .collect(Collectors.toList());
    }
}

public boolean isValid() {
    return validatedCards != null &&
           !validatedCards.isEmpty() &&
           validatedCards.size() >= MIN_CARDS_REQUIRED;
}
```

### 6. Getters with Fallbacks
```java
public String getHeaderTitleColor() {
    return StringUtils.isNotBlank(headerTitleColor)
        ? headerTitleColor
        : "#6b6b6b";
}

public List<CardItem> getCards() {
    return validatedCards != null
        ? Collections.unmodifiableList(validatedCards)
        : Collections.emptyList();
}
```

### 7. Icon/SVG Generation Pattern
```java
public String getIconSvg() {
    if (platform == null) return "";

    String size = this.size != null ? this.size.replace("px", "") : "28";

    switch (platform.toLowerCase()) {
        case "facebook":
            return "<svg width=\"" + size + "\" height=\"" + size + "\"...";
        case "twitter":
            return "<svg width=\"" + size + "\" height=\"" + size + "\"...";
        default:
            return "";
    }
}
```

---

## Dialog XML Patterns

### 1. Root Structure (Complete)
```xml
<?xml version="1.0" encoding="UTF-8"?>
<jcr:root xmlns:sling="http://sling.apache.org/jcr/sling/1.0"
    xmlns:granite="http://www.adobe.com/jcr/granite/1.0"
    xmlns:cq="http://www.day.com/jcr/cq/1.0"
    xmlns:jcr="http://www.jcp.org/jcr/1.0"
    xmlns:nt="http://www.jcp.org/jcr/nt/1.0"
    jcr:primaryType="nt:unstructured"
    jcr:title="Component Display Name"
    sling:resourceType="cq/gui/components/authoring/dialog">
```

**Critical:** ALL 5 namespaces must be included!

### 2. Tab Organization
```xml
<content jcr:primaryType="nt:unstructured"
         sling:resourceType="granite/ui/components/coral/foundation/container">
    <items jcr:primaryType="nt:unstructured">
        <tabs jcr:primaryType="nt:unstructured"
              sling:resourceType="granite/ui/components/coral/foundation/tabs">
            <items jcr:primaryType="nt:unstructured">

                <!-- Tab 1: Header/Content -->
                <content jcr:primaryType="nt:unstructured"
                         jcr:title="Content"
                         sling:resourceType="granite/ui/components/coral/foundation/container">
                    <items jcr:primaryType="nt:unstructured">
                        <!-- Fields here -->
                    </items>
                </content>

                <!-- Tab 2: Cards/Items -->
                <cards jcr:primaryType="nt:unstructured" jcr:title="Cards">
                    <items jcr:primaryType="nt:unstructured">
                        <!-- Multifield here -->
                    </items>
                </cards>

            </items>
        </tabs>
    </items>
</content>
</jcr:root>
```

### 3. Field Types

**Textfield (Short Text):**
```xml
<headerTitle jcr:primaryType="nt:unstructured"
    sling:resourceType="granite/ui/components/coral/foundation/form/textfield"
    fieldLabel="Header Title"
    fieldDescription="Main heading text"
    name="./headerTitle"
    required="{Boolean}true"
    maxlength="{Long}100"/>
```

**Textarea (Long Text):**
```xml
<description jcr:primaryType="nt:unstructured"
    sling:resourceType="granite/ui/components/coral/foundation/form/textarea"
    fieldLabel="Description"
    name="./description"
    rows="{Long}3"
    maxlength="{Long}200"/>
```

**Pathfield (Links):**
```xml
<ctaLink jcr:primaryType="nt:unstructured"
    sling:resourceType="granite/ui/components/coral/foundation/form/pathfield"
    fieldLabel="CTA Link"
    name="./ctaLink"
    rootPath="/content"
    required="{Boolean}true"/>
```

**Colorfield:**
```xml
<headerTitleColor jcr:primaryType="nt:unstructured"
    sling:resourceType="granite/ui/components/coral/foundation/form/colorfield"
    fieldLabel="Title Color"
    name="./headerTitleColor"
    value="#6b6b6b"/>
```

**Select Dropdown:**
```xml
<ctaTarget jcr:primaryType="nt:unstructured"
    sling:resourceType="granite/ui/components/coral/foundation/form/select"
    fieldLabel="Link Target"
    name="./ctaTarget">
    <items jcr:primaryType="nt:unstructured">
        <self jcr:primaryType="nt:unstructured"
            text="Same Window"
            value="_self"
            selected="{Boolean}true"/>
        <blank jcr:primaryType="nt:unstructured"
            text="New Window"
            value="_blank"/>
    </items>
</ctaTarget>
```

### 4. Multifield Pattern
```xml
<cards jcr:primaryType="nt:unstructured"
    sling:resourceType="granite/ui/components/coral/foundation/form/multifield"
    composite="{Boolean}true"
    required="{Boolean}true"
    fieldLabel="Cards"
    fieldDescription="Add teaser cards (minimum 1, maximum 6)">
    <field jcr:primaryType="nt:unstructured"
        sling:resourceType="granite/ui/components/coral/foundation/container"
        name="./cards">
        <items jcr:primaryType="nt:unstructured">

            <image jcr:primaryType="nt:unstructured"
                sling:resourceType="cq/gui/components/authoring/dialog/fileupload"
                fieldLabel="Image"
                name="./image"
                mimeTypes="[image/png,image/jpeg,image/webp]"
                required="{Boolean}true"/>

            <title jcr:primaryType="nt:unstructured"
                sling:resourceType="granite/ui/components/coral/foundation/form/textarea"
                fieldLabel="Title"
                name="./title"
                required="{Boolean}true"
                maxlength="{Long}100"/>

        </items>
    </field>
</cards>
```

---

## SCSS Patterns

### 1. File Structure
```scss
// Variables at top
$teaser-grid-primary-color: #5EA6DB;
$teaser-grid-text-color: #6b6b6b;
$teaser-grid-card-height-desktop: 541px;
$teaser-grid-card-height-mobile: 420px;

// Main block
.cmp-teaser-grid {
    // Block styles

    // Elements
    &__header { }
    &__card { }

    // Modifiers
    &--empty { }
}
```

### 2. Responsive Breakpoints (MOHH Standard)
```scss
// Mobile first
.cmp-teaser-grid__card {
    width: 320px;
    height: $teaser-grid-card-height-mobile;

    // Tablet
    @media (min-width: 768px) {
        width: calc((100% - 28px) / 2);
    }

    // Desktop
    @media (min-width: 1024px) {
        width: calc((100% - 64px) / 3);
        height: $teaser-grid-card-height-desktop;
    }
}
```

### 3. Transitions & Animations
```scss
.cmp-teaser-grid__cards-container {
    transition: transform 0.5s cubic-bezier(0.4, 0, 0.2, 1);
    will-change: transform; // Performance optimization
}

// Respect user preferences
@media (prefers-reduced-motion: reduce) {
    .cmp-teaser-grid__cards-container {
        transition: none;
    }
}
```

### 4. List Resets (Always Include)
```scss
.cmp-teaser-grid__cards-container,
.cmp-teaser-grid__pagination {
    list-style: none;
    padding: 0;
    margin: 0;
}
```

### 5. Hover Effects
```scss
.cmp-teaser-grid__card {
    transition: transform 0.3s ease, box-shadow 0.3s ease;

    &:hover {
        transform: translateY(-4px);
        box-shadow: 0 8px 24px rgba(0, 0, 0, 0.15);
    }
}
```

---

## JavaScript Patterns

### 1. ES5 Compatibility (CRITICAL for AEM)

**❌ WRONG - ES6:**
```javascript
const SELECTOR = '.component';
const cards = document.querySelectorAll(SELECTOR);
cards.forEach(card => {
    console.log(`Card: ${card.id}`);
});
```

**✅ CORRECT - ES5:**
```javascript
var SELECTOR = '.component';
var cards = document.querySelectorAll(SELECTOR);
for (var i = 0; i < cards.length; i++) {
    console.log('Card: ' + cards[i].id);
}
```

### 2. IIFE Pattern with Strict Mode
```javascript
(function() {
    'use strict';

    // Component code here

})();
```

### 3. Initialization Pattern
```javascript
function initComponents() {
    var components = document.querySelectorAll('[data-cmp-is="component-name"]');
    for (var i = 0; i < components.length; i++) {
        new ComponentName(components[i]);
    }
}

// DOM ready detection
if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', initComponents);
} else {
    initComponents();
}
```

### 4. Constructor Pattern
```javascript
function ComponentName(element) {
    this.element = element;
    this.isInitialized = false;
    this.isTransitioning = false;

    this.init();
}

ComponentName.prototype.init = function() {
    if (this.isInitialized) return;

    this.setupEventListeners();
    this.setupAccessibility();
    this.isInitialized = true;
};
```

### 5. Event Listener Setup
```javascript
ComponentName.prototype.setupEventListeners = function() {
    var self = this;
    var prevButton = this.element.querySelector('.arrow--prev');
    var nextButton = this.element.querySelector('.arrow--next');

    if (prevButton) {
        prevButton.addEventListener('click', function() {
            self.slidePrev();
        });
    }

    if (nextButton) {
        nextButton.addEventListener('click', function() {
            self.slideNext();
        });
    }
};
```

### 6. Debouncing Pattern
```javascript
ComponentName.prototype.handleResize = function() {
    var self = this;
    clearTimeout(this.resizeTimeout);
    this.resizeTimeout = setTimeout(function() {
        self.updateLayout();
    }, 150);
};
```

### 7. Analytics Integration
```javascript
ComponentName.prototype.trackEvent = function(eventData) {
    if (typeof window.dataLayer !== 'undefined') {
        window.dataLayer.push({
            event: 'componentInteraction',
            componentName: 'teaser-grid-card',
            action: eventData.action,
            label: eventData.label
        });
    }

    // Development logging
    if (window.location.hostname === 'localhost') {
        console.log('Analytics Event:', eventData);
    }
};
```

### 8. AEM Author Mode Support
```javascript
// Re-initialize on dynamic content
if (typeof Granite !== 'undefined' && Granite.author) {
    var observer = new MutationObserver(function(mutations) {
        initComponents();
    });

    observer.observe(document.body, {
        childList: true,
        subtree: true
    });
}
```

---

## MOHH Color Palette

```scss
$mohh-primary-blue: #5EA6DB;      // Primary CTA, links
$mohh-primary-blue-dark: #6AACDB; // Hover state
$mohh-secondary-orange: #E85C23;  // Accents
$mohh-text-primary: #6b6b6b;      // Body text
$mohh-text-secondary: #7ba7d6;    // Subtitles
$mohh-text-light: #666666;        // Light text
$mohh-background: #F5F5F5;        // Page background
$mohh-border: #ddd;               // Borders, dividers
```

---

## Component Checklist

Before considering a component complete, verify:

### HTL Template:
- ✅ Model binding with data-sly-use
- ✅ All classes use cmp- prefix consistently
- ✅ data-sly-test for optional content
- ✅ data-sly-list for repeating items (NO hardcoded lists)
- ✅ Proper context hints (@context='uri', etc.)
- ✅ ARIA attributes for accessibility
- ✅ Empty state for author mode

### Sling Model:
- ✅ @Model annotation with adaptables
- ✅ @ValueMapValue for all dialog properties
- ✅ @ChildResource for multifields
- ✅ @PostConstruct init() for validation
- ✅ Inner class for child resources
- ✅ isValid() method
- ✅ Getters with JavaDoc
- ✅ Getters with fallback values
- ✅ Collections return unmodifiable or empty list

### Dialog:
- ✅ ALL 5 XML namespaces
- ✅ Complete XML structure (not truncated)
- ✅ Organized tabs
- ✅ name="./property" matches Model
- ✅ fieldLabel and fieldDescription on all fields
- ✅ required="{Boolean}true" for required fields
- ✅ Proper field types

### SCSS:
- ✅ Matches ALL HTL classes exactly
- ✅ BEM naming with cmp- prefix
- ✅ Responsive breakpoints (768px, 1024px)
- ✅ list-style: none on lists
- ✅ Transitions with prefers-reduced-motion
- ✅ Hover effects
- ✅ Variables for colors

### JavaScript:
- ✅ ES5 syntax (no const/let, no template literals, no arrows)
- ✅ IIFE with 'use strict'
- ✅ String concatenation (not template literals)
- ✅ for loops (not forEach)
- ✅ DOM ready detection
- ✅ Accessibility features
- ✅ Analytics integration
- ✅ AEM author mode support
