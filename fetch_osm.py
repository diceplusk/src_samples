#---------------------------------------------------
# Open Street Map (OSM)
#---------------------------------------------------
# - https://www.openstreetmap.org/about
# - to get the map image from OSM
# - It is possible to plot GPS trajectories on the map.
# Bounding Box:
# http://wiki.openstreetmap.org/wiki/Bounding_Box
# bbox = left,bottom,right,top
# bbox = min Longitude , min Latitude , max Longitude , max Latitude"
# Scale (Zoom Level):
# http://wiki.openstreetmap.org/wiki/Zoom_levels
# small value (fine granularity) to high (coarse)
#---------------------------------------------------
#!/usr/bin/env python



from urllib2 import urlopen # to fetch data via http
from PIL import Image # to open image
from cStringIO import StringIO # to read downloaded file; n/a in Python 3



def get_osm_img(self, minlon, minlat, maxlon, maxlat, scale):
	"""Get an OpenStreetMap export image file via http"""

	# Export Image formats
	im_format = "png"
	# im_format = "jpg"
	# im_format = "svg"
	# im_format = "pdf"

	# Access URL
	URL = "http://parent.tile.openstreetmap.org/cgi-bin/export?" + \
	      "bbox=%f,%f,%f,%f" % (minlon, minlat, maxlon, maxlat) + \
	      ";scale=%d" % scale + \
	      ";format=%s" % im_format

	print "Fetching map... "
	tries = 0
	url = None
	while tries < 10:
		tries += 1
		print "Try %d..." % tries

		try:
			# open an openstreetmap export file via http
			url = urlopen(URL)

		except:
			time.sleep(5)
			continue

		else:
			print "Map successfully downloaded."
			break

	if url is None:
		print "Failed to download a map."

	else:

		# Save the map
		file = StringIO(url.read())
		img = Image.open(file)
		img = img.convert("L") # change to gray-scale color
		img.show()
		img.save("img.png")

		return url


