[![Downloads](https://img.shields.io/pypi/v/ninka.svg)](https://pypi.python.org/pypi/ninka/)
[![Circle CI](https://circleci.com/gh/bear/ninka.svg?style=svg)](https://circleci.com/gh/bear/ninka)
[![CodeCov](http://codecov.io/github/bear/ninka/coverage.svg?branch=master)](http://codecov.io/github/bear/ninka)
[![Requirements Status](https://requires.io/github/bear/ninka/requirements.svg?branch=master)](https://requires.io/github/bear/ninka/requirements/?branch=master)

認可 ninka - permission, license

Python package to assist working with IndieAuth.

* IndieAuth tools
* MicroPub support

See the examples/ directory for sample command line tools.

Contributors
============
* bear (Mike Taylor)

IndieAuth
=========
discoverAuthEndpoints()
-----------------------
Find the authorization or redirect_uri endpoints for the given authDomain.

validateAuthCode()
------------------
Call authorization endpoint to validate given auth code.

Requires
========
Python v2.7+ but see requirements.txt for a full list
