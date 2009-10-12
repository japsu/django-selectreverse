====================
Django selectreverse
====================

This module contains a set of helpers to reduce the number of queries needed to access m2m relations or reverse foreign key relations.

Introduction
------------

Consider a parent-child relationship building-appartements. It is created using a foreign key field to the Building model in the Appartment model.

A common pattern is to list some or all buildings and for each of the buildings list the appartments.

An example:

In the template:

	{% for building in buildinglist %}
	  <p>Building: {{ building }}</p>
	  <p>Appartments:</p>
	  <ul>
	    {% for appartment in building.appartment_set.all %}
	      <li>{{ appartment.number }}</li>
	    {% endfor %}
	  </ul>
	{% endfor %}


In the view:

	buildinglist = Building.objects.all()

The problem is that this causes an extra query for each building, when the list of appartments for each building gets loaded from the database.

Using the ReverseManager in this package, this can be reduced to only one extra query.

How ?

In the Building model, use the ReverseManager instead (or in addition to) the default manager.

	objects = ReverseManager()

In the view use the select_reverse method to prefetch the appartments:

	buildinglist = Building.objects.select_reverse({'appartments': 'appartment_set'})

The select_reverse method accepts a dictionary, mapping a reverse (or m2m) relationship to a new attribute name.

Now when retrieving the buildinglist from the database, one extra query will be performed to get the corresponding appartments. Each building will get an 'appartments' attribute, which contains a list of the corresponding appartment objects.

All we need to do to use this in the template is replace the 'building.appartment_set.all' query with a reference to the new attribute: 'building.appartments', like this:

	{% for building in buildinglist %}
	  <p>Building: {{ building }}</p>
	  <p>Appartments:</p>
	  <ul>
	    {% for appartment in building.appartments %}
	      <li>{{ appartment.number }}</li>
	    {% endfor %}
	  </ul>
	{% endfor %}

Instead of many queries, this only requires two queries, regardless of the number of buildings in the list.


API
---

The package contains a custom manager, called ReverseManager.

ReverseManager contains a custom method 'select_reverse', which accepts one argument: a dictionary mapping relationships to a new attribute name.

	buildinglist = Building.objects.select_reverse({'appartments': 'appartment_set'})

This will use one single extra query to get the appartment objects and adds to each building in the set an attribute 'appartments' which is a list of appartments, equivalent to the result of a building.appartment_set.all() query.

Mind that overriding an existing attribute name is not allowed and will raise a ImproperlyConfigured exception.

The following relationships are currently supported:

- reverse foreign key
- m2m
- reverse m2m

It is also possible to define a default mapping when defining the manager. Just pass the mapping in the manager constructor like this:

	objects = ReverseManager({'appartments': 'appartment_set'})

Now when you use Building.objects.all() or Building.objects.select_reverse(), this default mapping will be used to prefetch the objects.

Of course select_reverse() can be chained after filter(), e.g. Building.objects.filter(pk__lt=20).select_reverse().

Look at the tests for examples of m2m and reverse m2m relationships.


