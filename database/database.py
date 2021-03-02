import psycopg2
import pandas as pd
import os
from dotenv import load_dotenv

# pabaigti dokumentuoti update_database()

load_dotenv()

def connect_to_database() -> psycopg2.extensions.connection:
    """ Initiates connection with remote Heroku database.
    """

    connection = psycopg2.connect(
        database=os.getenv("DB"),
        user=os.getenv("DB_USER"),
        password=os.getenv("DB_PASSWORD"),
        host=os.getenv("DB_HOST"),
        port=os.getenv("DB_PORT")
    )

    return connection


def create_tables_in_database() -> None:
    """ Creates empty apartment table in the database.
    """

    connection = connect_to_database()
    cursor = connection.cursor()

    try:
        cursor.execute('''
        CREATE TABLE apartments(
        id SERIAL PRIMARY KEY,
        room_count INT,
        sq_meters REAL,
        apartment_floor INT, 
        area VARCHAR(100), 
        total_floors INT, 
        building_age INT, 
        predicted_price REAL
        );
        ''')
    except:
        raise

    connection.commit()
    cursor.close()

def insert_into_apartments(dataframe: pd.DataFrame) -> None:
    """Converts given dataframe into list_of_tuples and then loops over the tuples to insert them into the database.
    """

    connection = connect_to_database()
    cursor = connection.cursor()

    records = dataframe.to_records(index=False)
    list_of_tuples = list(records)

    for row in list_of_tuples:
        (room_count, sq_meters, apartment_floor, area, total_floors, building_age, predicted_price) = row
        query = (
            f"INSERT INTO apartments (room_count, sq_meters, apartment_floor, area, total_floors, building_age, predicted_price) VALUES ('{room_count}', '{sq_meters}', '{apartment_floor}', '{area}', '{total_floors}', '{building_age}', '{predicted_price}');")
        try:
            cursor.execute(query)
        except:
            raise


    connection.commit()
    cursor.close()

def update_database(input, prediction):  
    """Takes raw input from app.py POST method and connects it with price prediction. 

    :param input: raw input from app.py POST method
    :type input: 
    :param prediction: price prediction for an apartment
    :type prediction: 
    """
    input["predicted_price"] = pd.Series(prediction)

    try:
        create_tables_in_database()
    except:
        insert_into_apartments(input)