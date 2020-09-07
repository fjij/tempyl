# Tempyl

Tempyl is a super simple python-based templating tool. It's super easy to use
with LaTeX and HTML, but can be used for whatever you want.

## Usage

Download `tempyl.py` and run it as follows:
```bash
python3 tempyl.py template_file data_file output_file
```

## Features

### Replacing identifiers

`template.html`
```html
<h1>$article_name</h1>
```
`data.json`
```json
{
  "article_name": "My favorite restauraunt!"
}
```
`output.html`
```html
<h1>My favorite restaurant!</h1>
```

### Data scopes
Use data scopes access JSON sub-objects.

`template.html`
```html
## article
<h1>$name</h1>
##
```
`data.json`
```json
{
  "article": {
    "name": "Why pasta tastes good."
  }
}
```
`output.html`
```html
<h1>Why pasta tastes good.</h1>
```

### List iteration
Iterate over JSON lists and reuse part of a template.

`template.html`
```html
<h1>$title</h1>
## items
<h2>$name</h2>
<p>$desc</p>
##
```
`data.json`
```json
{
  "title": "A list of things",
  "items": [
    {
      "name": "Thing A",
      "desc": "Not thing B"
    },
    {
      "name": "Thing B",
      "desc": "Not thing A"
    }
  ]
}
```
`output.html`
```html
<h1>A list of things</h1>
<h2>Thing A</h2>
<p>Not thing B</p>
<h2>Thing B</h2>
<p>Not thing A</p>
```

## Extra Features

### List properties, `self` identifier
Use special identifier `self for a list of strings.
`template.txt`
```txt
My favorite letters:
## items
  $self
##
```
Edit `list.begin`, `.separator` and `.end` properties to change how lists are
rendered.
`data.json`
```json
{
  "items.begin": "",
  "items.separator": ", ",
  "items.end": ".",
  "items": ["a", "b", "c"]
}
```
`out.txt`
```txt
My favorite letters: a, b, c.
```

### List disabling
Disable elements in a list with `.disabled`.
`template.txt`
```txt
## items
  $items.name
##
```
`data.json`
```json
{
  "items": [
    { "name": "grape" },
    { ".disabled": true, "name": "apple" },
    { "name": "orange" }
  ]
}
```
`out.txt`
```txt
  grape
  orange
```
