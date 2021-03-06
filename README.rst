===========
 Globalist
===========

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


RESTful HTTP API
================

Globalist has a web API that makes an effort to map as closely to the
MongoDB API as possible. There are some use cases such as GridFS and
tailable cursors that are not implemented.

Globalist doesn't try to support more being is that if
you need to use extremely large chunks of data, then you are unlikely
to be able to cache that data anyway. For example, if I had a
collection full of 2 GB documents, I would need 2 GB to cache each
document. In this case, Globalist is not a viable option.



MongoDB, Redis and HTTP
=======================

Data is stored in MongoDB, data is cached in Redis and the API is
implemented over HTTP.

It is assumed that the user will configure and set up the necessary
databases.
