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

# Text input for Stock ticker
#ticker = st.text_input("Enter the stock ticker")

# Function to create the form
def user_input(ticker):
    #st.title("Stock Ticker Input Form")
    # Display the input values
    if st.button("Submit"):
        if ticker:
            #st.write(f"API Key: {api_key}")
            st.write(f"Stock Ticker: {ticker}")
            st.write(yf.Ticker(ticker).info["longBusinessSummary"])
        else:
            st.write("Please fill in ticker.")

# Text input for API key
#api_key = st.text_input("Enter your API key", type="password")  # type="password" hides the input

@st.cache_data
def process_api_request(api_key, ticker):
#if st.button("Fetch Financial Statements"):
    file_paths = ['income_statement.json', 'balance_sheet.json', 'cash_flow.json']
    #Income Statement
    financial_statement = "INCOME_STATEMENT"
    url_income_statement = "https://www.alphavantage.co/query?function=" + financial_statement + "&symbol="+ ticker + "&apikey="+ api_key

    #Balance Sheet
    financial_statement = "BALANCE_SHEET"
    url_balance_sheet = "https://www.alphavantage.co/query?function=" + financial_statement + "&symbol="+ ticker + "&apikey="+ api_key
    
    #Cash Flow
    financial_statement = "CASH_FLOW"
    url_cash_flow = "https://www.alphavantage.co/query?function=" + financial_statement + "&symbol="+ ticker + "&apikey="+ api_key
    
    # URLs and file paths
    urls = [url_income_statement, url_balance_sheet, url_cash_flow]
    
    data = {
    'income_statement': None,
    'balance_sheet': None,
    'cash_flow': None
        }   


    # Send GET requests and store data
    for url, file_path in zip(urls, file_paths):
        response = requests.get(url)
        json_data = response.json()

        # Save JSON response to file
        with open(file_path, 'w') as file:
            json.dump(json_data, file, indent=4)

        # Assign data to respective variables
        if 'INCOME_STATEMENT' in url:
            data['income_statement'] = json_data
        elif 'BALANCE_SHEET' in url:
            data['balance_sheet'] = json_data
        elif 'CASH_FLOW' in url:
            data['cash_flow'] = json_data

    # Return the fetched data
    #st.write(data)
    return data #['income_statement'], data['balance_sheet'], data['cash_flow']

def clean_data(data):
    quarterannual_income = [(report["fiscalDateEnding"],
                            report["netIncome"],
                            report["grossProfit"],
                            report["totalRevenue"],
                            report["costofGoodsAndServicesSold"],
                            report["operatingIncome"],
                            report["sellingGeneralAndAdministrative"],
                            report["researchAndDevelopment"],
                            report["operatingExpenses"],
                            report["interestExpense"],
                            report["depreciation"],
                            report["incomeBeforeTax"],
                            report["incomeTaxExpense"]
                        #) for report in loaded_data['income']["annualReports"]]
                        ) for report in data['income_statement']["annualReports"]]


    quarterannual_balance = [(report["fiscalDateEnding"],
                            report["commonStockSharesOutstanding"],
                            report["shortLongTermDebtTotal"],
                            report["cashAndCashEquivalentsAtCarryingValue"]
                    #) for report in loaded_data['balance']["annualReports"]]
                            ) for report in data['balance_sheet']["annualReports"]]

    quarterannual_cash = [(report["fiscalDateEnding"],
                        report["operatingCashflow"],
                        report["capitalExpenditures"]
                    #) for report in loaded_data['cashflow']["annualReports"]]
                            ) for report in data['cash_flow']["annualReports"]]


    df_income_statement = pd.DataFrame(quarterannual_income, columns =
                    ["fiscalDateEnding",
                    "netIncome",
                    "grossProfit",
                    "totalRevenue",
                    "costofGoodsAndServicesSold",
                    "operatingIncome",
                    "sellingGeneralAndAdministrative",
                    "researchAndDevelopment",
                    "operatingExpenses",
                    "interestExpense",
                    "depreciation",
                    "incomeBeforeTax",
                    "incomeTaxExpense"])


    df_balance_statement = pd.DataFrame(quarterannual_balance, columns = ["fiscalDateEnding",
                                                                        "commonStockSharesOutstanding",
                                                                        "shortLongTermDebtTotal",
                                                                        "cashAndCashEquivalentsAtCarryingValue"
                                                                        ])

    df_cashflow_statement = pd.DataFrame(quarterannual_cash, columns = ["fiscalDateEnding",
                                                                        "operatingCashflow",
                                                                        "capitalExpenditures"])

    # Sort the DataFrame by the fiscalDateEnding column

    df_sorted_income_statement = df_income_statement.sort_values(by="fiscalDateEnding")
    df_sorted_balance_statement = df_balance_statement.sort_values(by="fiscalDateEnding")
    df_sorted_cashflow_statement = df_cashflow_statement.sort_values(by="fiscalDateEnding")

    #Currently python is viewing the values as string; hence need to convert values to integers
    columns_to_convert = [
                        "netIncome",
                        "grossProfit",
                        "totalRevenue",
                        "costofGoodsAndServicesSold",
                        "operatingIncome",
                        "sellingGeneralAndAdministrative",
                        "researchAndDevelopment",
                        "operatingExpenses",
                        "interestExpense",
                        "depreciation",
                        "incomeBeforeTax",
                        "incomeTaxExpense"]

    #In case of nan values, fill it as integer 0
    for col in columns_to_convert:
        df_sorted_income_statement[col] = pd.to_numeric(df_sorted_income_statement[col], errors='coerce').fillna(0).astype(int)

    columns_to_convert = ["commonStockSharesOutstanding", "shortLongTermDebtTotal", "cashAndCashEquivalentsAtCarryingValue"]

    for col in columns_to_convert:
        df_sorted_balance_statement[col] = pd.to_numeric(df_sorted_balance_statement[col], errors='coerce').fillna(0).astype(int)

    columns_to_convert = ["operatingCashflow", "capitalExpenditures"]

    for col in columns_to_convert:
        df_sorted_cashflow_statement[col] = pd.to_numeric(df_sorted_cashflow_statement[col], errors='coerce').fillna(0).astype(int)

    # Merge the two dataframes on the fiscal dates
    merged_df = pd.merge(df_sorted_cashflow_statement, df_sorted_income_statement, on="fiscalDateEnding")
    merged_df = pd.merge(merged_df, df_sorted_balance_statement, on="fiscalDateEnding")

    return merged_df

def ocf_netincome_revenue(merged_df):
    categories = merged_df["fiscalDateEnding"]

    ocf_millions = merged_df["operatingCashflow"]/1000000
    netincome_millions = merged_df["netIncome"]/1000000
    totalrevenue_millions = merged_df["totalRevenue"]/1000000

    # Set the width of the bars
    bar_width = 0.35

    x = np.arange(len(categories))  # the label locations
    width = 0.35  # the width of the bars
    # multiplier = 0

    # Create figure and axes
    fig, ax = plt.subplots()

    # Create bar plots
    rects1 = ax.bar(x - width, ocf_millions, width, label='Operating Cash Flow')
    rects2 = ax.bar(x, netincome_millions, width, label='Net Income')
    rects3 = ax.bar(x + width, totalrevenue_millions, width, label='Total Revenue')

    # Add labels and title
    ax.set_ylabel('Amount In Millions')
    ax.set_title('Operating Cash Flow, Net Income & Total Revenue For Each Year ')
    ax.set_xticks(x)
    ax.set_xticklabels(categories, rotation=90)
    ax.legend()

    st.pyplot(fig)

def main():
    st.title("Stock Ticker Input Form")
    # Text input for Stock ticker
    ticker = st.text_input("Enter the stock ticker")

    # # Call the user input function
    # ticker = user_input()
    user_input(ticker)
    
    # Text input for API key
    api_key = st.text_input("Enter your API key", type="password")  # type="password" hides the input

    if st.button("Fetch Financial Statements"):
        if len(api_key)==16 and len(ticker)>2:
            #data_income_statement, data_balance_sheet, data_cash_flow 
            data = process_api_request(api_key, ticker)
            #target_string = "Thank you for using Alpha Vantage"
            if "annualReports" in data["income_statement"]:
                merged_df = clean_data(data)
                ocf_netincome_revenue(merged_df)
            elif "Information" in data["income_statement"]:
                st.write(data["income_statement"]["information"])
            else:
                st.write(data)

        else:
            st.write("Please enter a valid ticker and API key")


# Entry point of the application
if __name__ == "__main__":
    main()
