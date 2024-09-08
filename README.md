# Terminal Static Site Generator
A static site generator that takes a directory structure and turns it into a pseudo-terminal-like website.

---

Requires PyYAML, Jinja2, ignorelib and Markdown libraries.

```
usage: terminal-ssg.py [-h] [-c CONFIG] [-t TEMPLATE]

An SSG for generating a psudo-terminal website

options:
  -h, --help            show this help message and exit
  -c CONFIG, --config CONFIG
                        Path to config.yaml file
  -t TEMPLATE, --template TEMPLATE
                        Path to templates folder
```

## Config File Parameters

| Parameter | Type | Explanation |
| --- | --- | --- |
| `websiteDir` 		| String 		| Path to the website directory |
| `url` 			| String 		| URL of your website |
| `hostname` 		| String 		| Fictitious hostname of your "server" |
| `username` 		| String 		| Fictitious username of your "server" |
| `cwd` 			| String 		| Current Working Directory.  Not actually needed in the config file as it is created and edited at runtime but can be used as a variable in `prompt`. |
| `prompt` 			| String 		| Format of the terminal (PS1) prompt |
| `ignored` 		| String Array 	| Files/folders to be ignored and not be displayed on site |
| `forceDir` 		| String Array 	| Folders to force-display as a directory page regardless of contents |
| `logo` 			| String		| Text-based logo to be displayed on root and directory pages.  Requires a leading character so whitespace isn't eaten |
| `rootPreamble` 	| String Array 	| Text that will be displayed before the logo at root.  Each item is a new <p> block |
| `rootLogo` 		| String 		| Text-based logo to be displayed on root.  Requires a leading character so whitespace isn't eaten |
| `rootPostamble` 	| String Array 	| Text that will be displayed after the logo at root.  Each item is a new <p> block |
| `rootHeaders` 	| String Array 	| Headers that will only be put in the root <head> block |
| `errorPage` 		| Dict Array 	| Array of dictionaries with keys `error` and `text` to render http error pages |
| `embedTitle` 		| String 		| Title to be used in embeds |
| `embedDesc` 		| String 		| Default embed description to be used in the root page |
| `embedImage` 		| String 		| Image to be displayed in embeds |
| `embedColor` 		| String 		| Color to highlight embeds |
| `txtCommand` 		| String 		| Fictitious command that will preface the display of .txt files |
| `mdCommand` 		| String 		| Fictitious command that will preface the display of .md files |
| `htmlCommand` 	| String 		| Fictitious command that will preface the display of .html files |

Each key in the yaml file can be used as a templating variable in the file by surrounding it with braces such as `{username}` due to Python's str.format function.

Example provided in `config.yaml.sample`.

## File Display

The kinds of files that will be read and displayed are:

### .txt

Inserted in a `<pre>` tag.

### .md

Parsed through a markdown parser to html and inserted verbatim without autoescape.

### .html

Inserted verbatim without autoescape.

### links.yaml

A yaml file containing an array of dictionaries with the keys `name` and `href` to be inserted to allow external links.

e.g.

```yaml
- name: example
  href: https://example.com
```

Everything else will be listed in the `ls` module unless blacklisted in the config file.

Example output and website this was made for can be found at https://rockofdestiny.com