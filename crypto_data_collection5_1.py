# A library to handle logging and events
import logging

# A library to load environment variables from a .env file
from dotenv import load_dotenv

# A library to connect and interact with a mySQL database
import mysql.connector

# A library to interact with the operating system
import os

# Importing the request library to make an HTTP request
import requests

# Importing the time library to handle the time delay
import time


# Load environment variables from .env file
load_dotenv()

logging.basicConfig(level=logging.INFO)

# Read environment variable
CMC_url = os.getenv("CMC_url")
CMC_api_key = os.getenv("CMC_API_KEY")
db_user = os.getenv("MYSQL_USER")
db_pass = os.getenv("MYSQL_PASSWORD")
db_host = os.getenv("MYSQL_HOST")
db_name = os.getenv("MYSQL_HOST")


# Function to get the latest cryptocurrency data from coinMarketCap API
def get_crypto_data(crypto_symbol):
    url = CMC_url
    parameters = {"symbol": crypto_symbol, "convert": "USD"}
    headers = {
        "Accepts": "application/json",
        "X-CMC_PRO_API_KEY": CMC_api_key,
    }

    try:
        response = requests.get(url, headers=headers, params=parameters)
        response.raise_for_status()  # Raise HTTPError for bad responses (4xx and 5xx)

        try:
            data = response.json()
            return data["data"][crypto_symbol]
        except KeyError as e:
            logging.error(
                f"Key error - API structure may have changed the symbol may be incorrect: {e}"
            )
            return None
        except ValueError as e:
            logging.error(f"Failed to parse JSON response: {e}")
            return None

    except requests.exceptions.HTTPError as http_err:
        logging.error(f"HTTP Error occurred: {http_err}")
    except requests.exceptions.ConnectionError as conn_err:
        logging.error(f"Connection Error occurred: {conn_err}")
    except requests.exceptions.Timeout as timeout_err:
        logging.error(f"Timeout Error occurred: {timeout_err}")
    except requests.exceptions.RequestException as req_err:
        logging.error(f"Request Error occurred: {req_err}")
    except Exception as e:
        logging.error(f"Unexpected error occurred: {e}")

    return None


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
        volume_24 = crypto_data.get("quote", {}).get("USD", {}).get("volume_24h", 0.0)
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

        insert_query = """INSERT INTO crypto_prices (name, symbol, market_cap, formatted_market_cap, price, formatted_price, volume_24, timestamp,
                        percent_change_1hr, percent_change_24hr, percent_change_7d, percent_change_30d, percent_change_60d, percent_change_90d) 
                        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"""
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
        )

        cursor.execute(insert_query, data_tuple)
        conn.commit()
        return True  # Indicate success
    except mysql.connector.Error as e:
        logging.error(f"Database error: {e}")
        return False  # Indicate failure
    finally:
        if cursor:
            cursor.close()
        if conn:
            conn.close()


def main():
    crypto_symbol = "BTC"

    while True:
        crypto_data = get_crypto_data(crypto_symbol)
        if crypto_data:
            success = store_data_in_db(crypto_data)
            if success:
                print(f"Data stored at {time.strftime('%Y-%m-%d %H:%M:%S')}")
            else:
                print(f"Failed to store data at {time.strftime('%Y-%m-%d %H:%M:%S')}")
        else:
            print("Failed to retrieve data")
        time.sleep(1)


if __name__ == "__main__":
    main()
