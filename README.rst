https://paste.yougov.net/LCtax

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


MongoDB, Redis and HTTP
=======================

Globalist uses some technologies you can tweak to support its
operation.

Data is stored in MongoDB, data is cached in Redis and the API is
implemented over HTTP.


Cache Invalidation
==================

The key is the caching. When a client talks to the globalist REST API
it *must* use a compliant HTTP cache based client. The reason being is
that when any client does an operation that changes an object, that
cache entry will be invalidated.

Below is a simple diagram of how Globalist starts caching requests. ::

  +--------+   	       	   +--------+
  |        |  cache        |        |
  | client +--------+ 	   | client |
  |        |   set  |      |        |
  +----+---+ 	    |  	   +----+---+
       |       	    |	       	|
       | GET	    |		| GET (cached)
       |	    |		|
       |	    |		|
  +----+--------+   |  	  +-----+----+
  |             |   |     |          |
  |  Globalist  |   +----->  Redis   |
  |             |         |          |
  +-------^-----+	  +----------+
	  |
	  |
	  | DB Read
	  |
    	  |
    +-----+-----+
    |  MongoDB  |
    +-----------+


The first client makes a GET request. It caches the response according
to HTTP caching rules. The cache on the is configured to use a Redis
store for its storage. The second client, that is also configured to
use the same Redis store, makes a request for the same resource, it is
provided the result immediately from the Redis cache.

Here is a diagram of what happens when a client updates a resource and
another client tries to GET the same resource. ::


  +--------+
  |    	   |   		cache delete
  | client +------------------------------------+
  |    	   |  		      			|
  +--+-----+		      			|
     |	  		      			|
     |	  		      			|
     | PUT		      			|
     |			      			|
     |			      			|
  +--V--------+	update 	+-----------+	  +-----V-----+
  |	      +--------->     	    |	  |	      |
  | Globalist |	       	|  MongoDB  |	  +   Redis   |
  |	      <---------+	    |	  |	      |
  +---^-------+	 read  	+-----------+	  +-----^---^-+
      |						|   |
      | GET (after cache miss)                  |   |
      |						|   |
  +---+----+					|   |
  |    	   |	       	 cache miss		|   |
  | client +------------------------------------+   |
  |	   |					    |
  +---+----+					    |
      |			 cache set     	       	    |
      +---------------------------------------------+




In this scenario the first client makes an update to a resource. Since
the update is a PUT, it will see if that value is in the cache and
delete it since it is invalid now. The second client, upon making a
request to the resource will check the cache and see it doesn't
exist. At that point the client will perform a GET and cache the
result.

The key is that as long as all clients are updating the cache
properly, then each client will be reading the from the cache a
majority of the time. The use case where this fails is when a resource
is constantly changing.


Why MongoDB / Redis?
====================

The choice to use MongoDB is because it is easy to map objects to the
database. It has indexes that can be used in query responses and it
provides an infrastructure for scaling.

Redis is a well known cache that also allows caching objects. A user
can then decide whether to cache a web request or an actual object if
need be.

It is assumed that the user will configure and set up the necessary
databases.

RESTful API
===========

Globalist has a web API that maps as closely to the MongoDB API as
possible. There are some use cases such as GridFS and tailable cursors
that are not implemented. The reason being is that if you need to use
extremely large chunks of data, then you are unlikely to be able to
cache that data anyway. For example, if I had a collection full of 2
GB documents, I would need 2 GB to cache each document. In this case,
Globalist is not a viable option.
