# Common AEM Component Mistakes & Fixes

Based on real issues found and fixed in MOHH project.

---

## 1. Hardcoded Content Instead of Dynamic

### ❌ WRONG: Hardcoded Social Icons
```html
<ul class="social-list">
  <li><a href="#"><svg>facebook icon</svg></a></li>
  <li><a href="#"><svg>twitter icon</svg></a></li>
  <li><a href="#"><svg>instagram icon</svg></a></li>
</ul>
```

**Problems:**
- Not author-friendly
- Can't add/remove platforms
- Can't change URLs

### ✅ CORRECT: Dynamic with Multifield
```html
<ul class="social-list">
  <li data-sly-list.icon="${model.socialIcons}">
    <a href="${icon.url}">
      ${icon.iconSvg @ context='unsafe'}
    </a>
  </li>
</ul>
```

**Sling Model:**
```java
@ChildResource
private List<Resource> socialIcons;

public static class SocialIcon {
    @ValueMapValue
    private String platform; // facebook, twitter, etc.

    @ValueMapValue
    private String url;

    public String getIconSvg() {
        // Generate SVG based on platform
    }
}
```

---

## 2. CSS Class Name Mismatches

### ❌ WRONG: HTL and SCSS Don't Match
```html
<!-- HTL -->
<footer class="footer">
  <div class="footer__logo">Logo</div>
</footer>
```

```scss
/* SCSS */
.cmp-footer {           /* ← MISMATCH! */
  &__logo { }
}
```

**Result:** No styles applied!

### ✅ CORRECT: Exact Match
```html
<!-- HTL -->
<footer class="cmp-footer">
  <div class="cmp-footer__logo">Logo</div>
</footer>
```

```scss
/* SCSS */
.cmp-footer {           /* ← MATCHES! */
  &__logo { }
}
```

---

## 3. ES6 Syntax in JavaScript (Breaks AEM)

### ❌ WRONG: ES6 Features
```javascript
// Template literals
const message = `Hello ${name}`;

// Arrow functions
cards.forEach(card => {
  console.log(card);
});

// const/let
const SELECTOR = '.component';

// Destructuring
const {title, description} = card;
```

**Result:** JavaScript errors in AEM!

### ✅ CORRECT: ES5 Compatible
```javascript
// String concatenation
var message = 'Hello ' + name;

// Regular functions
for (var i = 0; i < cards.length; i++) {
  console.log(cards[i]);
}

// var only
var SELECTOR = '.component';

// Manual property access
var title = card.title;
var description = card.description;
```

---

## 4. Incomplete Dialog XML

### ❌ WRONG: Truncated XML
```xml
<?xml version="1.0" encoding="UTF-8"?>
<jcr:root xmlns:sling="http://sling.apache.org/jcr/sling/1.0"
    jcr:primaryType="nt:unstructured">
    <content>
        <items>
            <tabs>
                <items>
                    <content>
                        <items>
                            <!-- Fields here but XML cuts off... -->
```

**Result:** Dialog won't work!

### ✅ CORRECT: Complete Structure
```xml
<?xml version="1.0" encoding="UTF-8"?>
<jcr:root xmlns:sling="http://sling.apache.org/jcr/sling/1.0"
    xmlns:granite="http://www.adobe.com/jcr/granite/1.0"
    xmlns:cq="http://www.day.com/jcr/cq/1.0"
    xmlns:jcr="http://www.jcp.org/jcr/1.0"
    xmlns:nt="http://www.jcp.org/jcr/nt/1.0"
    jcr:primaryType="nt:unstructured"
    jcr:title="Component Name"
    sling:resourceType="cq/gui/components/authoring/dialog">
    <content jcr:primaryType="nt:unstructured">
        <items jcr:primaryType="nt:unstructured">
            <tabs>
                <!-- Complete structure -->
            </tabs>
        </items>
    </content>
</jcr:root>  <!-- ← Must close! -->
```

**Must include:**
- ✅ All 5 XML namespaces
- ✅ Proper closing tags
- ✅ Complete nested structure

---

## 5. Missing Data Flow Chain

### ❌ WRONG: Broken Chain
```xml
<!-- Dialog -->
<heading name="./title"/>  <!-- ← Wrong name! -->
```

```java
// Sling Model
@ValueMapValue
private String heading;  // ← Doesn't match dialog!

public String getHeading() {
    return heading;
}
```

```html
<!-- HTL -->
${model.title}  <!-- ← Wrong property! -->
```

**Result:** Data doesn't flow, component empty!

### ✅ CORRECT: Complete Chain
```xml
<!-- Dialog -->
<heading name="./heading"/>  <!-- ← Matches! -->
```

```java
// Sling Model
@ValueMapValue
private String heading;  // ← Matches! -->

public String getHeading() {
    return heading;
}
```

```html
<!-- HTL -->
${model.heading}  <!-- ← Matches! -->
```

---

## 6. Missing List Resets in SCSS

### ❌ WRONG: Default List Styling
```scss
.cmp-footer__social-list {
  display: flex;
  gap: 18px;
}
```

**Result:** Bullet points visible, extra padding!

### ✅ CORRECT: Reset List Styles
```scss
.cmp-footer__social-list {
  list-style: none;    /* ← Remove bullets */
  padding: 0;          /* ← Remove padding */
  margin: 0;           /* ← Remove margin */
  display: flex;
  gap: 18px;
}
```

---

## 7. No Validation in Sling Model

### ❌ WRONG: No Validation
```java
@Model(adaptables = Resource.class)
public class ComponentModel {
    @ValueMapValue
    private String title;

    @ChildResource
    private List<Resource> items;

    // No validation!
    public List<Resource> getItems() {
        return items;  // Could be null!
    }
}
```

**Result:** NullPointerException, component breaks!

### ✅ CORRECT: With Validation
```java
@Model(adaptables = Resource.class,
       defaultInjectionStrategy = DefaultInjectionStrategy.OPTIONAL)
public class ComponentModel {
    private static final int MAX_ITEMS = 6;

    @ValueMapValue
    private String title;

    @ChildResource
    private List<Resource> items;

    private List<Item> validatedItems;

    @PostConstruct
    protected void init() {
        if (items != null && !items.isEmpty()) {
            validatedItems = items.stream()
                .map(r -> r.adaptTo(Item.class))
                .filter(Objects::nonNull)
                .filter(Item::isValid)
                .limit(MAX_ITEMS)
                .collect(Collectors.toList());
        }
    }

    public boolean isValid() {
        return StringUtils.isNotBlank(title) &&
               validatedItems != null &&
               !validatedItems.isEmpty();
    }

    public List<Item> getItems() {
        return validatedItems != null
            ? Collections.unmodifiableList(validatedItems)
            : Collections.emptyList();
    }
}
```

---

## 8. Missing Context Hints (Security Issue)

### ❌ WRONG: No Context
```html
<a href="${model.link}">           <!-- Vulnerable! -->
<img src="${model.image}">         <!-- Vulnerable! -->
<div style="color: ${model.color}"><!-- Vulnerable! -->
```

**Result:** XSS vulnerability!

### ✅ CORRECT: Proper Context
```html
<a href="${model.link @ context='uri'}">
<img src="${model.image @ context='uri'}">
<div style="color: ${model.color @ context='styleString'}">
${model.svg @ context='unsafe'}  <!-- Only for trusted content -->
```

---

## 9. Hardcoded Carousel Visible Cards

### ❌ WRONG: Fixed Number
```javascript
var visibleCards = 3;  // Always 3!
```

**Result:** Breaks on mobile!

### ✅ CORRECT: Responsive
```javascript
ComponentName.prototype.updateVisibleCards = function() {
    var width = window.innerWidth;

    if (width < 768) {
        this.visibleCards = 1;  // Mobile
    } else if (width < 1024) {
        this.visibleCards = 2;  // Tablet
    } else {
        this.visibleCards = 3;  // Desktop
    }
};
```

---

## 10. No Accessibility Attributes

### ❌ WRONG: No ARIA
```html
<button class="arrow-prev">Prev</button>
<div class="card">
  <img src="...">
  <h3>Title</h3>
</div>
```

**Result:** Screen readers can't understand!

### ✅ CORRECT: With ARIA
```html
<button class="arrow-prev"
        aria-label="Previous card"
        aria-controls="cards-container">
  Prev
</button>

<article class="card"
         role="article"
         aria-label="Card: ${card.title}">
  <img src="..." alt="${card.imageAlt}">
  <h3 id="card-title-${cardList.index}">${card.title}</h3>
</article>
```

---

## 11. Missing Empty State for Authors

### ❌ WRONG: Blank Component
```html
<div class="component" data-sly-test="${model.valid}">
  <!-- Content -->
</div>
<!-- Nothing shown if invalid! -->
```

**Result:** Authors confused, think component broken!

### ✅ CORRECT: With Empty State
```html
<div class="component" data-sly-test="${model.valid}">
  <!-- Content -->
</div>

<sly data-sly-test="${!model.valid && wcmmode.edit}">
  <div class="component--empty">
    <svg><!-- Icon --></svg>
    <h3>Component Not Configured</h3>
    <p>Please open the dialog to configure this component.</p>
  </div>
</sly>
```

---

## 12. Transitions Without prefers-reduced-motion

### ❌ WRONG: Always Animates
```scss
.card {
  transition: transform 0.3s ease;

  &:hover {
    transform: translateY(-4px);
  }
}
```

**Result:** Accessibility issue for users with motion sensitivity!

### ✅ CORRECT: Respects User Preferences
```scss
.card {
  transition: transform 0.3s ease;

  &:hover {
    transform: translateY(-4px);
  }

  @media (prefers-reduced-motion: reduce) {
    transition: none;

    &:hover {
      transform: none;
    }
  }
}
```

---

## 13. Missing Namespace in Dialog XML

### ❌ WRONG: Missing Namespaces
```xml
<?xml version="1.0" encoding="UTF-8"?>
<jcr:root xmlns:sling="http://sling.apache.org/jcr/sling/1.0"
    jcr:primaryType="nt:unstructured">
  <!-- Missing granite, cq, jcr, nt namespaces! -->
</jcr:root>
```

**Result:** Dialog won't render!

### ✅ CORRECT: All 5 Namespaces
```xml
<?xml version="1.0" encoding="UTF-8"?>
<jcr:root xmlns:sling="http://sling.apache.org/jcr/sling/1.0"
    xmlns:granite="http://www.adobe.com/jcr/granite/1.0"
    xmlns:cq="http://www.day.com/jcr/cq/1.0"
    xmlns:jcr="http://www.jcp.org/jcr/1.0"
    xmlns:nt="http://www.jcp.org/jcr/nt/1.0"
    jcr:primaryType="nt:unstructured"
    jcr:title="Component"
    sling:resourceType="cq/gui/components/authoring/dialog">
```

---

## 14. No Image Alt Text Fallback

### ❌ WRONG: Empty Alt If Not Provided
```java
public String getImageAlt() {
    return imageAlt;  // Could be null or empty!
}
```

**Result:** Accessibility failure!

### ✅ CORRECT: Fallback to Title
```java
public String getImageAlt() {
    return StringUtils.isNotBlank(imageAlt)
        ? imageAlt
        : title;  // Fallback to card title
}
```

---

## 15. Missing Module Export for JS

### ❌ WRONG: No Export
```javascript
(function() {
    'use strict';

    function ComponentName(element) {
        // Constructor
    }

    // Methods...

    // Not exported!
})();
```

**Result:** Can't test or reuse!

### ✅ CORRECT: With Export
```javascript
(function() {
    'use strict';

    function ComponentName(element) {
        // Constructor
    }

    // Methods...

    // Export for CommonJS/Node
    if (typeof module !== 'undefined' && module.exports) {
        module.exports = ComponentName;
    }

    // Also attach to window for browser
    if (typeof window !== 'undefined') {
        window.ComponentName = ComponentName;
    }

})();
```

---

## Quick Checklist to Avoid Mistakes

Before completing a component:

- [ ] No hardcoded lists (use data-sly-list)
- [ ] HTL and SCSS classes match exactly
- [ ] JavaScript uses ES5 only (no ES6)
- [ ] Dialog XML is complete (not truncated)
- [ ] Data flow chain verified (Dialog → Model → HTL)
- [ ] List styles reset (list-style: none, padding: 0)
- [ ] Sling Model has validation
- [ ] Context hints on all dynamic values
- [ ] Responsive visible cards calculation
- [ ] ARIA attributes for accessibility
- [ ] Empty state for author mode
- [ ] prefers-reduced-motion support
- [ ] All 5 XML namespaces in dialog
- [ ] Image alt text with fallback
- [ ] JavaScript module export
