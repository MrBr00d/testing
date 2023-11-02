from geopy.geocoders import Nominatim
import pandas as pd

def adress_finder(path):
    df = pd.read_csv(path)
    nrows = len(df)

    streets_dict = df.to_dict(orient="list")
    appened_streets = []

    for item in range(nrows):
        appened_streets.append(streets_dict["Straat"][item] + "," + streets_dict["Stad"][item])
        
    loc = Nominatim(user_agent="Geopy Library")
    lats = []
    longs = []
    for item in range(0, len(appened_streets)):
        getLoc = loc.geocode(appened_streets[item])
        lat = getLoc.latitude
        long = getLoc.longitude
        lats.append(lat)
        longs.append(long)
        print(getLoc.address)
    df["Latitude"] = lats
    df["Longitude"] = longs
    df.to_csv("output.csv")

if __name__ == "__main__":
    adress_finder(input("Please enter the name of the csv file. This csv file ahs to be in the same fodler as this .py file. "))