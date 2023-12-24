import streamlit as st
from scrapy import main as display_page1
from dataswift import main as display_page2

st.title("Multi-Page App")
def main():

    # Radio button for page selection
    selected_page = st.radio("Select a page", ["Scrapy", "DataSwift"], horizontal= True)

    # Display content based on the selected page
    if selected_page == "Scrapy":
        display_page1()
    elif selected_page == "DataSwift":
        display_page2()

if __name__ == "__main__":
    main()

