# -*- coding: utf-8 -*-
"""
:copyright: (c) 2014-2016 by Mike Taylor
:license: MIT, see LICENSE for more details.

IndieAuth Toolkit
"""

import requests
from bs4 import BeautifulSoup, SoupStrainer

try:  # Python v3
    from urllib.parse import urlparse, parse_qs, ParseResult
except ImportError:
    from urlparse import urlparse, parse_qs, ParseResult

import ronkyuu


_html_parser = 'lxml'   # 'html.parser', 'lxml', 'lxml-xml', 'html5lib'

def setParser(htmlParser='html5lib'):
    global _html_parser
    _html_parser = htmlParser


# find authorization endpoint
# look in headers for given domain for a HTTP Link header
#   Link:<https://indieauth.com/auth>; rel="authorization_endpoint"
#   Link:<https://tokens.oauth.net/token>; rel="token_endpoint"
#   Link:<https://aaronparecki.com/api/post>; rel="micropub"
#
# if not found, look for an HTML <link> element in page returned from domain given
#   <link rel="authorization_endpoint" href="https://indieauth.com/auth">
#   <link rel="token_endpoint" href="https://tokens.oauth.net/token">
#   <link rel="micropub" href="https://aaronparecki.com/api/post">

def discoverAuthEndpoints(authDomain, content=None, look_in={'name': 'link'}, test_urls=True, validateCerts=True, headers={}):
    """Find the authorization or redirect_uri endpoints for the given authDomain.
    Only scan html element matching all criteria in look_in.

    optionally the content to be scanned can be given as an argument.

    :param authDomain: the URL of the domain to handle
    :param content: the content to be scanned for the authorization endpoint
    :param look_in: dictionary with name, id and class_. only element matching all of these will be scanned
    :param test_urls: optional flag to test URLs for validation
    :param validateCerts: optional flag to enforce HTTPS certificates if present
    :param headers: optional headers to send with any request
    :rtype: list of authorization endpoints
    """
    if test_urls:
        ronkyuu.URLValidator(message='invalid domain URL')(authDomain)

    if content:
        result = {'status':   requests.codes.ok,
                  'headers':  None,
                  'content':  content
                  }
    else:
        r = requests.get(authDomain, verify=validateCerts, headers=headers)
        result = {'status':   r.status_code,
                  'headers':  r.headers
                  }
        # check for character encodings and use 'correct' data
        if 'charset' in r.headers.get('content-type', ''):
            result['content'] = r.text
        else:
            result['content'] = r.content

    result.update({'authorization_endpoint': set(), 'redirect_uri': set(), 'authDomain': authDomain})

    if result['status'] == requests.codes.ok:
        if 'link' in r.headers:
            all_links = r.headers['link'].split(',', 1)

            for link in all_links:
                if ';' in link:
                    link_parts = link.split(';')
                    for s in link_parts[1:]:
                        if 'rel=' in s:
                            href = link_parts[0].strip()
                            rel  = s.strip().replace('rel=', '').replace('"', '')
                            break
                    url = urlparse(href[1:-1])

                    if url.scheme in ('http', 'https') and rel in ('authorization_endpoint', 'redirect_uri'):
                        result[rel].add(url)

        all_links = BeautifulSoup(result['content'], _html_parser, parse_only=SoupStrainer(**look_in)).find_all('link')
        for link in all_links:
            rel = link.get('rel', None)[0]

            if rel in ('authorization_endpoint', 'redirect_uri'):
                href = link.get('href', None)
                if href:
                    url = urlparse(href)

                    if url.scheme in ('http', 'https'):
                        result[rel].add(url)
    return result

def validateAuthCode(code, redirect_uri, client_id, state=None, validationEndpoint='https://indieauth.com/auth', headers={}):
    """Call authorization endpoint to validate given auth code.

    :param code: the auth code to validate
    :param redirect_uri: redirect_uri for the given auth code
    :param client_id: where to find the auth endpoint for the given auth code
    :param state: state for the given auth code
    :param validationEndpoint: URL to make the validation request at
    :param headers: optional headers to send with any request
    :rtype: True if auth code is valid
    """
    payload = {'code':         code,
               'redirect_uri': redirect_uri,
               'client_id':    client_id,
              }
    if state is not None:
        payload['state'] = state

    authURL = None
    authEndpoints = discoverAuthEndpoints(client_id, headers=headers)
    for url in authEndpoints['authorization_endpoint']:
        authURL = url
        break
    if authURL is not None:
        validationEndpoint = ParseResult(authURL.scheme, authURL.netloc, authURL.path, '', '', '').geturl()

    r = requests.post(validationEndpoint, verify=True, data=payload, headers=headers)
    result = { 'status':  r.status_code,
               'headers': r.headers
             }
    if 'charset' in r.headers.get('content-type', ''):
        result['content'] = r.text
    else:
        result['content'] = r.content
    if r.status_code == requests.codes.ok:
        result['response'] = parse_qs(result['content'])

    return result
