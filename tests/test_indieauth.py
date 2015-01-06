#!/usr/bin/env python

import unittest
from ninka import discoverAuthEndpoints, validateAuthCode
from urlparse import ParseResult


_url = "https://bear.im/"

class TestDiscovery(unittest.TestCase):
    def runTest(self):
        r = discoverAuthEndpoints(_url)

        assert 'authorization_endpoint' in r

        authURL = None
        for url in r['authorization_endpoint']:
            authURL = url
            break

        assert authURL is not None
        assert authURL.scheme == 'https'
        assert authURL.netloc == 'indieauth.com'
        assert authURL.path   == '/auth'
