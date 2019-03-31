# -*- coding: utf-8 -*-
__url__ = "https://github.com/intelligent-agent/toggle"

from ._version import get_versions
__long_version__ = get_versions()['version']
try:
  __version__ = __long_version__.split('+')[0] + '-' + __long_version__.split('+')[1].split('.')[0]
except:
  __version__ = __long_version__.split('+')[0]
finally:
  del get_versions
