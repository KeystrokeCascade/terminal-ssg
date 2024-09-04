#!/usr/bin/env python3
'''
Terminal Static Site Generator
'''
import yaml
import jinja2
import os

PROGRAM_LOCATION = os.path.abspath(os.path.dirname(os.path.realpath(__file__)))
HTML_TEMPLATE = 'template.html'

with open(os.path.join(PROGRAM_LOCATION, 'config.yaml'), 'r', encoding='utf8') as f:
	config = yaml.safe_load(f)

# Config added/edited at runtime
config['cwd'] = '/'
config['logo'] = config['logo'][1:]
config['rootLogo'] = config['rootLogo'][1:]

# Jinja stuff here

print(config)
print(config['prompt'].format(**config))
print(config['rootLogo'].format(**config))