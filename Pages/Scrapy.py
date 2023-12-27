import streamlit as st
from tempfile import NamedTemporaryFile
import subprocess
import os
import json

st.set_page_config(
    page_title="Scrapy",
    page_icon="🕸️",
    layout="centered",
    initial_sidebar_state="auto",
)
        
def download_file(file_path, file_name):
    with open(file_path, "rb") as file:
        contents = file.read()
        st.download_button(label="Download JSON", data=contents, file_name=file_name, mime="application/json")

# Streamlit app
def main():
    st.title("🕸️ Scrapy: The Web-Scraping Maestro 🕷️🌐")
    st.write("Built by AJ with \u2764️")

    # File uploader for CSV
    uploaded_file = st.file_uploader("Upload a CSV file", type=["csv"])

    if st.button("Display Data"):
        display_scraped_data()

    file_path = "Pages/scraped_output.json"
    file_name = "scraped_output.json"

    if st.button("Download JSON"):
        download_file(file_path, file_name)

    if uploaded_file is not None:
        st.write("File Uploaded Successfully!")

        # Save the uploaded CSV file
        with NamedTemporaryFile(delete=False) as temp_file:
            temp_file.write(uploaded_file.read())
            csv_path = temp_file.name

        # Execute the Puppeteer script
        execute_puppeteer_script(csv_path)

        # Display the result from the scraped data
        os.remove(csv_path)

        
# Function to execute Puppeteer script
def execute_puppeteer_script(csv_path):
    puppeteer_script_path = "Pages/scrapy-main.js"  # Replace with the actual path
    command = ["node", puppeteer_script_path, csv_path]
    subprocess.run(command, check=True)

# Function to display the scraped data in Streamlit
def display_scraped_data():
    try:
        with open('Pages/scraped_output.json', 'r') as file:
            scraped_data = json.load(file)
            st.write("Scraped Data:")
            for entry in scraped_data:
                st.write(f"url: {entry['tool_url']}")
                st.write(f"user_input: {entry['user_input']}")
                st.write("---")
    except FileNotFoundError:
        st.warning("Scraped output file not found. Make sure the Puppeteer script ran successfully.")


# Run the Streamlit app
if __name__ == "__main__":
    main()