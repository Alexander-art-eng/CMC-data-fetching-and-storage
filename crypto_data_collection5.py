from datetime import datetime

from dotenv import load_dotenv

import mysql.connector

import os

# Importing the request library to make an HTTP request
import requests

# Importing the time library to handle the time delay
import time


#Load environment variables from .env file
load_dotenv()

# Read environment variable
CMC_url = os.getenv("CMC_url")
db_user = os.getenv("mysql_user")
db_pass = os.getenv("mysql_password")
db_host = os.getenv("mysql_host")
db_name = os.getenv("mysql_database")

# Function to get the latest cryptocurrency data from coinmarketCap API
def get_crypto_data(crypto_symbol):
    url = CMC_url
    parameters = {"symbol": crypto_symbol, "convert": "USD"}
    headers = {
        "Accepts": "application/json",
        "X-CMC_PRO_API_KEY": "67a5d930-9576-47c6-8ffa-dd1418fe562b",
    }

    try:
        response = requests.get(url, headers=headers, params=parameters)
        response.raise_for_status()  # Raise HTTPError for bad responses (4xx and 5xx)

        try:
            data = response.json()
            return data["data"][crypto_symbol]
        except KeyError:
            print(
                "Key error - API structure may have changed or the symbol maybe incorrect"
            )
            return None

    except requests.exceptions.HTTPError as http_err:
        print(f"HTTP Error occurred: {http_err}")
    except requests.exceptions.ConnectionError as conn_err:
        print(f"Connection Error occurred: {conn_err}")
    except requests.exceptions.Timeout as timeout_err:
        print(f"Timeout Error occurred: {timeout_err}")
    except requests.exceptions.RequestException as req_err:
        print(f"Request Error occurred: {req_err}")

    return None


# Function to get the historical data from the API of coinmarketcap
"""def get_historical_data(crypto_symbol, start_date, end_date):
    url = "https://pro-api.coinmarketcap.com/v1/cryptocurrency/quotes/historical"
    parameters = {
        "symbol": crypto_symbol,
        "time_start": start_date,  # ISO FORMAT (8601)
        "time_end": end_date,
    }
    headers = {
        "Accepts": "application/json",
        "X-CMC_PRO_API_KEY": "67a5d930-9576-47c6-8ffa-dd1418fe562b",
    }

    try:
        response = requests.get(url, headers=headers, params=parameters)
        response.raise_for_status()  # Raise HTTPError for bad responses (4xx and 5xx)

        try:
            data = response.json()
            return data["data"][crypto_symbol]
        except KeyError:
            print("Key Error - Unable to retrieve historical data")
            return None

    except requests.exceptions.HTTPError as http_err:
        print(f"HTTP Error occurred: {http_err}")
    except requests.exceptions.ConnectionError as conn_err:
        print(f"Connection Error occurred: {conn_err}")
    except requests.exceptions.Timeout as timeout_err:
        print(f"Timeout Error occurred: {timeout_err}")
    except requests.exceptions.RequestException as req_err:
        print(f"Request Error occurred: {req_err}")

    return None"""


# Function to store the crypto data in the database
def store_data_in_db(crypto_data):
    db_config = {
        "user": db_user,
        "password": db_pass,
        "host": db_host,
        "database": db_name,
    }
    conn = None
    cursor = None
    try:
        conn = mysql.connector.connect(**db_config)
        cursor = conn.cursor()

        # Extract relevant data
        name = crypto_data.get("name", "Unknown")
        symbol = crypto_data.get("symbol", "Unknown")
        market_cap = crypto_data.get("quote", {}).get("USD", {}).get("market_cap", 0.0)
        formatted_market_cap = "${:,.2f}".format(
            market_cap if isinstance(market_cap, (int, float)) else 0
        )
        price = crypto_data.get("quote", {}).get("USD", {}).get("price", 0.0)
        formatted_price = "${:,.2f}".format(price)
        volume_24 = crypto_data.get("quote", {}).get("USD", {}).get("volume_24", 0.0)
        timestamp = (
            crypto_data.get("quote", {})
            .get("USD", {})
            .get("last_updated", "No timestamp available")
        )
        percent_change_1hr = (
            crypto_data.get("quote", {}).get("USD", {}).get("percent_change_1h", 0.0)
        )
        percent_change_24hr = (
            crypto_data.get("quote", {}).get("USD", {}).get("percent_change_24h", 0.0)
        )
        percent_change_7d = (
            crypto_data.get("quote", {}).get("USD", {}).get("percent_change_7d", 0.0)
        )
        percent_change_30d = (
            crypto_data.get("quote", {}).get("USD", {}).get("percent_change_30d", 0.0)
        )
        percent_change_60d = (
            crypto_data.get("quote", {}).get("USD", {}).get("percent_change_60d", 0.0)
        )
        percent_change_90d = (
            crypto_data.get("quote", {}).get("USD", {}).get("percent_change_90d", 0.0)
        )
        low = crypto_data.get("quote", {}).get("USD", {}).get("low", 0.0)
        high = crypto_data.get("quote", {}).get("USD", {}).get("high", 0.0)
        buy = crypto_data.get("quote", {}).get("USD", {}).get("buy", 0.0)
        sell = crypto_data.get("quote", {}).get("USD", {}).get("sell", 0.0)
        spread = crypto_data.get("quote", {}).get("USD", {}).get("spread", 0.0)

        # Convert the timestamp to a format compatible to the mysql DATETIME
        if timestamp != "No timestamp available":
            timestamp = datetime.strptime(timestamp, "%Y-%m-%dT%H:%M:%S.%fz").strftime(
                "%Y-%m-%d %H:%M:%S"
            )

        insert_query = """INSERT INTO crypto_prices (name, symbol, market_cap, formatted_market_cap, price, formatted_price, volume_24, timestamp,
                        percent_change_1hr, percent_change_24hr, percent_change_7d, percent_change_30d, percent_change_60d, percent_change_90d, 
                        low, high, buy, sell, spread) 
                        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"""
        data_tuple = (
            name,
            symbol,
            market_cap,
            formatted_market_cap,
            price,
            formatted_price,
            volume_24,
            timestamp,
            percent_change_1hr,
            percent_change_24hr,
            percent_change_7d,
            percent_change_30d,
            percent_change_60d,
            percent_change_90d,
            low,
            high,
            buy,
            sell,
            spread,
        )

        cursor.execute(insert_query, data_tuple)
        conn.commit()
    except mysql.connector.Error as e:
        print(f"Database error: {e}")
    finally:
        if cursor:
            cursor.close()
        if conn:
            conn.close()


'''''
# Function for storing the historical data into the database
def store_historical_data_in_db(historical_data, symbol):
    db_config = {
        "user": "root",
        "password": "sA!EXAyLP2@m59x%GPE9",
        "host": "127.0.0.1",
        "database": "crypto_data",
    }

    conn = None
    cursor = None

    try:
        conn = mysql.connector.connect(**db_config)
        cursor = conn.cursor()
        for data_point in historical_data["data"]:
            insert_query = """INSERT INTO historical_crypto_prices (symbol, price, market_cap, volume_24h, timestamp)
                            VALUES (%s, %s, %s, %s, %s)"""

            data_tuple = (
                symbol,
                data_point["price"],
                data_point["market_cap"],
                data_point["volume_24h"],
                data_point["timestamp"],
            )
            cursor.execute(insert_query, data_tuple)
            conn.commit()
    except mysql.connector.Error as e:
        print(f"Database error {e}")
    finally:
        if cursor:
            cursor.close()
        if conn:
            conn.close()''' ""


def main():
    crypto_symbol = "BTC"

    """historical_data = get_historical_data(
        crypto_symbol, start_date="2023-10-10", end_date="2024-01-01"
    )
    if historical_data:
        store_historical_data_in_db(historical_data, crypto_symbol)
        print("Historical data was successfully stored in the database")
    else:
        print("No historical data was found for the given symbol")"""

    while True:
        crypto_data = get_crypto_data(crypto_symbol)
        if crypto_data:
            store_data_in_db(crypto_data)
            print(f"Data stored at {time.strftime('%Y-%m-%d %H:%M:%S')}")
        else:
            print("Failed to retrieve data")
        time.sleep(1)


if __name__ == "__main__":
    main()
