# Terminal Static Site Generator
A static site generator that takes a directory structure and turns it into a pseudo-terminal-like website.

---

Config file parameters:
| Parameter | Type | Explanation |
| --- | --- | --- |
| `website` 		| String 		| Path to the website directory |
| `hostname` 		| String 		| Fictitious hostname of your "server" |
| `username` 		| String 		| Fictitious username of your "server" |
| `cwd` 			| String 		| Current Working Directory.  Not actually needed in the config file as it is created and edited at runtime but can be used as a variable in `prompt`. |
| `prompt` 			| String 		| Format of the terminal (PS1) prompt |
| `ignored` 		| String Array 	| ArrayFiles/folders to be ignored and not be displayed on site |
| `logo` 			| String		| Text-based logo to be displayed on root and directory pages.  Requires a leading character so whitespace isn't eaten |
| `rootPreamble` 	| String Array 	| Text that will be displayed before the logo at root.  Each item is a new <p> block |
| `rootLogo` 		| String 		| Text-based logo to be displayed on root.  Requires a leading character so whitespace isn't eaten |
| `rootPostamble` 	| String Array 	| Text that will be displayed after the logo at root.  Each item is a new <p> block |

Each key in the yaml file can be used as a templating variable in the file by surrounding it with braces such as `{username}` due to Python's str.format function.

Example provided in `config.yaml.sample`.
