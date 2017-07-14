A simple wrapper for the Thenmap API.

Installing
==========

.. code:: bash

  pip install thenmap

Installing
==========

.. code:: python

  >>> from thenmap import Thenmap

  >>> api = Thenmap()
  >>> swedish_municipalities = api["se-7"]
  >>> swedish_municipalities.geojson  # defaults to current local date
  {{u'crs': {u'type': u'name', ...}

  >>> swedish_municipalities.date = "1975-05-03"
  >>> swedish_municipalities.geojson
  {{u'crs': {u'type': u'name', ...}

  >>> swedish_municipalities.in_which("13.46,59.38")
  1780

For more fine grained controll over the return geodata use the method get_geodata:

  >>> swedish_municipalities.get_geodata(date="1975-05-03", format="topojson")
  {{u'crs': {u'type': u'name', ...}


See http://thenmap.net for more info on the API.