import requests
import pandas as pd
from time import sleep
import tkinter as tk
from tkinter import filedialog
from pathlib import Path


def get_address(postcode: str, huisnummer: int):
    url = f"https://api.bag.kadaster.nl/lvbag/individuelebevragingen/v2/adressen?postcode={postcode}&huisnummer={huisnummer}&exacteMatch=false&page=1&pageSize=20&inclusiefEindStatus=true"
    headers = {
    'X-Api-Key': 'l7380e3cfc716f4788beea66f144e155d9'
    }

    response = requests.request("GET", url, headers=headers).json()
    sleep(1/50)

    straat = response["_embedded"]["adressen"][0]["korteNaam"]
    huis = response["_embedded"]["adressen"][0]["huisnummer"]
    plaats = response["_embedded"]["adressen"][0]["woonplaatsNaam"]

    return straat,huis,plaats


def get_address_toevoeging(postcode: str, huisnummer: int, toevoeging: str):
    if toevoeging:
        url = f"https://api.bag.kadaster.nl/lvbag/individuelebevragingen/v2/adressen?postcode={postcode}&huisnummer={huisnummer}&huisletter={toevoeging}&exacteMatch=false&page=1&pageSize=20&inclusiefEindStatus=true"
    
    headers = {
    'X-Api-Key': 'l7380e3cfc716f4788beea66f144e155d9'
    }

    response = requests.request("GET", url, headers=headers).json()
    sleep(1/50)

    straat = response["_embedded"]["adressen"][0]["korteNaam"]
    huis = response["_embedded"]["adressen"][0]["huisnummer"]
    huisletter = response["_embedded"]["adressen"][0]["huisletter"]
    plaats = response["_embedded"]["adressen"][0]["woonplaatsNaam"]

    return straat,huis,huisletter,plaats


def convert_postcodes(dataframe: pd.DataFrame):
    """Assumes a dataframe of 3 columns. postcode -> huisnummer -> huisletter"""
    straten = []
    huisnummers = []
    toevoegingen = []
    plaatsen = []

    for row in range(len(dataframe)):
        letter = dataframe.iloc[row,2]
        if letter:
            straat,huis,huisletter,plaats = get_address_toevoeging(dataframe.iloc[row,0], dataframe.iloc[row,1], letter)

            straten.append(straat)
            huisnummers.append(huis)
            toevoegingen.append(huisletter)
            plaatsen.append(plaats)


        else:
            straat,huis,plaats = get_address(dataframe.iloc[row,0], dataframe.iloc[row,1])

            straten.append(straat)
            huisnummers.append(huis)
            toevoegingen.append(None)
            plaatsen.append(plaats)

    data = {"straat": straten,
            "huisnummer": huisnummers,
            "huisletter": toevoegingen,
            "plaats": plaatsen}
    return pd.DataFrame(data)


if __name__ == "__main__":
    root = tk.Tk()
    root.withdraw()
    data = filedialog.askopenfilename(initialdir=Path.cwd(), filetypes=[("CSV", ".csv")], title="Selecteer CSV bestand")
    res = convert_postcodes(dataframe=data)
    res.to_csv("output_postcodes.csv", index=False)