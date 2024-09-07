#!/usr/bin/env python3
'''
Terminal Static Site Generator
'''
import yaml
import jinja2
import os
import ignorelib

#todo: make these flags?
PROGRAM_LOCATION = os.path.abspath(os.path.dirname(os.path.realpath(__file__)))
CONFIG_FILE = 'config.yaml'
TEMPLATE_FOLDER = './templates'
HEAD_TEMPLATE = 'headers.html'
ROOT_TEMPLATE = 'root.html'
DIR_TEMPLATE = 'directory.html'
DIS_TEMPLATE = 'display.html'

# Open config
with open(os.path.join(PROGRAM_LOCATION, CONFIG_FILE), 'r', encoding='utf8') as f:
	config = yaml.safe_load(f)

# Config added/edited at runtime
config['cwd'] = '/'
# Eat leading character in logos to preserve whitespace
config['logo'] = config['logo'][1:]
config['rootLogo'] = config['rootLogo'][1:]

# Load jinja
env = jinja2.Environment(
	loader = jinja2.FileSystemLoader(os.path.join(PROGRAM_LOCATION, TEMPLATE_FOLDER)),
	trim_blocks = True,
	lstrip_blocks = True,
	autoescape = False)

# Load ignored files/folders
ig = ignorelib.IgnoreFilterManager.build(
	os.path.join(PROGRAM_LOCATION, config['websiteDir']),
	global_patterns=config['ignored'])

##
# Stuff that needs to be done each time
##

def render(path):
	# Get folder and remove ignored files
	folders, files = next(os.walk(path))[1:]
	files = [file for file in files if not ig.is_ignored(file)]
	folders = [folder for folder in folders if not ig.is_ignored(folder)]

	# Apply yaml templates
	for key in config.keys():
		try:
			config[key] = config[key].format(**config)
		except: # Go into arrays too
			for i in range(len(config[key])):
				config[key][i] = config[key][i].format(**config)

	# Render page
	template = env.get_template(ROOT_TEMPLATE) # figure out how to switch template
	output = template.render(**config)

	# Write out to file
	with open(os.path.join(path, 'index.html'), mode='w', encoding='utf8') as f:
		f.write(output)

def ls():

# should these be in one function? cant imagine being called twice
def txt():

def md():

def html():

path = os.path.join(PROGRAM_LOCATION, config['websiteDir'], '.'+config['cwd'])
render(path)