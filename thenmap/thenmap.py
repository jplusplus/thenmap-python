# coding: utf-8
""" Thenmap API wrapper. Note that geoanalysis in Python
is slow. For anything but very basic use cases, you probably
want to use e.g. C++ with CGAL
"""

import requests
from shapely.geometry import shape, Point
from collections import Iterable
from six import string_types
from datetime import datetime


def point_from_coordinates(input_):
    """ Factory method for Points """
    if isinstance(input_, Point):
        return input_

    if isinstance(input_, tuple):
        t = input_

    elif isinstance(input_, string_types):
        for sep in [",", ";", "|"]:
            if len(input_.split(sep)) in range(2, 3):
                t = input_.split(sep)

    elif isinstance(input_, Iterable):
        # Strings are iterable in Python 3,
        # so this must come after string check
        t = (input_)

    else:
        raise Exception("Invalid coordinates: %s" % input_)

    return Point(tuple(float(x) for x in t))


def point_in_polygon(point, polygon):
    """ Check if a point is in a polygon """
    pnt = point_from_coordinates(point)
    polygon = shape(polygon['geometry'])
    return polygon.contains(pnt)


class Dataset(object):
    """Represents a Thenmap dataset, e.g. countries of the world
    """

    def __init__(self, api, id_, label=None, date=None):
        self.api = api
        self.id = id_
        if label is not None:
            self.label = label
        else:
            label = id_
        if date is None:
            date = datetime.now().isoformat().split("T")[0]
        self.date = date

    def _fetch(self, date=None, module="info", params={}):
        """Generic method for fetching any data from any modul"""
        if date is None:
            date = self.date
        fragments = [self.api.VERSION, self.id, module, date]

        url = self.api.URL % "/".join(fragments)

        paramstr = "&".join("%s=%s" % (k, v)
                            for k, v in params.items())

        if len(paramstr):
            url += "?%s" % paramstr

        res = requests.get(url)
        return res.json()[module]

    def get_geodata(self, date=None,
                    format="geojson", properties={},
                    language=None):
        """Get geodata for a certain date, or all dates
        as either geojson or topojson
        """
        return self._fetch(date=date,
                           module="geo",
                           params={"format": format,
                                   "geo_props": "|".join(properties),
                                   "geo_lang": language,
                                   "geo_flatten_props": True,
                                   })

    def get_info(self, date=None):
        """Get info. `date` does nothing here,
        but is forwarded for consistency.
        """
        return self._fetch(date=date,
                           module="info")

    def get_data(self, date=None, properties=[], language="en"):
        """Get properties from the data module.

        Available properties varyby dataset (such as `capital`),
        but at least `name` is always available.
        """
        return self._fetch(date=date,
                           module="data",
                           params={"data_props": "|".join(properties),
                                   "data_lang": language})

    @property
    def info(self):
        return self.get_info()

    @property
    def geojson(self):
        """Return geojson, for the active date
        (defaults to the current date
        """
        return self.get_geodata(date=self.date, format="geojson")

    @property
    def topojson(self):
        """Return topojson, for the active date
        (defaults to the current date
        """
        return self.get_geodata(date=self.date, format="topojson")

    def in_which(self, coordinate, date=None):
        """ Find out in wich polygon a coordinate is"""
        polygons = self.get_geodata(date=date)
        for feature in polygons['features']:
            if point_in_polygon(coordinate, feature):
                return feature["properties"]["id"]
        return None

    def __repr__(self):
        return "<Dataset: %s (%s)>" % (self.id, self.label)


class Thenmap(object):
    """Represents a connection to the Thenmap API"""

    VERSION = "v1"
    URL = "http://api.thenmap.net/%s"

    def __init__(self):
        pass

    @property
    def datasets(self):
        """ List of all available datasets.

        This is hardcoded for now. A method for listing datasets
        is available in v2 of the API, but that version is still beta.
        """
        datasets = [
            ("fi-8", "Finnish municipalities"),
            ("ch-8", "Swiss municipalities"),
            ("no-7", "Norwegian municipalities"),
            ("dk-7", "Danish municipalities"),
            ("se-7", "Swedish municipalities"),
            ("se-4", "Swedish counties"),
            ("us-4", "US states"),
            ("gl-7", "Municipalities of Greenland"),
            ("world-2", "Countries of the world")]
        return [Dataset(self, x[0], label=x[1]) for x in datasets]

    def __getitem__(self, key):
        """ Expose datasets with bracket notation """
        try:
            return list(filter(lambda x: x.id == key, self.datasets)).pop()
        except IndexError:
            raise IndexError("No such dataset. \
Check Thenmap.dataset for avilable id's.")

    def __repr__(self):
        return "<Thenmap API version %s>" % (self.VERSION)


if __name__ == "__main__":
    print("This module is only intended to be called from other scripts.")
    import sys
    sys.exit()
