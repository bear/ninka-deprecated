#!/usr/bin/env python

import unittest
from ninka import discoverMicropubEndpoints, discoverTokenEndpoints
from urlparse import ParseResult


_url = "https://bear.im/"

class TestDiscovery(unittest.TestCase):
    def runTest(self):
        r = discoverMicropubEndpoints(_url)

        assert 'micropub' in r

        micropubURL = None
        for url in r['micropub']:
            micropubURL = url
            break

        assert micropubURL is not None
        assert micropubURL.scheme == 'https'
        assert micropubURL.netloc == 'bear.im'
        assert micropubURL.path   == '/micropub'
