ninka
=====

認可 ninka - permission, license

Python package to help working with IndieAuth.

Roadmap
=======
Working
* IndieAuth tools

Pending
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
Python v2.6+ but see requirements.txt for a full list

Installing the latest version of Requests and it's OAuth plugin now requires
pyOpenSSL which will require compiling of source libs. You may need to have
installed the -dev package for the version of Python you are working with.

For testing we use [httmock](https://pypi.python.org/pypi/httmock/) to mock
the web calls.
