import yfinance as yf
from yahoofinancials import YahooFinancials
import pendulum
import mplfinance as mpf
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
import json
import requests
from bs4 import BeautifulSoup
import streamlit as st

# Function to create the form
def user_input():
    st.title("Stock Ticker Input Form")
    
    # Text input for API key
    api_key = st.text_input("Enter your API key", type="password")  # type="password" hides the input

    # Text input for Stock ticker
    ticker = st.text_input("Enter the stock ticker")

    # Display the input values
    if st.button("Submit"):
        if api_key and ticker:
            #st.write(f"API Key: {api_key}")
            st.write(f"Stock Ticker: {ticker}")
        else:
            st.write("Please fill in both fields.")

    return api_key, ticker

# if 'api_key' in st.session_state and 'ticker' in st.session_state:
#     api_key = st.session_state.api_key
#     ticker = st.session_state.ticker
    
file_paths = ['income_statement.json', 'balance_sheet.json', 'cash_flow.json']

def process_api_request(api_key, ticker):
    #Income Statement
    financial_statement = "INCOME_STATEMENT"
    url_income_statement = "https://www.alphavantage.co/query?function="+ financial_statement + "&symbol="+ ticker + "&apikey="+ alpha_vantage_api_key
    
    #Balance Sheet
    financial_statement = "BALANCE_SHEET"
    url_balance_sheet = "https://www.alphavantage.co/query?function="+ financial_statement + "&symbol="+ ticker + "&apikey="+ alpha_vantage_api_key
    
    #Cash Flow
    financial_statement = "CASH_FLOW"
    url_cash_flow = "https://www.alphavantage.co/query?function="+ financial_statement + "&symbol="+ ticker + "&apikey="+ alpha_vantage_api_key
    
    # URLs and file paths
    urls = [url_income_statement, url_balance_sheet, url_cash_flow]
    
    # Dictionary to store the URL to file path mapping
    url_to_file_path = dict(zip(urls, file_paths))
    
    data_income_statement, data_balance_sheet, data_cash_flow = {}, {}, {}
    
    # Save JSON responses to files
    for url, file_path in url_to_file_path.items():
      response = requests.get(url)
      json_data = response.json()
    
      with open(file_path, 'w') as file:
          json.dump(json_data, file, indent=4)  # Correctly dumping JSON data
    
      print(f"JSON data from {url} has been written to {file_path}")
      # Assign data to respective variables
      if "INCOME_STATEMENT" in url:
          data_income_statement = json_data
      elif "BALANCE_SHEET" in url:
          data_balance_sheet = json_data
      elif "CASH_FLOW" in url:
          data_cash_flow = json_data
    return (data_income_statement, data_balance_sheet, data_cash_flow)

def main():
    # Call the user input function
    api_key, ticker = user_input()

    # Add a separator
    st.write("---")

    # Check if the necessary values are provided
    if api_key and ticker:
        # Add a button to trigger fetching financial statements
        if st.button("Fetch Financial Statements"):
            data_income_statement, data_balance_sheet, data_cash_flow = process_api_request(api_key, ticker)
            
            if data_income_statement:
                st.write("Income Statement:")
                st.json(data_income_statement)
            else:
                st.error("Failed to fetch Income Statement data.")
            
            if data_balance_sheet:
                st.write("Balance Sheet:")
                st.json(data_balance_sheet)
            else:
                st.error("Failed to fetch Balance Sheet data.")
            
            if data_cash_flow:
                st.write("Cash Flow Statement:")
                st.json(data_cash_flow)
            else:
                st.error("Failed to fetch Cash Flow Statement data.")
    else:
        st.info("Please enter the API key and stock ticker above.")

# Entry point of the application
if __name__ == "__main__":
    main()
