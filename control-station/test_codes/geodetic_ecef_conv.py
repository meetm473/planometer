import math
import numpy as np

def gps_to_ecef(lat, lon, alt):
	"""
		Converts GPS coordinates into ECEF coordinate frame

		Parameters
		----------
		* lat: float: Latitude of the point in degs
		* lon: float: Longitude of the point in degs
		* alt: float: Altitude of the point in degs

		Returns
		-------
		x,y,z coordinates of the point in ECEF coordinate frame
	"""
	rad_lat = lat * (math.pi / 180.0)
	rad_lon = lon * (math.pi / 180.0)

	a = 6378137.0
	finv = 298.257223563
	f = 1 / finv
	e2 = 1 - (1 - f) * (1 - f)
	v = a / math.sqrt(1 - e2 * math.sin(rad_lat) * math.sin(rad_lat))

	x = (v + alt) * math.cos(rad_lat) * math.cos(rad_lon)
	y = (v + alt) * math.cos(rad_lat) * math.sin(rad_lon)
	z = (v * (1 - e2) + alt) * math.sin(rad_lat)

	return x, y, z

def gps_to_enu(ref_coords, point_coords):
	"""
		Converts GPS coordinates into ENU coordinate frame

		Parameters
		----------

		* ref_coords: tuple: 1x3 size tuple consisting of the GPS coordinates (deg,deg,m) of reference point.
		* point_coords: tuple: 1x3 size tuple consisting of GPS coordinates (deg,deg,m) of the point of interest.

		Returns
		-------
		x,y,z coordinates of the point wrt reference point in ENU coordinate frame
	"""
	rad_lat = ref_coords[0] * (math.pi / 180.0)
	rad_lon = ref_coords[1] * (math.pi / 180.0)

	rot_mat = np.array([[-math.sin(rad_lon), math.cos(rad_lon), 0],
						[-math.sin(rad_lat)*math.cos(rad_lon), -math.sin(rad_lat)*math.sin(rad_lon), math.cos(rad_lat)],
						[math.cos(rad_lat)*math.cos(rad_lon), math.cos(rad_lat)*math.sin(rad_lon), math.sin(rad_lat)]])

	ref_ecef = np.array(gps_to_ecef(ref_coords[0], ref_coords[1], ref_coords[2]))
	point_ecef = np.array(gps_to_ecef(point_coords[0], point_coords[1], point_coords[2]))

	return rot_mat @ (point_ecef - ref_ecef)

def calc_area(pts):
	"""
		Calculates the area defined by a convex polygon formed by the points in the clockwise direction.

		Parameters
		----------

		* pts : list of tuples : List of GPS coordinates (lat-deg, lon-deg, alt-m) of the points forming the polygon in
		a list. The first point is considered as the reference point. 

		Returns
		--------

		Area enclosed by the polygon in sq. m.
	"""
	triangle_coords = []

	for i in range(1, len(pts)):
		triangle_coords.append(tuple(gps_to_enu(pts[0], pts[i])))

	area = 0

	for i in range(0, len(triangle_coords)-1):
		area = area + 0.5*np.linalg.norm(np.cross(triangle_coords[i], triangle_coords[i+1]))
	
	return area


pts = [ (12.837747, 80.136509, 15),
		(12.837745, 80.136680, 15),
		(12.837577, 80.136680, 15),
		(12.837577, 80.136508, 15)
		]

pts_test1 = [ (12.838213639809869, 80.13742363644306, 6),
			  (12.838316938506967, 80.13731835973662, 6),
			  (12.838206448126842, 80.13721978855287, 6)
			]

pts_test1_1 = [ (12.8381966, 80.1374473, 6),
			  (12.8382253, 80.1374791, 6),
			  (12.8383551, 80.1375928, 6)
			]


pts_test2 = [ (12.837996796488122, 80.13761328688672, 6),
			  (12.838456133460289, 80.13764750825891, 6),
			  (12.838427216387503, 80.1361121093599, 6),
			  (12.838077986861459, 80.1361121093599, 6)
			]

print(calc_area(pts_test1_1))

