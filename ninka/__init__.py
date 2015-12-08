# -*- coding: utf-8 -*-
"""
:copyright: (c) 2014-2015 by Mike Taylor
:license: MIT, see LICENSE for more details.
"""

__author__       = 'bear (Mike Taylor)'
__email__        = 'bear@bear.im'
__copyright__    = 'Copyright (c) 2014-2015 by Mike Taylor'
__license__      = 'MIT'
__version__      = '0.3.2'
__url__          = 'https://github.com/bear/ninka'
__download_url__ = 'https://pypi.python.org/pypi/ninka'
__description__  = "Indieauth Toolkit"

from indieauth import discoverAuthEndpoints, validateAuthCode
from micropub import discoverMicropubEndpoints, discoverTokenEndpoints
