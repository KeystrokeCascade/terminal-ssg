# Terminal Static Site Generator
A static site generator that takes a directory structure and turns it into a pseudo-terminal-like website.

---

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

### .md

### .html

Everything else will be listed in the `ls` module unless blacklisted in the config file.

Example output and website this was made for can be found at https://rockofdestiny.com