import os
import sys

from sphinx_markdown_builder import MarkdownBuilder
from sphinx_markdown_parser.parser import MarkdownParser

# Add project root to sys.path for autodoc discoverability
sys.path.insert(0, os.path.abspath('../'))

project = 'aioa2squery'
# noinspection PyShadowingBuiltins
copyright = '2019, insurgency.gg'
author = 'hink'
extensions = [
    'sphinx.ext.autodoc',
    'sphinx.ext.coverage',
    'sphinx.ext.coverage',
    'sphinx.ext.doctest',
    'sphinx.ext.extlinks',
    'sphinx.ext.githubpages',
    'sphinx.ext.intersphinx',
    # 'sphinx.ext.linkcode',
    # 'recommonmark',
    'sphinxcontrib.programoutput',
]
extlinks = {
    'github-branch': ('https://github.com/insurgency/aioa2squery/tree/branches/%s', 'name'),
    'issue': ('https://github.com/insurgency/aioa2squery/issues/%s', 'gh-'),
    'valve-wiki': ('https://developer.valvesoftware.com/wiki/%s', 'page'),
    'wikipedia': ('https://wikipedia.org/wiki/%s', 'page'),
    'steam-app': ('https://store.steampowered.com/app/%s', 'app-id')
}
# https://github.com/NextThought/sphinxcontrib-programoutput/issues/37#issuecomment-504008704
programoutput_prompt_template = "$ a2squery query --help\n{output}"
intersphinx_mapping = {
    'py': ('https://docs.python.org/{0.major}.{0.minor}'.format(sys.version_info), None),
}
cwd = '../../'
autodoc_member_order = 'bysource'
templates_path = ['_templates']
exclude_patterns = []
html_theme = 'alabaster'
html_static_path = ['_static']
nitpicky = True
source_suffix = {
    '.rst': 'restructuredtext',
    '.md': 'markdown'
}

# Spelling: https://sphinxcontrib-spelling.readthedocs.io/en/stable/install.html#configuration

# Spell checking needs an additional module. Add it only if spell checking is requested so docs can be generated without
# it.
if 'spelling' in sys.argv:
    extensions.append('sphinxcontrib.spelling')

spelling_lang = 'en_US'


def setup(app):
    app.add_source_suffix('.md', 'markdown')
    app.add_source_parser(MarkdownParser)
