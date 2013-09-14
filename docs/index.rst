.. Globalist documentation master file, created by
   sphinx-quickstart on Sat Sep 14 10:11:58 2013.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

=======================================
 Welcome to Globalist's documentation!
=======================================

Globalist is a horrible idea to make a fast place for global storage.

As developers we are told globals are bad. In largely distributed
systems it is imperative that data be immutable and procedures be side
effect free if there is any hope to create a performant system. A
system must be stateless in order to scale.

The thing is that we are kidding ourselves! There is always a state
that needs to be stored. Whether it is an async system that is able to
take a snapshot of the current stack or a database, we keep this data
somewhere that eventually becomes a bottleneck.

The solution for many scaling problems involve caching. We cache
database requests, memoize functions and use HTTP caching to make our
services seem faster. Yet, caching is a hard problem, especially
when you need reasonably current data. Invalidating the cache and
communicating that invalidation to clients is a hard problem that
makes caching a difficult problem.

So, we know that global data, in some form or another, is a necessary
evil. We also know caching works to speed things up, but invalidating
that cache can be difficult. Finally, we know that we should aim for
typical distributed techniques such as sharding and stateless nodes in
order to scale up an application. With all that in mind, globalist is
an attempt to provide a reasonable solution to a distributed data
store that does caching well.

Contents:

.. toctree::
   :maxdepth: 2

   concepts
   gettingstarted



Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`
