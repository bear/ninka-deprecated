# -*- coding: utf-8 -*-
"""
:copyright: (c) 2014-2016 by Mike Taylor
:license: MIT, see LICENSE for more details.

Micropub Tools
"""

import requests
from bs4 import BeautifulSoup, SoupStrainer

try:  # Python v3
    from urllib.parse import urlparse, urljoin
except ImportError:
    from urlparse import urlparse, urljoin

import ronkyuu


_html_parser = 'lxml'   # 'html.parser', 'lxml', 'lxml-xml', 'html5lib'

def setParser(htmlParser='html5lib'):
    global _html_parser
    _html_parser = htmlParser


# find an endpoint
# look in headers for given domain for a HTTP Link header
# if not found, look for an HTML <link> element in page returned from domain given

def discoverEndpoint(domain, endpoint, content=None, look_in={'name': 'link'}, test_urls=True, validateCerts=True):
    """Find the given endpoint for the given domain.
    Only scan html element matching all criteria in look_in.

    optionally the content to be scanned can be given as an argument.

    :param domain: the URL of the domain to handle
    :param endpoint: list of endpoints to look for
    :param content: the content to be scanned for the endpoint
    :param look_in: dictionary with name, id and class_. only element matching all of these will be scanned
    :param test_urls: optional flag to test URLs for validation
    :param validateCerts: optional flag to enforce HTTPS certificates if present
    :rtype: list of endpoints
    """
    if test_urls:
        ronkyuu.URLValidator(message='invalid domain URL')(domain)

    if content:
        result = {'status':   requests.codes.ok,
                  'headers':  None,
                  'content':  content
                  }
    else:
        r = requests.get(domain, verify=validateCerts)
        result = {'status':   r.status_code,
                  'headers':  r.headers
                  }
        # check for character encodings and use 'correct' data
        if 'charset' in r.headers.get('content-type', ''):
            result['content'] = r.text
        else:
            result['content'] = r.content

    for key in endpoint:
        result.update({key: set()})
    result.update({'domain': domain})

    if result['status'] == requests.codes.ok:
        if 'link' in r.headers:
            all_links = r.headers['link'].split(',', 1)
            for link in all_links:
                if ';' in link:
                    href, rel = link.split(';')
                    url = urlparse(href.strip()[1:-1])
                    if url.scheme in ('http', 'https') and rel in endpoint:
                        result[rel].add(url)

        all_links = BeautifulSoup(result['content'], _html_parser, parse_only=SoupStrainer(**look_in)).find_all('link')
        for link in all_links:
            rel = link.get('rel', None)[0]
            if rel in endpoint:
                href = link.get('href', None)
                if href:
                    url = urlparse(href)
                    if url.scheme == '' or url.netloc == '':
                        url = urlparse(urljoin(domain, href))
                    if url.scheme in ('http', 'https'):
                        result[rel].add(url)
    return result

def discoverMicropubEndpoints(domain, content=None, look_in={'name': 'link'}, test_urls=True, validateCerts=True):
    """Find the micropub for the given domain.
    Only scan html element matching all criteria in look_in.

    optionally the content to be scanned can be given as an argument.

    :param domain: the URL of the domain to handle
    :param content: the content to be scanned for the endpoint
    :param look_in: dictionary with name, id and class_. only element matching all of these will be scanned
    :param test_urls: optional flag to test URLs for validation
    :param validateCerts: optional flag to enforce HTTPS certificates if present
    :rtype: list of endpoints
    """
    return discoverEndpoint(domain, ('micropub',), content, look_in, test_urls, validateCerts)

def discoverTokenEndpoints(domain, content=None, look_in={'name': 'link'}, test_urls=True, validateCerts=True):
    """Find the token for the given domain.
    Only scan html element matching all criteria in look_in.

    optionally the content to be scanned can be given as an argument.

    :param domain: the URL of the domain to handle
    :param content: the content to be scanned for the endpoint
    :param look_in: dictionary with name, id and class_. only element matching all of these will be scanned
    :param test_urls: optional flag to test URLs for validation
    :param validateCerts: optional flag to enforce HTTPS certificates if present
    :rtype: list of endpoints
    """
    return discoverEndpoint(domain, ('token_endpoint',), content, look_in, test_urls, validateCerts)
