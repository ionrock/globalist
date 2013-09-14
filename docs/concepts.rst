====================
 Globalist Concepts
====================

Globalist is meant to act as a gateway. Its role is to make an
underlying store faster by providing a consistent means of caching.

MongoDB
=======

Globalist uses MongoDB for storage. There are a few reasons for this:

 1. It is easy to store objects
 2. It is easy to scale out (add hardware)
 3. It (eventually) stores data on disk
 4. Querying is document based

MongoDB has its drawbacks as well. It is still relatively new and has
bugs. It also is somewhat immature in some areas. With that said, it
is document based, which means it can work well with HTTP and most
importantly for Globalist, HTTP caching.

Redis
=====

Redis is used for caching by default. Feel free to use any cache you'd
like. The only requirement is to provide a CacheControl_ compatible
cache store.

HTTP Caching
============

Globalist uses the HTTP caching algorithms to safely cache and
invalidate cached data.

This caching is the key concept of Globalist! The fastest database
query is the one that never happens. Globalist wants to optimize for
this use case.


Cache Invalidation
------------------

When a client talks to the globalist REST API it *must* use a
compliant HTTP cache based client. The reason being is that when any
client does an operation that changes an object, that cache entry will
be invalidated.

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
