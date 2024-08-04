CoinMarketCap API Data Collector and MySQL Storage Script

Video Demo: <URL HERE>
Github and edx username: alexanderhabte5@gmail.com

Description: Overview

This is a Python script that retrieves cryptocurrency data from the CoinMarketCap API and stores it in a MySQL database. The script runs indefinitely, fetching and storing data every second.

Importing Libraries

The script starts by importing the necessary libraries:
These libraries are used for:

os: interacting with the operating system (e.g., loading environment variables)
requests: making HTTP requests to the CoinMarketCap API
time: handling time-related tasks (e.g., sleeping for a second between API requests)
mysql.connector: interacting with the MySQL database
datetime: working with dates and times (e.g., parsing timestamps from the API response)
dotenv: loading environment variables from a .env file
Loading Environment Variables

The script loads environment variables from a .env file using dotenv:
This loads variables such as the CoinMarketCap API URL, MySQL database credentials, and others.

Defining Functions

The script defines three functions:
get_crypto_data(crypto_symbol)
This function retrieves cryptocurrency data from the CoinMarketCap API for a given crypto_symbol (e.g., "BTC"). It:

Constructs the API request URL and headers
Sends a GET request to the API
Parses the response JSON data
Extracts relevant data (e.g., name, symbol, market cap, price)
Returns the extracted data as a dictionary

store_data_in_db(crypto_data)
This function stores the cryptocurrency data in a MySQL database. It:

Connects to the database using the mysql.connector library
Creates a cursor object to execute SQL queries
Extracts relevant data from the crypto_data dictionary
Formats the data for insertion into the database (e.g., converting timestamps to a compatible format)
Executes an INSERT query to store the data in the database
Commits the changes and closes the cursor and connection

main()
This is the main function that runs indefinitely. It:

Sets the crypto_symbol variable to "BTC"
Enters an infinite loop where it:
Calls get_crypto_data() to retrieve cryptocurrency data
If data is retrieved successfully, calls store_data_in_db() to store it in the database
Prints a success message with the current timestamp
Sleeps for 1 second before repeating the loop
Running the Script

The script runs the main() function if it is executed directly (i.e., not imported as a module by another script).

This ensures that the script runs indefinitely, fetching and storing cryptocurrency data every second.