A simple wrapper for the Thenmap API.


Installing
==========

.. code:: bash

  pip install thenmap


Using
=====

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
  '1780'

For more fine grained controll over the return geodata use the method get_geodata:

.. code:: python

  >>> swedish_municipalities.get_geodata(date="1975-05-03", format="topojson")
  {{u'crs': {u'type': u'name', ...}

See http://thenmap.net for more info on the API.


Developing
==========

To run tests:

.. code-block:: python

  python2 -m pytest test/*
  python3 -m pytest test/*

  
Changelog
=========

- next

  - Added tests
  - Require Shapely >= 1.7

- 1.1.0

  - Always get features from only one date. Default to current date
  - Add Dataset.info method
  - Make Python3.x compatible

- 1.0.1
  - Fixed import bug

- 1.0.0
  - First working version

