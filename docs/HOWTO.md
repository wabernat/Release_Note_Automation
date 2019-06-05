# How to Modify the Release Notes

All templates and static assets used to build the release notes reside in a subdirectory of docs/.

Currently three products are defined:
 - S3C => s3c
 - RING => ring
 - Zenko => zenko
A special subdirectory `common` also exists for cross-product assets (such as css styling)

Within each subdirectory, define a `layout.yaml` with the following structure:

```yaml
---
layout:
    - mypages.html
    - gohere.html
    - woohoo.html
```
This file specifies the order in which components are added to the generated document.

## Where do the file names come from?

To reference files from within the same product (denoted by assets/<product>) simply use the file name (e.g., `introduction.html`)
To reference files from other projects, or from common/, prefix it with the subdirectory name (e.g., `common/issue_header.html`)
To reference generated sections (e.g., the fixed issues table) use the special prefix `$templates/` (e.g., `$templates/issues.fixed`)
Currently there are only two generated sections: `issues.fixed` and `issues.known`. In the future this may include New Features,
but we need more disciplined in our Jira use before this can be automated.

**NOTE**: Isolating files by product is not enforced by notomaton, both for flexibility and simplicity. **You** are the only one
standing in the way of turning this into a giant pile of spaghetti. WITH GREAT POWER COMES GREAT RESPONSIBILITY.

## What's this about templates?
All HTML files specified in a layout are treated as a `jinja2` template, giving you access to variables from the current product within the template itself.

### Why would you want to do this?

Consider the introduction currently used by all projects:

```html
<h2>New for {{ ctx.product.name }} Version {{ ctx.product.version }}</h2>

{{ ctx.product.name }} introduces the following new features in version {{ ctx.product.version }}.
```

Here the variables `{{ ctx.product.version }}` and `{{ ctx.product.name }}` are replaced with the appropriate values when generating the release notes.
This allows you to reuse copy and assets between products, obviating the need to maintain a custom version for each.

### The Context

All variables in templates are accessed as properties of the `ctx` variable.

**Avalailable properties**
- `ctx.product.name` - Product name as used in print ie `S3 Connector`
- `ctx.product.version` - Product version ie `1.0.0`
- `ctx.product.canonical` - Canonical product name ie `S3 Connector` => `s3c` (useful for links)
- `ctx.issues.fixed` - List of fixed issues in this release
- `ctx.issues.known` - List of know issue for this release
- `ctx.style` - CSS stylesheet
