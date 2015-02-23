import urllib
import time
import re
from math import radians, sqrt, sin, cos, atan2

f = urllib.urlopen("http://earthquake.usgs.gov/earthquakes/feed/v1.0/summary/all_month.geojson")

# constants
curr_time = time.time()
week_sec = 604800
interana_lat = 37.452443
interana_lon = -122.166165

# see http://andrew.hedges.name/experiments/haversine/
def haversine_dist (lon1, lon2, lat1, lat2):
    lon1, lon2, lat1, lat2 = map(radians, [lon1, lon2, lat1, lat2])
    dlon = lon2 - lon1
    dlat = lat2 - lat1
    a = (sin(dlat/2.))**2 + cos(lat1) * cos(lat2) * (sin(dlon/2.))**2
    return 3963 * 2 * atan2(sqrt(a), sqrt(1-a))


# regex to extract time, latitude and longitude, and magnitude
def extract_time (string):
    match = re.search(r'\"time\":(\d+)', string)
    return float(match.group(1))

def extract_lat_lon (string):
    match = re.search(r'\"coordinates\":\[(\-?\d*\.?\d*),(\-?\d*\.?\d*)', string)
    return float(match.group(1)), float(match.group(2))

def extract_mag (string):
    match = re.search(r'\"mag\":(\d*\.?\d*)', string)
    return float(match.group(1))


# find the highest mag earthquake and its distance away
def greatest_mag ():
    mag, dist, time_hr = 0, 0, 0
    for line in f:
        t = extract_time(line)
        if (curr_time - t/1000.) <= week_sec:
            lon, lat = extract_lat_lon(line)
            d = haversine_dist(interana_lon, lon, interana_lat, lat)
            if d <= 100.:
                new_mag = extract_mag(line)
                if new_mag > mag:
                    mag = new_mag
                    dist = d
                    time_hr = (curr_time - t/1000.)/3600.
    return mag, dist, time_hr

if __name__ == '__main__':
    mag, dist, time_hr = greatest_mag()
    print "There was a", str(mag), "magnitude earthquake", str(dist), "miles away", str(time_hr), "hours ago. Watch out!"
