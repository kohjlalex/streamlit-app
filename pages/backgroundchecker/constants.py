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
