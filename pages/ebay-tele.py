import streamlit as st
import re
import requests
from bs4 import BeautifulSoup
import re
import json
import ast
import datetime
import pytz
import _strptime
from datetime import datetime, timedelta
from pytz import timezone

# Streamlit app
st.title("Ebay Telegram Bot")

#urls_to_scrape = ["https://www.ebay.com.sg/itm/204781289466?_trkparms=amclksrc%3DITM%26aid%3D777008%26algo%3DPERSONAL.TOPIC%26ao%3D1%26asc%3D20230811125216%26meid%3D4d3ed92226d544138a02639cbf8cc0b0%26pid%3D101771%26rk%3D1%26rkt%3D1%26itm%3D204781289466%26pmt%3D0%26noa%3D1%26pg%3D4375194%26algv%3DWatchlistVariantWithMLR%26brand%3DCanon&_trksid=p4375194.c101771.m47999&_trkparms=parentrq%3A8b33e28a18f0a54e317619b1ffff99de%7Cpageci%3Aae59042e-14ff-11ef-97d7-c25dc6d1c00c%7Ciid%3A1%7Cvlpname%3Avlp_homepage",
# "https://www.ebay.com.sg/itm/204781289466",
# "https://www.ebay.com.sg/itm/387013925413?_trkparms=amclksrc%3DITM%26aid%3D777008%26algo%3DPERSONAL.TOPIC%26ao%3D1%26asc%3D20230811123856%26meid%3Ddd9a46f3f73e425d9cfb2e19850a1033%26pid%3D101770%26rk%3D1%26rkt%3D1%26itm%3D387013925413%26pmt%3D0%26noa%3D1%26pg%3D4375194%26algv%3DRecentlyViewedItemsV2&_trksid=p4375194.c101770.m146925&_trkparms=parentrq%3A8b37412d18f0a8cc93df3628ffff9df8%7Cpageci%3A31f83d34-1500-11ef-8eeb-fa40e6d0f5b6%7Ciid%3A1%7Cvlpname%3Avlp_homepage"
#]

#urls_to_scrape = input('Enter urls separated by commas:')

# Create a text input area where the user can enter multiple URLs separated by commas
urls_to_scrape = st.text_area(
    "Enter URLs separated by commas:",
    placeholder="e.g. https://www.ebay.com.sg/itm/204781289466, https://www.ebay.com.sg/itm/387013925413"
)

# Process the input if it's not empty
if urls_input:
    # Split the input string into a list of URLs
    urls_to_scrape = [url.strip() for url in urls_input.split(',')]
    
    st.write("URLs to scrape:", urls_to_scrape)
else:
    st.write("Please enter some URLs.")

wishlist = []

pattern = r'www\.ebay\.com\.sg/itm/(\d+)(?:\?|$)'

for url in urls_to_scrape:
    match = re.search(pattern, url)

    if match:
        item_number = match.group(1)
        wishlist.append(item_number)
        print(item_number)
    else:
        print("No match found.")


#wishlist = [196383109829, 204781289466,387007540962]

bid_times = []

def scrape_ebay(wishlist):
    for itm_num in wishlist:
        url = f"https://www.ebay.com.sg/itm/{itm_num}"
        response = requests.get(url)
        soup = BeautifulSoup(response.text, "html.parser")
        script_tags = soup.find_all("script")

        for script_tag in script_tags:
            script_text = script_tag.string
            if script_text and r'appendText' in script_text:
                # Ensure script_text is not None before using it in the regular expression search
                pattern = r'appendText":{(.*?)\}'
                match = re.search(pattern, script_text)

                # If the pattern is found, extract the desired text
                if match:
                    extracted_text = match.group(1)
                    # Remove any leading/trailing whitespace

                    text = extracted_text.strip()

                    # Safely evaluate the string as a Python literal
                    try:
                        #print(text[28:-2])
                        #date_time = datetime.strptime(text[28:-6], '%B %d, %Y %H:%M:%S')
                        bid_times.append({"url": url, "date_time": datetime.strptime(text[28:-6], '%B %d, %Y %H:%M:%S')})
                        #return(bid_times)
                    except (SyntaxError, ValueError) as e:
                        print("Error evaluating the string:", e)

    print(bid_times)
    return(bid_times)

# Example usage:
data = scrape_ebay(wishlist)
st.write(data)
# sgt = timezone('Asia/Singapore')
# now_sgt = datetime.now(sgt)
# #Define the timezone for Singapore

# def trigger_tele(data):
#   # Search for the pattern in the text
#     for dict_item in data:
#         # Convert the extracted datetime to Singapore Time (SGT)

#         extracted_date_time = sgt.localize(dict_item["date_time"])    #current_time_sgt = now_sgt.strftime(format)
#         #extracted_time_sgt = extracted_date_time.strftime(format)
#         print("Current time in SGT:", now_sgt)
#         print("End time in SGT:", extracted_date_time)
#         # Calculate the difference between current date and extracted date

#         difference = extracted_date_time - now_sgt
#         days = difference.days
#         hours, remainder = divmod(difference.seconds, 3600)
#         minutes, seconds = divmod(remainder, 60)

#         diff = f'{hours} hours, {minutes} minutes, {seconds} seconds'

#         #print("difference",difference)
#         print(now_sgt)
#         print(extracted_date_time)

#         # Check if the difference is less than 10 minutes
#         if difference < timedelta(minutes=10):
#             message = f"Bid for {dict_item['url']} ends in <10 minutes at {extracted_date_time}"
#             print(message)
#             response = send_telegram_message(message)

#         # Check if the difference is at least 3 days
#         elif difference > timedelta(minutes=10):
#             message = f"Bid for {dict_item['url']} ends in {diff} at {extracted_date_time}"
#             print(message)
#             response = send_telegram_message(message)
