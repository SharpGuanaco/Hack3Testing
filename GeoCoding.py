import sys; address = " ".join(sys.argv[1:])
from geopy.geocoders import Nominatim

def main():
    geolocator = Nominatim(user_agent="WaterFinder")
    print(address)
    location = geolocator.geocode(address)
    print(location.latitude, location.longitude)

if __name__ == '__main__':
    main()