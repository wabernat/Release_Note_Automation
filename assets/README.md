# How to modify the Release Notes

All templates and static assets used to build the release notes should live in a subdirectory of assets.

Currently 3 products are defined:
 - S3C => s3c
 - RING => ring
 - Zenko => zenko
A special subdirectory `common` also exists for cross product assets (think css styling)

Within each subdirectory a `layout.yaml` should be defined with the following structure:

```yaml
---
layout:
    - mypages.html
    - gohere.html
    - woohoo.html
```
This file specifies the order components should be added to the generated document.

## So where do the file names come from?**
To reference files from within the same product (denoted by asset/<product>) simply use the file name (eg `introduction.html`)
To reference files from other projects, or from common, prefix it with the subdirectory name (eg `common/issue_header.html`)
To reference generated bits (eg the fixed issues table) use the special prefix `$gen/` (eg `$gen/fixed_issues`)
Currently there are only 2 generated sections: `fixed_issues` and `known_issues`

**NOTE**: Isolating files by product is not enforced by notomaton, both for flexibility and simplicity. **You** are the only one
standing in the way of the turning into a giant pile of spaghetti. WITH GREAT POWER COME GREAT RESPONSIBILITY.

## So what this about templates?
All html files specified in a layout will be treated as a `jinja2` template. This means you can access variables from the current product within the template itself.

### Why would you want to do this?

Consider the introduction currently used by all projects:

```html
<h2>New for Version {{ version }}</h2>

{{ product }} introduces the following new features in release {{ version }}.
```

Here the variables `{{ version }}` and `{{ product }}` are used, which are replaced with the appropriate values when generating the release notes.
This allows you to reuse copy and assets between products negating the need to maintain a custom version for each.

Currently only two variables are defined:
 - `{{ version }}`
 - `{{ product }}`
