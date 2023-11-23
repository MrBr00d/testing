from geopy.geocoders import Nominatim
import pandas as pd
import time
import tkinter as tk
from tkinter import filedialog

def adress_finder(path, steetname, housenumber, addition, place):
    start = time.time()
    print("start geocoding...")
    df = pd.read_csv(path, index_col=False, sep=";")
    df = df[[steetname, housenumber, addition, place]]
    nrows = len(df)

    streets_dict = df.to_dict(orient="list")
    appened_streets = []

    for item in range(nrows):
        if pd.isna(streets_dict[addition][item]):
            appened_streets.append(streets_dict[steetname][item] + " " + str(streets_dict[housenumber][item]) + ", " + streets_dict[place][item])
        else:
            appened_streets.append(streets_dict[steetname][item] + " " + str(streets_dict[housenumber][item]) + streets_dict[addition][item] + ", " + streets_dict[place][item])
            
    loc = Nominatim(user_agent="Nick van Vliet")
    lats = []
    longs = []
    failed = []
    df2 = pd.DataFrame()
    df2["Address"] = None
    print("DATA OK")
    for item in range(0, len(appened_streets)):
        try:
            getLoc = loc.geocode(appened_streets[item])
            time.sleep(1)
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
    end = time.time()
    print(f"Total runtime: {end-start}")


if __name__ == "__main__":
    try:
        root = tk.Tk()
        root.withdraw()
        data_path = filedialog.askopenfilename(filetypes=[("CSV", "*.csv")], title="Select CSV file with address info")
        root.destroy()
        adress_finder(data_path,
                    input("Please enter the name of the column containing streetnames. "),
                    input("Please enter the name of the column containing housenumber. "),
                    input("Please enter the name of the column containing addition to the housenumber (toevoeging). "),
                    input("Please enter the name of the column containing place. "))
        print("Geocoding done")
        input('press any button to close')
    except Exception as e:
        print(e)