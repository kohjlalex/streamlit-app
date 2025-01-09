from backgroundchecker.functions import display_datetime, write_pdf, create_zip, fetch_and_process_pdf, updated_on, split_into_columns, create_df,input_uens_ui, filter_dataframe
from backgroundchecker.constants import pdf_links, pdf_url, items

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
