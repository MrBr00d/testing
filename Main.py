from geopy.geocoders import Nominatim
import pandas as pd

df = pd.read_csv("Map1.csv")
nrows = len(df)

streets_dict = df.to_dict(orient="list")
# streets_dict
streets_dict["Straat"]
streets_dict["Stad"]
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
    print("Latitude = ", lat)
    print("Longitude = ", long)
    print(getLoc.address, "\n")
    lats.append(lat)
    longs.append(long)

df["Latitude"] = lats
df["Longitude"] = longs

df.head()
    