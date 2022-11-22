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
temp = input("What is your vehicles range (default: 300): ")
range = int(temp) if temp != "" else 300
range *= .7
range = int(range)


def LocationToLatLon(location):
    cords = gmaps.geocode(location)[0]["geometry"]["location"]
    return (cords["lat"], cords["lng"])


def LatLonAlongSlope(p1, p2, d = range):
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


def AllStops(start, end):
    route = gmaps.directions(start, end)
    latlon = []
    for i in route[0]["legs"][0]["steps"]:
        latlon.append((i["end_location"]["lat"], i["end_location"]["lng"]))
    return latlon


def Routing(start, end):
    # stops = [start] #create an array for stops
    # distance = Distance(start, end)
    # num_stops = int(distance/range)
    # print(num_stops)
    # while num_stops > 0:
    #     next_coord = LatLonAlongSlope(stops[-1], end)
    #     arr = gmaps.reverse_geocode(next_coord)
    #     for i in arr:
    #         print(i)
    #     # if "lake" not in gmaps.reverse_geocode(next_coord):
    #     stops.append(next_coord)
    #     num_stops -= 1
    # stops.append(end)
    # return stops
    distance = Distance(start, end)
    num_stops = int(distance / range)
    route = AllStops(start, end)
    stops = [start]
    #while i < len(route)
    # while dist from one latlon - next < range
    # if check next
    # first get all major stops around manuvers
    l = len(route)
    i = 0
    while i < l:
        while i < l and Distance(stops[-1], route[i]) < range:
            i += 1
        if i < l:
            stops.append(route[i])
        i += 1
    # filter list for outliers and add new stops accordingly
    i = 0
    while i < len(stops) - 1:
        if Distance(stops[i], stops[i + 1]) > range:
            stop = LatLonAlongSlope(stops[i], stops[i + 1], int(range * .7))
            stops.insert(i + 1, stop)
        i += 1
    stops.append(end)
    return stops

def ConvertLatLon(cord):
    position = gmaps.reverse_geocode(cord)
    if len(position) > 0:
        return position[0]["formatted_address"]
    else:
        return cord


start = input("What is your starting location: ")
end = input("What is you destination: ")
# Geocoding an address
geoStart = LocationToLatLon(start) #getting lat/lon of start coord
geoEnd = LocationToLatLon(end) # getting lat/long of end coord
# distance = Distance(geoStart, geoEnd) #get the dist between the 2
# if distance > (range):
#     stops = int(distance/(range))
#     print(f"You need to take {stops} stops to go from {start} to {end}")
# else:
#     print(f"You dont need any stops to go from {start} to {end}")


# Look up an address with reverse geocoding
# reverse_geocode_result = gmaps.reverse_geocode((40.714224, -73.961452))
# print(reverse_geocode_result[0])
# p1 = (42.466591, -83.474701) # novi
# p2 = (42.736980, -84.483864)
# d = Distance(p1, p2)
# print(d)
# print(LatLonAlongSlope(p1, p2, 100))
cords = Routing(geoStart, geoEnd)
route = []
for cord in cords:
    route.append(ConvertLatLon(cord))

print(route)


# test = gmaps.directions("Novi", "Chicago")
# for i in test[0]["legs"][0]["steps"]:
#     print(i["end_location"]["lat"], i["end_location"]["lng"])