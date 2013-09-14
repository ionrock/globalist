=================
 Getting Started
=================

Globalist needs two primary services, MongoDB for storage and Redis
for caching.

Take a look at the MongoDB getting started guide `here
<http://docs.mongodb.org/manual/tutorial/getting-started/>`_. You can
get started with Redis `here <http://redis.io/topics/quickstart>`_.

We'll assume that both Redis and MongoDB are running locally at the
default locations.


Installing Globalist
====================

It is a good idea to use virtualenv_ when trying out python
projects. ::

  $ mkdir globalist-test
  $ cd globalist-test
  $ virtualenv .
  $ source bin/activate

You can download and install Globalist via PyPI using pip_. ::

  $ pip install globalist

From there you can start up the globalist server. ::

  $ bin/globalist

Globalist will be running on port 5000.


Adding a Document
=================

To add a document, use the Globalist client: ::

  >>> from globalist.client import GlobalistClient
  >>> client = GlobalistClient('http://localhost:5000')
  >>> result = client.post('mydb', 'foo_collection', {'hello': 'world'})
  >>> print(result.location)
   http://localhost:5000/mydb/foo_collection/18019874039847
