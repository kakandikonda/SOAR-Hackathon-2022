import googlemaps
import math
import numpy as np

gmaps = googlemaps.Client(key = "AIzaSyBZBc-Rm_vK74EW73o6DcSzPCNBCV7uwP8")

# directions_result = gmaps.directions("Novi, MI", "East Lansing, MI", mode="driving")
# print(directions_result[0]["legs"])
#Latitude is up and down
#Longitude is left and right
#raise/run = lat/lon
degreeLat = 69
degreeLon = 54.6

def LocationToLatLon(location):
    cords = gmaps.geocode(location)[0]["geometry"]["location"]
    return (cords["lat"], cords["lng"])


def LatLonAlongSlope(p1, p2, d = 300):
    p1 = (p1[0] * degreeLat, p1[1] * degreeLon)
    p2 = (p2[0] * degreeLat, p2[1] * degreeLon)
    p1 = np.array(p1)
    p2 = np.array(p2)
    v = p2 - p1
    u = v/np.linalg.norm(v) # v/magnitude of v
    cord =  p1 + (d * u)
    cord = (cord[0]/degreeLat, cord[1]/degreeLon)
    return cord


def Distance(p1, p2):
    lat1, lon1 = p1
    lat2, lon2 = p2
    R = 6371 * 10**3
    phi1 = lat1 * (math.pi/180)
    phi2 = lat2 * (math.pi/180)
    deltaPhi = (lat2 - lat1) * (math.pi/180)
    deltaLamda = (lon2 - lon1) * (math.pi/180)
    a = math.sin(deltaPhi/2) * math.sin(deltaPhi/2) + math.cos(phi1/2) * math.cos(phi2/2) * math.sin(deltaLamda/2) * math.sin(deltaLamda/2)
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))
    return (R * c)/1609

temp = input("What is your vehicles range (default: 300): ")
range = temp if temp != "" else 300
start = input("What is your starting location: ")
end = input("What is you destination: ")
# Geocoding an address
geoStart = LocationToLatLon(start)
geoEnd = LocationToLatLon(end)
distance = Distance(geoStart, geoEnd)
if distance > (range/2):
    stops = int(distance/(range/2))
    print(f"You need to take {stops} stops to go from {start} to {end}")
else:
    print(f"You dont need any stops to go from {start} to {end}")


# Look up an address with reverse geocoding
# reverse_geocode_result = gmaps.reverse_geocode((40.714224, -73.961452))
# p1 = (42.466591, -83.474701)
# p2 = (42.736980, -84.483864)
# d = Distance(p1, p2)
# print(d/1609)
# print(LatLonAlongSlope(p1, p2, 100))
# # test = input("Input a value: ")
# # dist = int(test) if test != "" else 300
# #
# # print(dist)


