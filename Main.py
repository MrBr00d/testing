from geopy.geocoders import Nominatim
import pandas as pd
import time

def adress_finder(path, steetname, housenumber, addition, place):
    print("This program makes the following assumption: \n")
    print("- all locations are in the city of Den Haag. \n")
    input("Press any button to conttinue...")
    df = pd.read_csv(path, index_col=False)
    df = df[[steetname, housenumber, addition, place]]
    nrows = len(df)

    streets_dict = df.to_dict(orient="list")
    appened_streets = []

    for item in range(nrows):
        if pd.isna(streets_dict["toevoeging"][item]):
            appened_streets.append(streets_dict["straatnaam"][item] + " " + str(streets_dict["huisnummer"][item]) + ", " + streets_dict["plaats"][item])
        else:
            appened_streets.append(streets_dict["straatnaam"][item] + " " + str(streets_dict["huisnummer"][item]) + streets_dict['toevoeging'][item] + ", " + streets_dict["plaats"][item])
            
    loc = Nominatim(user_agent="Nick van Vliet")
    lats = []
    longs = []
    failed = []
    df2 = pd.DataFrame()
    df2["Address"] = None
    for item in range(0, len(appened_streets)):
        try:
            getLoc = loc.geocode(appened_streets[item])
            lats.append(getLoc.latitude)
            longs.append(getLoc.longitude)
            print(getLoc.address)
            df2.loc[len(df2)] = [appened_streets[item]]
        except:
            failed.append(appened_streets[item])
    df2["Latitude"] = lats
    df2["Longitude"] = longs
    print("The following addresses were not found \n")
    print(failed)
    df2.to_csv("output.csv", index=False)
    input("Press any button to close...")

if __name__ == "__main__":
    start = time.time
    adress_finder(input("Please enter the name of the csv file. This csv file ahs to be in the same fodler as this .py file "),
                   input("Please enter the name of the column containing streetnames. "),
                   input("Please enter the name of the column containing housenumber. "),
                   input("Please enter the name of the column containing addition to the housenumber (toevoeging). "),
                   input("Please enter the name of the column containing place. "))
    end = time.time
    print(end-start)