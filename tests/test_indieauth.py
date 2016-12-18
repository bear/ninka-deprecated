#!/usr/bin/env python

import unittest

from ninka import discoverAuthEndpoints


class TestDiscovery(unittest.TestCase):
    def runTest(self):
        for url in ('https://bear.im', ):
            r = discoverAuthEndpoints(url)
            assert 'authorization_endpoint' in r

            authURL = None
            for endpoint_url in r['authorization_endpoint']:
                authURL = endpoint_url
                break

            assert authURL is not None
            assert authURL.scheme == 'https'
