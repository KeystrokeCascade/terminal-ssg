#!/usr/bin/env python3
'''
Terminal Static Site Generator

todo: good embed generation, finish when I have built compatable structure
'''
import argparse
import yaml
import jinja2
import os
import ignorelib
import markdown
from bs4 import BeautifulSoup
import re

# Flags
parser = argparse.ArgumentParser(
	description='An SSG for generating a psudo-terminal website',
	formatter_class=argparse.RawDescriptionHelpFormatter)

parser.add_argument('-c', '--config', default='config.yaml', help='Path to config.yaml file')
parser.add_argument('-t', '--template', default='./templates', help='Path to templates folder')
args = parser.parse_args()

# Constants
PROGRAM_LOCATION = os.path.abspath(os.path.dirname(os.path.realpath(__file__)))
CONFIG_FILE = args.config
TEMPLATE_FOLDER = args.template
DIS_TEMPLATE = 'display.html'
ERR_TEMPLATE = 'error.html'

# Open config
with open(os.path.join(PROGRAM_LOCATION, CONFIG_FILE), 'r', encoding='utf8') as f:
	CONFIG = yaml.safe_load(f)

# Eat leading character in logos to preserve whitespace
CONFIG['logo'] = CONFIG['logo'][1:]
CONFIG['rootLogo'] = CONFIG['rootLogo'][1:]

# Load jinja
env = jinja2.Environment(
	loader = jinja2.FileSystemLoader(os.path.join(PROGRAM_LOCATION, TEMPLATE_FOLDER)),
	trim_blocks = True,
	lstrip_blocks = True,
	autoescape = False)

# Load ignored files/folders
ig = ignorelib.IgnoreFilterManager.build(
	os.path.join(PROGRAM_LOCATION, CONFIG['websiteDir']),
	global_patterns=CONFIG['ignored'])

##
# Stuff that needs to be done each time
##

def generate(path):
	# Set cwd
	relPath = os.path.relpath(path, os.path.join(PROGRAM_LOCATION, CONFIG['websiteDir']))
	CONFIG['cwd'] = '/' + relPath.replace('\\', '/').strip('.') # Windows normalisation

	# Apply yaml templates
	config = templateConfig()

	# Get folder and remove ignored files
	folders, files = next(os.walk(path))[1:]
	files = [file for file in files if not ig.is_ignored(os.path.join(CONFIG['cwd'][1:], file))]
	folders = [folder for folder in folders if not ig.is_ignored(os.path.join(CONFIG['cwd'][1:], folder))]

	# Don't render if nothing in dir
	if not folders and not files:
		return

	# Set embed description for directories
	if not files and config['cwd'] != '/':
		config['embedDesc'] = f'Directory Listing for {config["cwd"]}'

	external = []
	# Disable display for forced-list directories
	if config['cwd'] not in config['forceDir']:
		# Put together file displays
		txtFile, mdFile, htmlFile, yamlFile = ingestFiles(files, path, ['.txt', '.md', '.html', '.yaml'])
		config['txt'] = txtFile
		config['md'] = mdFile
		config['html'] = htmlFile

		# Add external links
		if 'links.yaml' in yamlFile:
			f = yaml.safe_load(yamlFile['links.yaml'])
			if f:
				external = f

		# Process markdown files
		for key in config['md'].keys():
			config['md'][key] = config['md'][key].replace('# ', '## ') # Demote headers
			config['md'][key] = markdown.markdown(config['md'][key])

		# Generate embed
		desc = {**config['md'], **config['html']}
		if desc:
			# Use first p as description
			for key, value in desc.items():
				if '<p' in value:
					bs = BeautifulSoup(value, features='html.parser')
					if bs.p:
						p = str(bs.p)
						p = re.sub('<br.?>', '&#x0A;', p)
						p = re.sub('<.*?>', '', p)
						config['embedDesc'] = p
						break
			# Use first valid image as embed
			for key, value in desc.items():
				if '<img' in value:
					bs = BeautifulSoup(value, features='html.parser')
					if bs.img:
						img = bs.img.attrs['src']
						if img.startswith('/'):
							img = config['url'] + img
						if img.endswith('.png') or img.endswith('.jpeg') or img.endswith('.jpg'):
							print(img)
							config['embedImage'] = img
						break

		# Remove displayed files from display
		ingested = list(txtFile.keys()) + list(mdFile.keys()) + list(htmlFile.keys()) + list(yamlFile.keys())
		files = [file for file in files if file not in ingested]

	# Put together ls output
	folders = [{'name':folder, 'href':folder+'/'} for folder in folders] # Add trailing slash
	files = [{'name':file, 'href':file} for file in files]
	ls = folders + files + external
	config['ls'] = sorted(ls, key=lambda d: d['name'])

	# Render page
	render(os.path.join(path, 'index.html'), DIS_TEMPLATE, config)
	print(f'generated {CONFIG["cwd"]}')

	# Recurse
	for folder in folders:
		generate(os.path.join(path, folder['name']))

# Parse the yaml so that template variables are replaced
# This is kinda cursed and I couldn't figure out a nice way to do it both globally and recursively so it has limited depth
def templateConfig():
	config = CONFIG.copy()
	for key in CONFIG.keys():
		if isinstance(CONFIG[key], str):
			config[key] = CONFIG[key].format(**CONFIG)
		if isinstance(CONFIG[key], list):
			for i in range(len(CONFIG[key])):
				if isinstance(CONFIG[key], str):
					config[key] = CONFIG[key].format(**CONFIG)
	return config

# Construct an array of dictionaries of the files
def ingestFiles(files, path, filetypes):
	output = []
	for type in filetypes:
		ingest = [file for file in files if file.endswith(type)]
		dict = {}
		for file in ingest:
			with open(os.path.join(path, file), 'r', encoding='utf8') as f:
				contents = f.read()
			dict[file] = contents
		output.append(dict)
	return output

# Render and write the html
def render(path, template, config):
	template = env.get_template(template)
	output = template.render(**config)
	with open(path, mode='w', encoding='utf8') as f:
		f.write(output)

# Generate site
path = os.path.join(PROGRAM_LOCATION, CONFIG['websiteDir'])
generate(path)

# Generate error pages
for error in CONFIG['errorPage']:
	CONFIG['cwd'] = '?' + error['error']
	CONFIG['error'] = error
	config = templateConfig()
	render(os.path.join(path, error['error'] + '.html'), ERR_TEMPLATE, config)