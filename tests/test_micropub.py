#!/usr/bin/env python

import unittest

try:  # Python v3
    from urllib.parse import urlparse
except ImportError:
    from urlparse import urlparse

from ninka import discoverMicropubEndpoints


_url = "https://bear.im/"

class TestDiscovery(unittest.TestCase):
    def runTest(self):
        for url in ('https://bear.im/',):
            u = urlparse(url)
            r = discoverMicropubEndpoints(url)

            assert 'micropub' in r

            micropubURL = None
            for url in r['micropub']:
                micropubURL = url
                break

            assert micropubURL is not None
            assert micropubURL.scheme == u.scheme
            assert micropubURL.netloc == u.netloc
            assert micropubURL.path   == '/micropub'
