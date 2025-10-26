# AEM Component Development Patterns and Best Practices

## Component Structure Standards

### Standard AEM Component File Structure
```
component-name/
├── _cq_dialog.xml              # Author dialog configuration
├── _cq_editConfig.xml          # Edit configuration (optional)
├── _cq_design_dialog.xml       # Design dialog (optional)
├── component-name.html         # HTL template
├── clientlibs/                 # Client libraries folder
│   ├── css/
│   │   └── component-name.css
│   ├── js/
│   │   └── component-name.js
│   └── .content.xml
├── README.md                   # Component documentation
└── .content.xml                # Component metadata
```

## HTL (Sightly) Best Practices

### 1. Use data-sly-use for Java/JavaScript Models
```htl
<!-- Good: Use Sling Models for backend logic -->
<div data-sly-use.model="com.mycompany.core.models.MyComponentModel">
    <h2>${model.title}</h2>
    <p>${model.description}</p>
</div>

<!-- Also acceptable: Use JavaScript Use-API for simple logic -->
<div data-sly-use.helper="helper.js">
    <p>${helper.formattedDate}</p>
</div>
```

### 2. Proper HTL Context and XSS Protection
```htl
<!-- Text content - auto-escapes HTML -->
<p>${properties.text}</p>

<!-- HTML content - requires @context -->
<div>${properties.richText @ context='html'}</div>

<!-- Attributes -->
<a href="${properties.link @ context='uri'}">${properties.linkText}</a>

<!-- JavaScript -->
<script>
    var config = ${model.jsonConfig @ context='scriptString'};
</script>

<!-- CSS -->
<style>
    .component { color: ${properties.color @ context='styleString'}; }
</style>
```

### 3. Conditional Rendering
```htl
<!-- Use data-sly-test for conditionals -->
<div data-sly-test="${properties.showContent}">
    <p>${properties.content}</p>
</div>

<!-- Combine with unwrap for cleaner markup -->
<sly data-sly-test="${properties.title}">
    <h2>${properties.title}</h2>
</sly>
```

### 4. Iteration Patterns
```htl
<!-- List iteration -->
<ul data-sly-list.item="${model.items}">
    <li>${item.title}</li>
</ul>

<!-- Access index -->
<ul data-sly-list.item="${model.items}">
    <li data-sly-test="${itemList.index == 0}" class="first">${item.title}</li>
    <li data-sly-test="${itemList.index != 0}">${item.title}</li>
</ul>
```

## Sling Model Best Practices

### 1. Standard Sling Model Pattern
```java
package com.mycompany.core.models;

import org.apache.sling.api.resource.Resource;
import org.apache.sling.models.annotations.Model;
import org.apache.sling.models.annotations.DefaultInjectionStrategy;
import org.apache.sling.models.annotations.injectorspecific.ValueMapValue;
import org.apache.sling.models.annotations.injectorspecific.ChildResource;
import javax.annotation.PostConstruct;
import java.util.Collections;
import java.util.List;

@Model(adaptables = Resource.class,
       defaultInjectionStrategy = DefaultInjectionStrategy.OPTIONAL)
public class MyComponentModel {

    @ValueMapValue
    private String title;

    @ValueMapValue
    private String description;

    @ChildResource
    private List<Resource> items;

    private String processedTitle;

    @PostConstruct
    protected void init() {
        // Post-processing logic
        processedTitle = title != null ? title.toUpperCase() : "";
    }

    // Getters
    public String getTitle() {
        return title;
    }

    public String getDescription() {
        return description;
    }

    public String getProcessedTitle() {
        return processedTitle;
    }

    public List<Resource> getItems() {
        return items != null ? items : Collections.emptyList();
    }
}
```

### 2. Use DefaultInjectionStrategy
```java
// Always use DefaultInjectionStrategy.OPTIONAL
@Model(adaptables = Resource.class,
       defaultInjectionStrategy = DefaultInjectionStrategy.OPTIONAL)
```

### 3. Proper Injection Annotations
```java
@ValueMapValue                  // For direct properties
@ChildResource                  // For child resources
@Self                          // For current adaptable
@SlingObject                   // For Sling objects (Request, Response, etc.)
@OSGiService                   // For OSGi services
@ScriptVariable                // For script variables
```

## Dialog Configuration Patterns

### 1. Standard Text Field
```xml
<title
    jcr:primaryType="nt:unstructured"
    sling:resourceType="granite/ui/components/coral/foundation/form/textfield"
    fieldLabel="Title"
    name="./title"
    required="{Boolean}true"/>
```

### 2. Rich Text Editor
```xml
<text
    jcr:primaryType="nt:unstructured"
    sling:resourceType="cq/gui/components/authoring/dialog/richtext"
    fieldLabel="Text"
    name="./text"
    useFixedInlineToolbar="{Boolean}true">
    <rtePlugins jcr:primaryType="nt:unstructured">
        <format
            jcr:primaryType="nt:unstructured"
            features="[bold,italic,underline]"/>
        <links
            jcr:primaryType="nt:unstructured"
            features="[modifylink,unlink]"/>
        <lists
            jcr:primaryType="nt:unstructured"
            features="[ordered,unordered]"/>
    </rtePlugins>
</text>
```

### 3. Path Field (Image/Asset)
```xml
<image
    jcr:primaryType="nt:unstructured"
    sling:resourceType="cq/gui/components/authoring/dialog/fileupload"
    fieldLabel="Image"
    name="./fileReference"
    multiple="{Boolean}false"
    mimeTypes="[image/gif,image/jpeg,image/png,image/webp,image/svg+xml]"/>
```

### 4. Dropdown/Select
```xml
<layout
    jcr:primaryType="nt:unstructured"
    sling:resourceType="granite/ui/components/coral/foundation/form/select"
    fieldLabel="Layout"
    name="./layout">
    <items jcr:primaryType="nt:unstructured">
        <left
            jcr:primaryType="nt:unstructured"
            text="Left Aligned"
            value="left"/>
        <center
            jcr:primaryType="nt:unstructured"
            text="Center Aligned"
            value="center"/>
        <right
            jcr:primaryType="nt:unstructured"
            text="Right Aligned"
            value="right"/>
    </items>
</select>
```

### 5. Multifield (Repeating Items)
```xml
<items
    jcr:primaryType="nt:unstructured"
    sling:resourceType="granite/ui/components/coral/foundation/form/multifield"
    composite="{Boolean}true"
    fieldLabel="Items">
    <field
        jcr:primaryType="nt:unstructured"
        sling:resourceType="granite/ui/components/coral/foundation/container"
        name="./items">
        <items jcr:primaryType="nt:unstructured">
            <title
                jcr:primaryType="nt:unstructured"
                sling:resourceType="granite/ui/components/coral/foundation/form/textfield"
                fieldLabel="Title"
                name="title"/>
            <description
                jcr:primaryType="nt:unstructured"
                sling:resourceType="granite/ui/components/coral/foundation/form/textarea"
                fieldLabel="Description"
                name="description"/>
        </items>
    </field>
</multifield>
```

## Component Metadata (.content.xml)

```xml
<?xml version="1.0" encoding="UTF-8"?>
<jcr:root xmlns:cq="http://www.day.com/jcr/cq/1.0"
    xmlns:jcr="http://www.jcp.org/jcr/1.0"
    jcr:primaryType="cq:Component"
    jcr:title="My Component"
    jcr:description="Description of what this component does"
    componentGroup="MyProject - Content"
    cq:icon="text"/>
```

## Naming Conventions

### Component Names
- Use lowercase with hyphens: `hero-banner`, `card-grid`, `feature-list`
- Be descriptive and consistent
- Group related components: `form-text`, `form-select`, `form-checkbox`

### Property Names
- Use camelCase: `title`, `description`, `imageAlt`, `linkUrl`
- Be semantic and clear
- Avoid abbreviations unless standard (e.g., `url`, `alt`, `src`)

### Model Class Names
- Use PascalCase: `HeroBannerModel`, `CardGridModel`
- Suffix with "Model": `MyComponentModel`
- One model per component typically

### CSS Class Names
- Use BEM notation: `.cmp-herobannerblock__title`, `.cmp-card--featured`
- Prefix with `cmp-`: `.cmp-component-name`
- Be specific to avoid conflicts

## AEM 6.5 vs Cloud Service Considerations

### File Naming Differences
- AEM 6.5: Use underscore prefix `_cq_dialog.xml`
- AEM Cloud Service: Can use `.cq_dialog.xml` (dot prefix)

### Editable Templates
- Use Editable Templates (not static templates)
- Define component policies
- Configure allowed components per template

## Testing Checklist

- [ ] Component renders without errors in author mode
- [ ] Component renders correctly in publish mode
- [ ] All dialog fields work and save properly
- [ ] Sling Model returns expected values
- [ ] HTL escaping is correct (no XSS vulnerabilities)
- [ ] Component is responsive (mobile, tablet, desktop)
- [ ] Component works in different parsys/containers
- [ ] Component can be copied/pasted
- [ ] Component exports work for SPA/headless if needed
- [ ] Clientlibs are loaded correctly
- [ ] Component has proper accessibility (ARIA, semantic HTML)

## Common Pitfalls to Avoid

1. **Don't use scriptlets (Java in JSP)** - Always use HTL + Sling Models
2. **Don't access JCR directly** - Use Sling Resource API
3. **Don't hardcode paths** - Use configurable dialogs
4. **Don't forget XSS protection** - Use proper HTL contexts
5. **Don't create monolithic components** - Keep components focused and reusable
6. **Don't skip null checks** - Always handle missing properties gracefully
7. **Don't use inline styles** - Use CSS classes and clientlibs
8. **Don't forget responsive design** - Test on multiple screen sizes
9. **Don't skip documentation** - Add README.md for each component
10. **Don't deploy without testing** - Test in author and publish modes
