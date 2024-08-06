# Project title: CryptoData collection and storage
#### Video Demo: <https://youtu.be/yHKT-9WEQUI>
#### Description:
Crypto Data Collector
This Python script is designed to fetch and store cryptocurrency data from the CoinMarketCap API into a MySQL database. It continuously monitors a specified cryptocurrency symbol, retrieves its latest data, and updates a database with relevant information. The script is configured to handle various types of errors gracefully and logs important events and issues.

Features
Fetch Cryptocurrency Data: Retrieves the latest market data for a specified cryptocurrency symbol using the CoinMarketCap API.
Store Data in MySQL Database: Inserts the retrieved data into a MySQL database, including details such as market cap, price, trading volume, and percent changes.
Error Handling and Logging: Handles API errors, connection issues, and JSON parsing problems, and logs errors and relevant information.

How It Works

API Request:
Uses the CoinMarketCap API to get the latest data for a given cryptocurrency symbol. The API key and endpoint URL are retrieved from environment variables.

Data Processing:
Extracts relevant data from the API response, including market cap, price, trading volume, and percentage changes over different time periods.
Formats and prepares this data for storage.

Database Interaction:
Connects to a MySQL database using credentials from environment variables.
Inserts the cryptocurrency data into the crypto_prices table, which should be pre-defined in the database schema.

Error Handling and Logging:
Uses logging to record errors and important events during data retrieval and storage processes.
Catches various exceptions related to HTTP requests and database operations.

Continuous Operation:
Runs in an infinite loop, fetching and storing data every second. This can be adjusted according to the required data retrieval frequency.

Prerequisites

Python Libraries:
requests: For making HTTP requests to the CoinMarketCap API.
mysql-connector-python: For interacting with the MySQL database.
python-dotenv: For loading environment variables from a .env file.
logging: For handling and recording log messages.

MySQL Database:
The database should be set up with a table named crypto_prices with the following structure:
CREATE TABLE crypto_prices (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(255),
    symbol VARCHAR(10),
    market_cap DECIMAL(20, 2),
    formatted_market_cap VARCHAR(50),
    price DECIMAL(20, 2),
    formatted_price VARCHAR(50),
    volume_24 DECIMAL(20, 2),
    timestamp VARCHAR(30),
    percent_change_1hr DECIMAL(5, 2),
    percent_change_24hr DECIMAL(5, 2),
    percent_change_7d DECIMAL(5, 2),
    percent_change_30d DECIMAL(5, 2),
    percent_change_60d DECIMAL(5, 2),
    percent_change_90d DECIMAL(5, 2)
);

Create a .env File:
In the root directory of your project, create a .env file with the following variables:
CMC_url= url
CMC_API_KEY = your_coinmarketcap_api_key
mysql_user = your_mysql_username
mysql_password = your_mysql_password
mysql_host = your_mysql_host
mysql_database = your_mysql_database

Notes
The script is designed to run indefinitely and will need to be stopped manually.
Modify the crypto_symbol variable in the script to monitor different cryptocurrencies.
