# HTL (HTML Template Language) Quick Reference

## Core HTL Block Elements

### data-sly-use
Load and initialize a Use-API object (Java class, JavaScript file, or template).

```htl
<!-- Java Sling Model -->
<div data-sly-use.model="com.mycompany.core.models.MyModel">
    ${model.property}
</div>

<!-- JavaScript Use-API -->
<div data-sly-use.helper="helper.js">
    ${helper.computed}
</div>

<!-- HTL Template -->
<div data-sly-use.templates="templates.html">
    <div data-sly-call="${templates.myTemplate}"></div>
</div>
```

### data-sly-test
Conditionally show/hide elements. Removes element if false/empty/null.

```htl
<!-- Basic conditional -->
<div data-sly-test="${properties.title}">
    <h2>${properties.title}</h2>
</div>

<!-- Store test result -->
<sly data-sly-test.hasContent="${properties.description}">
    <p data-sly-test="${hasContent}">${properties.description}</p>
</sly>

<!-- Logical operations -->
<div data-sly-test="${properties.show && properties.title}">
    Content
</div>
```

### data-sly-list
Iterate over arrays, lists, or collections.

```htl
<!-- Basic iteration -->
<ul data-sly-list="${model.items}">
    <li>${item}</li>
</ul>

<!-- Named item -->
<ul data-sly-list.product="${model.products}">
    <li>${product.name} - $${product.price}</li>
</ul>

<!-- Access iteration metadata -->
<ul data-sly-list.item="${model.items}">
    <li class="${itemList.first ? 'first' : ''} ${itemList.last ? 'last' : ''}">
        Item ${itemList.index + 1} of ${itemList.count}: ${item.title}
    </li>
</ul>
```

### data-sly-repeat
Like list, but doesn't generate surrounding element.

```htl
<div data-sly-repeat.item="${model.items}">
    <h3>${item.title}</h3>
    <p>${item.description}</p>
</div>
```

### data-sly-include
Include a script (processes JSP/HTL).

```htl
<!-- Include another component -->
<div data-sly-include="header.html"></div>

<!-- Include with parameters -->
<div data-sly-include="${'content.html' @ title='My Title'}"></div>
```

### data-sly-resource
Include a Sling resource.

```htl
<!-- Include resource at path -->
<div data-sly-resource="${'path/to/resource'}"></div>

<!-- Include with resource type override -->
<div data-sly-resource="${'./child' @ resourceType='myapp/components/text'}"></div>

<!-- Include with selector -->
<div data-sly-resource="${'./child' @ selectors='teaser'}"></div>
```

### data-sly-template & data-sly-call
Define and call reusable templates.

```htl
<!-- Define template -->
<template data-sly-template.card="${@ title, description, image}">
    <div class="card">
        <img src="${image}" alt="${title}">
        <h3>${title}</h3>
        <p>${description}</p>
    </div>
</template>

<!-- Call template -->
<div data-sly-call="${card @ title=properties.title,
                            description=properties.description,
                            image=properties.image}"></div>
```

### data-sly-unwrap
Remove the element but keep its content.

```htl
<!-- Element removed, content kept -->
<div data-sly-unwrap="${true}">
    <p>This paragraph will remain</p>
</div>
<!-- Result: <p>This paragraph will remain</p> -->

<!-- Conditional unwrap -->
<div data-sly-unwrap="${properties.unwrap}">
    Content
</div>
```

### data-sly-element
Dynamically set element name.

```htl
<!-- Change element based on condition -->
<div data-sly-element="${properties.headingLevel || 'h2'}">
    ${properties.title}
</div>

<!-- Result could be: <h2>Title</h2> or <h3>Title</h3> -->
```

### data-sly-attribute
Dynamically set attributes.

```htl
<!-- Set multiple attributes -->
<div data-sly-attribute.class="${properties.cssClass}"
     data-sly-attribute.id="${properties.id}">
    Content
</div>

<!-- Conditional attribute -->
<a data-sly-attribute.href="${properties.link ? properties.link : '#'}">
    Link
</a>

<!-- Remove attribute if null -->
<div data-sly-attribute.data-value="${properties.value}">
    <!-- data-value only added if properties.value exists -->
</div>
```

## Expression Contexts (XSS Protection)

### Available Contexts

```htl
<!-- text (default) - HTML-encodes -->
<p>${properties.text}</p>

<!-- html - Allows HTML tags (use with caution) -->
<div>${properties.richText @ context='html'}</div>

<!-- attribute - For HTML attributes -->
<div title="${properties.tooltip @ context='attribute'}"></div>

<!-- uri - For URLs -->
<a href="${properties.link @ context='uri'}">Link</a>

<!-- scriptString - For JavaScript strings -->
<script>
    var message = '${properties.message @ context='scriptString'}';
</script>

<!-- scriptComment - For JavaScript comments -->
<script>
    /* ${properties.comment @ context='scriptComment'} */
</script>

<!-- styleString - For CSS strings -->
<style>
    .element { color: ${properties.color @ context='styleString'}; }
</style>

<!-- number - Outputs a number -->
<span>${properties.count @ context='number'}</span>

<!-- unsafe - No escaping (DANGEROUS - avoid!) -->
<div>${properties.content @ context='unsafe'}</div>
```

## HTL Expression Language

### Operators

```htl
<!-- Logical operators -->
${a && b}           <!-- AND -->
${a || b}           <!-- OR -->
${!a}               <!-- NOT -->

<!-- Comparison operators -->
${a == b}           <!-- Equal -->
${a != b}           <!-- Not equal -->
${a < b}            <!-- Less than -->
${a <= b}           <!-- Less than or equal -->
${a > b}            <!-- Greater than -->
${a >= b}           <!-- Greater than or equal -->

<!-- Ternary operator -->
${condition ? 'yes' : 'no'}

<!-- Null coalescence -->
${properties.title || 'Default Title'}
```

### String Concatenation

```htl
<!-- Using + operator -->
${'Hello ' + properties.name}

<!-- Multiple expressions -->
<div class="component ${properties.modifier} ${properties.size}">
```

### Array/List Access

```htl
<!-- Access by index -->
${model.items[0]}

<!-- Access property -->
${model.items[0].title}
```

## HTL Options

### Format Options

```htl
<!-- format - String formatting -->
${'Hello {0}, welcome to {1}' @ format=[properties.name, properties.site]}

<!-- i18n - Internationalization -->
${'welcome.message' @ i18n}

<!-- join - Join array with separator -->
${model.tags @ join=', '}
```

### Display Options

```htl
<!-- Display context -->
${properties.text @ context='html'}

<!-- Display format for dates/numbers -->
${properties.date @ format='dd MMM yyyy'}
${properties.price @ format='currency', locale='en_US'}
```

## Common Patterns

### Safe Property Access

```htl
<!-- Check if property exists before using -->
<div data-sly-test="${properties.title}">
    <h2>${properties.title}</h2>
</div>

<!-- Provide default value -->
<h2>${properties.title || 'Default Title'}</h2>
```

### Iteration with Index-based Styling

```htl
<ul data-sly-list.item="${model.items}">
    <li class="item-${itemList.index}
               ${itemList.first ? 'first' : ''}
               ${itemList.last ? 'last' : ''}
               ${itemList.odd ? 'odd' : 'even'}">
        ${item.title}
    </li>
</ul>
```

### Conditional CSS Classes

```htl
<div class="component
            ${properties.alignment}
            ${properties.highlighted ? 'highlighted' : ''}
            ${properties.size || 'medium'}">
    Content
</div>
```

### Image with Fallback

```htl
<img src="${properties.image || '/content/dam/default-image.jpg'}"
     alt="${properties.imageAlt || properties.title || 'Image'}"
     data-sly-test="${properties.image || '/content/dam/default-image.jpg'}"/>
```

### Link with Optional Target

```htl
<a href="${properties.link @ context='uri'}"
   data-sly-attribute.target="${properties.openInNewTab ? '_blank' : ''}"
   data-sly-attribute.rel="${properties.openInNewTab ? 'noopener noreferrer' : ''}">
    ${properties.linkText}
</a>
```

### Empty State Handling

```htl
<div data-sly-test="${model.items && model.items.size > 0}"
     data-sly-list.item="${model.items}">
    <div class="item">${item.title}</div>
</div>

<div data-sly-test="${!model.items || model.items.size == 0}">
    <p class="no-items">No items to display</p>
</div>
```

## ItemList Properties (for data-sly-list)

```htl
${itemList.index}       <!-- Current index (0-based) -->
${itemList.count}       <!-- Total number of items -->
${itemList.first}       <!-- true if first item -->
${itemList.middle}      <!-- true if middle item -->
${itemList.last}        <!-- true if last item -->
${itemList.odd}         <!-- true if odd index -->
${itemList.even}        <!-- true if even index -->
```

## Comments

```htl
<!-- HTML comment (visible in source) -->
<!--/* HTL comment (not rendered to output) */-->
```

## Best Practices

1. **Always use appropriate context** - Prevent XSS vulnerabilities
2. **Prefer data-sly-test over CSS display:none** - Better for performance
3. **Use templates for repeated markup** - Keep code DRY
4. **Null-safe expressions** - Use || for defaults
5. **Semantic HTML** - Use proper HTML5 elements
6. **Avoid complex logic in HTL** - Move to Sling Models
7. **Use data-sly-unwrap** - For cleaner markup
8. **Consistent naming** - Use meaningful variable names
9. **Document complex templates** - Add HTL comments
10. **Test for empty states** - Always handle no-data scenarios
