import os

from documentation.conf import *

# Add project root to sys.path for autodoc discoverability
sys.path.insert(0, os.path.abspath('../'))

project = 'aioa2squery'
cwd = '../../'
exclude_patterns = []

# Extension Settings

# See: https://github.com/NextThought/sphinxcontrib-programoutput/issues/37#issuecomment-504008704
programoutput_prompt_template = "$ a2squery query --help\n{output}"

# Spelling: https://sphinxcontrib-spelling.readthedocs.io/en/stable/install.html#configuration
# Spell checking needs an additional module. Add it only if spell checking is requested so docs can be generated without
# it.
if 'spelling' in sys.argv:
    extensions.append('sphinxcontrib.spelling')

spelling_lang = 'en_US'
