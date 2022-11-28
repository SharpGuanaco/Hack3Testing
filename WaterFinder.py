import sys; coordinates = sys.argv[1:]
import requests, math

def createURL(latitude,longitude,boxSize):
    westernLongitude = str(longitude - boxSize)
    southernLatitude = str(latitude - boxSize)
    easternLongitude = str(longitude + boxSize)
    northernLatitude = str(latitude + boxSize)
    url = "https://waterservices.usgs.gov/nwis/site/?format=rdb&bBox=" + westernLongitude + ","+ southernLatitude + ","+ easternLongitude + ","+ northernLatitude + "&siteStatus=all"
    return url

def parseData(response):
    #[Agency, Site identification number, Site name, Site type, Decimal latitude, Decimal longitude,
    # Latitude-longitude accuracy, Decimal Latitude-longitude datum, Altitude of Gage/land surface,
    # Altitude accuracy, Altitude datum, Hydrologic unit code]
    lines = response.text.split("\n")[32:]
    locations = []
    for line in lines:
        locations.append(line.split("\t"))
    for line in locations:
        print(line)
    return locations


def calculateDisance(latitude1, longitude1, latitude2, longitude2):

    y1 = float(latitude1)
    x1 = float(longitude1)
    y2 = float(latitude2)
    x2 = float(longitude2)

    R = 3958.76 # miles

    y1 *= math.pi/180.0
    x1 *= math.pi/180.0
    y2 *= math.pi/180.0
    x2 *= math.pi/180.0

    return math.acos( math.sin(y1)*math.sin(y2) + math.cos(y1)*math.cos(y2)*math.cos(x2-x1) ) * R


def sortLocations(locations,originalLatitude,originalLongitude):
    distances = [0] * len(locations)
    for i,location in enumerate(locations):
        latitude = location[4]
        longitude = location[5]
        distances[i] = calculateDisance(originalLatitude,originalLongitude,latitude,longitude)
    sortedDistancesIndex = sorted(enumerate(distances),key = lambda i: i[1])
    sortedLocations = [0]*len(locations)
    for i,sortedDistance in enumerate(sortedDistancesIndex):
        index,distance = sortedDistance
        sortedLocations[i] = [distance] + locations[index]
    return sortedLocations



def main():
    latitude = float(coordinates[0]) #vertical
    longitude = float(coordinates[1]) #horizontal
    boxSize = 1 # 111km
    locationCount = 3

    if len(coordinates) > 2:
        boxSize = float(coordinates[2])
    if len(coordinates) > 3:
        locationCount = int(coordinates[3])
    if abs(latitude) > 90:
        print ("ERROR: latitude out of bounds")
        print(latitude)
    if abs(longitude) > 180:
        print("ERROR: longitude out of bounds")
        print(longitude)

    apiURL = createURL(latitude,longitude,boxSize)

    response = requests.get(apiURL)
    locations = parseData(response)
    locations = locations[:len(locations)-1]
    sortedLocations = sortLocations(locations,latitude,longitude)

    if len(sortedLocations) > locationCount:
        for x in range(locationCount):
            print("Location " + str(x+1))
            print("Distance: " + str(sortedLocations[x][0]) + " miles")
            print("Name: " + str(sortedLocations[x][3]))
            print("Latitude: " + str(sortedLocations[x][5]))
            print("Longitude: " + str(sortedLocations[x][6]))
            print("Site Number: " + str(sortedLocations[x][2]))
            #print("Full Data: " + str(sortedLocations[x]))
    else:
        for x in range(len(sortedLocations)):
            print("Location " + str(x+1))
            print("Distance: " + str(sortedLocations[x][0]) + " miles")
            print("Name: " + str(sortedLocations[x][3]))
            print("Latitude: " + str(sortedLocations[x][5]))
            print("Longitude: " + str(sortedLocations[x][6]))
            print("Site Number: " + str(sortedLocations[x][2]))
            #print("Full Data: " + str(sortedLocations[x]))


if __name__ == '__main__':
    main()