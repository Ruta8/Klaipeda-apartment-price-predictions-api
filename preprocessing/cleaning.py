import pandas as pd
import numpy as np
import datetime
from price_parser import Price


def clean_area(data: pd.DataFrame) -> pd.DataFrame:

    # "1 kambario butas Klaipėdoje, Sportininkuose, Pušyno g. +2 " >>> "Sportininkuose"
    data["area"] = data.title.str.split(",").str[1].str.split("+")
    data["area"] = [area[0].strip() if area != None else area for area in data.area]
    return data


def clean_sq_meters(data: pd.DataFrame) -> pd.DataFrame:

    # "48.00 m²" >>> 48.00
    data["sq_meters"] = data.sq_meters.str.extract("([0-9]+[,.]+[0-9]+)").astype(float)
    return data


def split_apartment_floor(data: pd.DataFrame) -> pd.DataFrame:

    # Splits e.g. "5/5 a." into two columns
    data[["apartment_floor", "total_floors"]] = data.apartment_floor.str.split(
        "/", expand=True
    )
    return data


def convert_to_numeric(data: pd.DataFrame) -> pd.DataFrame:
    data["total_floors"] = data.total_floors.str.extract("([0-9])").astype(float)
    data["apartment_floor"] = data.apartment_floor.str.extract("([0-9])").astype(float)
    data["room_count"] = data.room_count.str.extract("([0-9])").astype(float)
    return data


def clean_year_built(data: pd.DataFrame) -> pd.DataFrame:

    # "1972 m." >>> 1972.0.
    data["year_built"] = data.year_built.str.split(" ").str[0]
    data["year_built"] = data.year_built.replace(r"^\s*$", "1800", regex=True)
    data["year_built"] = data.year_built.astype(float).replace(1800, np.NaN)
    return data


def create_building_age(data: pd.DataFrame) -> pd.DataFrame:

    # Calculates building age
    now = datetime.datetime.now()
    data["building_age"] = float(now.year) - data["year_built"]
    return data


def clean_price(data: pd.DataFrame) -> pd.DataFrame:

    # "Kaina: 159 000 € (935 €/m²)" >>> 159000
    data["price"] = [Price.fromstring(str(price)).amount for price in data.price]
    data["price"] = data.price.astype(int)
    return data


def clean_scraped_data():
    data = pd.read_csv("data/scraped_data.csv")

    data = clean_area(data)
    data = clean_sq_meters(data)
    data = split_apartment_floor(data)
    data = convert_to_numeric(data)
    data = clean_year_built(data)
    data = create_building_age(data)
    data = clean_price(data)

    data.drop(["title", "link", "year_built"], axis=1, inplace=True)
    data.dropna(inplace=True)

    column_names = data.columns
    data.to_csv("data/cleaned_data.csv", sep=",", header=column_names, index=None)


if __name__ == "__main__":
    clean_scraped_data()