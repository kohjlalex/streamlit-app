#from functions import display_datetime, write_pdf, create_zip, fetch_and_process_pdf, updated_on, split_into_columns, create_df,input_uens_ui, filter_dataframe
#from constants import pdf_links, pdf_url, items

#import libraries
import pytz
import os
import requests
import pdfplumber
import pandas as pd
import streamlit as st
import re
from datetime import datetime
import zipfile
import pytz

from pytz import timezone

#from constants import pdf_links, pdf_url, base_url

import streamlit as st

st.set_page_config(page_title="MOM Company Info Scraper", page_icon="👷‍♂️")\

st.title("PDF and Web Scraper for (MOM) background checks on companies")
st.markdown(
    """This tool scrapes various MOM websites and online pdfs for background checks on Companies of interest."""
)

    # # Download and store PDFs
    # for link, filename in pdf_links:
    #     download_pdf(link, "downloads/" + filename)

pdf_links = [
        (
            "https://www.mom.gov.sg/orca/list-of-companies-with-demerits",
            "list-of-companies-with-demerits.pdf",
        ),
        (
            "https://www.mom.gov.sg/-/media/mom/documents/safety-health/reports-stats/stop-work-orders.pdf",
            "stop-work-orders.pdf",
        ),
        (
            "https://www.mom.gov.sg/-/media/mom/documents/safety-health/reports-stats/list-of-companies-under-bus.pdf",
            "list-of-companies-under-bus.pdf",
        ),
    ]       

pdf_url = "https://www.mom.gov.sg/orca/list-of-companies-with-demerits"

base_url = "https://www.mom.gov.sg/orca/api/v2/GetIndividualCompany?q={UENNAME}%2C&_=1715326178538"

items = [
        "Number of Fatal Cases = 0",
        "Work Injury Compentation Permanent Injury = 0",
        "NOT Under SWO",
        "NOT Under BUS"
    ]

# Function to display the current date and time
def display_datetime():
        # Get the Singapore Time Zone
        sgt = pytz.timezone("Asia/Singapore")
        global current_datetime
        current_datetime = datetime.now(sgt).strftime("%Y-%m-%d %H:%M:%S")
        print("current_datetime")
        st.write("Current Date and Time:", current_datetime)
        
# Function to download a PDF file from a given URL
def write_pdf(url, filename):
    response = requests.get(url)

    # directory = os.path.dirname(filename)
    # if not os.path.exists(directory):
    #     os.makedirs(directory)

    with open(filename, "wb") as pdf_file:
        pdf_file.write(response.content)
    # st.success(f"Downloaded {filename} successfully!")
    

def create_zip(): 
    #Create a zip file containing all PDFs
    #current_datetime = current_datetime.replace('/', ':')
    zip_filename = current_datetime + "_all_pdfs" + ".zip"
    try:
        #with zipfile.ZipFile("downloads/" + zip_filename, "w") as zipf:
        with zipfile.ZipFile(zip_filename, "w") as zipf:
            for _, filename in pdf_links:
                zipf.write(
                    #"downloads/" + filename, arcname=current_datetime + "_" + filename
                    filename, arcname=current_datetime + "_" + filename
                )
    except Exception as e:
        st.error(f"Error occurred while creating zip file: {e}")

    # Provide a button to download the zip file
    try:
        # with open("downloads/" + zip_filename, "rb") as zip_file:
        with open(zip_filename, "rb") as zip_file:     
            zip_data = zip_file.read()

        st.download_button(
            label="Download All PDFs (Demerit Points, SWOs, BUS)",
            data=zip_data,
            file_name=zip_filename,
            mime="application/zip",
        )
    except FileNotFoundError:
        st.error("Error: Zip file not found.")
        
# if st.button("Fetch and Process PDF"):

def fetch_and_process_pdf(pdf_url):
    if pdf_url:
        try:
            # Make a GET request to fetch the PDF file
            response = requests.get(pdf_url)
            if response.status_code == 200:
                # Process the PDF file
                # Save the downloaded PDF file
                with open("downloaded_file.pdf", "wb") as f:
                    f.write(response.content)

                # Variable to store all pages' text
                all_text = ""

                # Open the downloaded PDF file
                with pdfplumber.open("downloaded_file.pdf") as pdf:
                    # Extract text from each page
                    for page in pdf.pages:
                        text = page.extract_text()
                        # Append the text of each page to the variable
                        all_text += text + "\n"  # Add a newline for separation

                # Find the index of the first instance of "\ncompany"
                index_company = all_text.find("\ncompany")

                # Extract the text after the first instance of "\ncompany"
                if index_company != -1:
                    text_after_company = all_text[
                        index_company + len("\ncompany") :
                    ].strip()
                    global lines_after_company
                    lines_after_company = text_after_company.split("\n")
            return (lines_after_company)
        except Exception as e:
            st.error(f"An error occurred: {e}")

def updated_on(lines_after_company):
# Regular expression pattern to match "Updated on <Date>"
    pattern = r"Updated on \d{2} [A-Za-z]{3} \d{4}"

    # Initialize variables to store the updated string and the string containing "Updated on <Date>"
    updated_data = []
    updated_on_string = None

    # Loop through each string in the data
    for item in lines_after_company:
        # Search for the pattern in the current string
        match = re.search(pattern, item)

        # If the pattern is found, save it to updated_on_string and remove it from the original string
        if match:
            updated_on_string = match.group(0)
            item = re.sub(pattern, "", item)

        # Append the updated string to the list
        updated_data.append(item)

    return updated_data

    # Display the output
    st.write(updated_on_string)                    

def split_into_columns(updated_data):
    split_list = []
    # Flatten the nested list using list comprehension
    # flattened_list = [string for sublist in nested_list for string in sublist]
    for string in updated_data:
        split_string = string.split(" ")  # Split by space
        # Check if the split string contains at least 5 elements
        if len(split_string) >= 5:
            first_column = split_string[1]
            second_column = " ".join(
                split_string[2:-3]
            )  # Join the second to second-last elements
            second_last_column = split_string[
                -2
            ]  # Second last column is the second-last element
            last_column = split_string[
                -1
            ]  # Last column is the last element
            split_list.append(
                [
                    first_column,
                    second_column,
                    second_last_column,
                    last_column,
                ]
            )
        else:
            # Handle the case where the string doesn't contain enough elements
            split_list.append([string])
            # print(f"Skipping string: {string}. Not enough elements to split into 5 columns.")
    return split_list

# Create a DataFrame


def create_df(updated_data):
    global df
    st.write("The table below allows users to interact with (eg sort, download) the information from the pdf https://www.mom.gov.sg/orca/list-of-companies-with-demerits")
    df = pd.DataFrame(
        split_into_columns(updated_data),
        columns=[
            "UEN",
            "Name of company",
            "Demerit points accumulated by company",
            "Debarment phase and period",
        ],
    )

    df.dropna(how="any", axis=0, inplace=True)
    df.reset_index(drop=True, inplace=True)

    # Display the output
    st.write(df)
    return df

def input_uens_ui():
    # Create a text input box for the user to enter strings
    st.text("Enter your list of UENs (separated by commas) below:")
    uenname_input_text = st.text_area("Input", height=5, key='uennames')
    if uenname_input_text != "":
        # Split the input text by newline to get a list of strings
        uen_name_list = [x.strip() for x in uenname_input_text.split(",")]
        #uen_name_list = uenname_input_text.strip().split(",")
        #st.write(uen_name_list)
        #uen_name_list = [
        #    uen_name for uen_name in uen_name_list if len(uen_name) in (9, 10)
        #]

        # Generate list of URLs
        url_list = [base_url.format(UENNAME=uenname) for uenname in uen_name_list]
        #st.write('url_list',url_list)
    
        # Initialize an empty list to store data from all URLs
        data_list = []

        # Iterate through each URL in the list
        for url in url_list:
            # Make the GET request for each URL
            response = requests.get(url)
            response.raise_for_status()  # Raise an error for non-200 status codes
            #st.write(f"Response from URL: {url}")
            #st.write(response)  # Optional: To display the entire response object for debugging
            data = response.json()  # Parse the JSON response

            # Check if the "data" key exists and is not empty
            if "data" in data and data["data"]:
                data_list.append(data["data"])  # Append the "data" part of the response to data_list

        # Now you have all the data in data_list
        add_info = []
        for data in data_list:
            # Process each "data" part and add it to the list
            add_info.extend(data)  # Using extend to flatten the list if data is a list

        # Convert the list to a pandas DataFrame
        df = pd.DataFrame(add_info)
        st.write("Collected Data as DataFrame:")
        st.dataframe(df)  # Display the DataFrame in Streamlit
        
        return df
    
    else:
        # If the user hasn't entered anything, handle it gracefully
        st.write("Please enter a list of UENs.") 

def filter_dataframe(df,items):   
    st.subheader("Criteria used for filtering:")
    for selected_item in items:
        st.write(selected_item)
    
    try:
        # Display the list of strings
        filter_actions = {
            "Number of Fatal Cases = 0": lambda df: df["nooffatalcases"] == '0',
            "Work Injury Compentation Permanent Injury = 0": lambda df: df["noofpicases"] == '0',
            "NOT Under SWO": lambda df: df["isunderswo"] == "no",
            "NOT Under BUS": lambda df: df["isunderbusprog"] == "no"
        }

        for description, filter_function in filter_actions.items():
            filtered_df = df[filter_function(df)]

        st.subheader("List of companies that meets criteria:")    
        st.write(filtered_df)
        
        st.subheader("List of companies that did not meet criteria:")
        df_dropped = df.drop(filtered_df.index)
        st.write(df_dropped)
        
        return filtered_df, df_dropped

    except Exception as e:
        return pd.DataFrame()

def main():
    display_datetime()
    for url, filename in pdf_links:
        write_pdf(url, filename)
    create_zip()
    lines_after_company = fetch_and_process_pdf(pdf_url)
    updated_data = updated_on(lines_after_company)
    split_into_columns(updated_data)
    create_df(updated_data)
    df = input_uens_ui()
    filter_dataframe(df, items)
        
if __name__ == "__main__":
     main()
