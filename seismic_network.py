#!/usr/bin/env python

import numpy as np

from mpl_toolkits.basemap import pyproj
from shapely.geometry import MultiPoint, Point


# WGS84 datum (Lat/Lon geographic coordinate system)
wgs84 = pyproj.Proj(init='EPSG:4326')

# Lambert Azimuthal Equal Area (laea)  projection
pj_laea = pyproj.Proj(proj='laea', lat_0=90, lon_0=0, x_0=0, y_0=0,
                      ellps='WGS84', datum='WGS84', units='m', no_defs=True)


class SeismicNetwork(object):
    def __init__(self, net_lats, net_lons):
        poly_x, poly_y = pyproj.transform(wgs84, pj_laea, net_lons, net_lats)
        self.polygon = MultiPoint(zip(poly_x, poly_y)).convex_hull

    def contains(self, lat, lon):
        x, y = pyproj.transform(wgs84, pj_laea, lon, lat)
        point = Point(x, y)
        if self.polygon.contains(point):
            return True
        else:
            return False

    def inside_network(self, epi_lats, epi_lons):
        """
        This function returns epicenter coordinates located inside a seismic
        station network. The point-in-polygon problem is solved based on ray
        casting method.

        :param epi_lats: Latitudes of earthquake epicenters.
        :param epi_lons: Longitudes of earthquake epicenters.

        :type epi_lats: numpy.array, list/tuple or scalar
        :type epi_lons: numpy.array, list/tuple or scalar

        :returns:
            Epicenter coordinates located within network. The first and second
            columns are latitude and longitude, respectively.
        :rtype: numpy.array
        """
        epi_x, epi_y = pyproj.transform(wgs84, pj_laea, epi_lons, epi_lats)
        r = []
        for i, (x, y) in enumerate(zip(epi_x, epi_y)):
            epicenter = Point(x, y)
            if epicenter.within(self.polygon):
                r.append((epi_lats[i], epi_lons[i]))
        return np.array(r)
