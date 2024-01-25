import streamlit as st
import pandas as pd
import json
import os
from tempfile import NamedTemporaryFile
from api_connect import process_user_input
from api_connect import split_generated_text

st.set_page_config(
    page_title="Dataswift",
    page_icon="🔮",
    layout="centered",
    initial_sidebar_state="auto",
)

prompt_1 = "Based on the input, provide a brief and clear two-sentence description of the tool. Present this information under the title 'One Line Description' (avoid using bold formatting or double asterisks)."
prompt_2 = "Craft a detailed and comprehensive paragraph-length description based on the input. Present the information under the title 'Long Description' (ensure that the output does not include bold formatting or double asterisks)."
prompt_3 = "Summarize detailed key features and functionalities in a bullet-point format based on the text from a website output. Ensure each feature is presented with a clear title. Display the information under the title 'Key Features and Functionalities' (avoid using bold formatting or double asterisks)."
prompt_4 = "Provide detailed information about the demographic or professional groups that can benefit from using this tool, outlining their characteristics and specific needs. Present the information under the title 'Target Audience' in a structured format using bullet points."
prompt_5 = "Specify the various use cases, outlining scenarios or applications where individuals or organizations can benefit from the features and functionalities of this tool. Present the information under the title 'Use Cases' (avoid using bold formatting or double asterisks)."
prompt_6 = "Can you provide details about the pricing structure of the tool, including different plans and any free or trial versions? Present this information under the title 'Pricing' (ensure no use of bold formatting or double asterisks)."
prompt_7 = "Where is the tool available, and on what platforms, such as web apps, app stores, extensions, or plugins? Present this information under the title 'Platform' (avoid using bold formatting or double asterisks)."
prompt_8 = "What is the current business stage of the tool, whether it's in alpha, beta, emerging, or considered a market leader or any other stage? Present this information under the title 'Stage' (ensure no use of bold formatting or double asterisks)."
prompt_9 = "In which categories or industries does the tool belong? Can you provide information on any subcategories that further specify its functionalities or services? Present this information under the title 'Categories' (don't elaborate in detail, only mention category names with ',' to separate, and avoid using bold formatting or double asterisks)."

def save_to_csv(data):
    try:
        existing_data = pd.read_csv('data.csv')
        new_data = pd.DataFrame(data, columns=['Tool name', 'URL', 'Description - One line', 'Description - Long Text',
                                               'Key Features and Functionalities', 'Target Audience', 'Use Cases','Pricing','Platform','Stage','Categories'
                                               ])

        # Concatenate the existing and new data
        combined_data = pd.concat([existing_data, new_data], ignore_index=True)

        # Save the combined data to the CSV file
        combined_data.to_csv('data.csv', index=False)

    except FileNotFoundError:
        # If the file doesn't exist, create a new DataFrame with the provided data and save it with a header
        pd.DataFrame(data, columns=['Tool name', 'URL', 'Description - One line', 'Description - Long Text',
                                     'Key Features and Functionalities', 'Target Audience', 'Use Cases','Pricing','Platform','Stage','Categories'
                                     ]).to_csv('data.csv', index=False, header=True)

def load_data():
    try:
        df = pd.read_csv('data.csv')
        return df
    except FileNotFoundError:
        return None

def process_and_save_data_for_json_entry(entry):
    tool_name = entry.get("tool_name", "")
    tool_url = entry.get("tool_url", "")
    user_input = entry.get("user_input", "")

    generated_text_with_line_breaks, usage = process_user_input(user_input, prompt_1, prompt_2, prompt_3, prompt_4, prompt_5, prompt_6,prompt_7,prompt_8, prompt_9)
    parts = split_generated_text(generated_text_with_line_breaks)
    
    short_description, long_description, key_features, trgt_audience, use_cases, pricing, platform, stage, categories = parts
    data = {
        'Tool name': [tool_name],
        'URL': [tool_url],
        'Description - One line': [short_description],
        'Description - Long Text': [long_description],
        'Key Features and Functionalities': [key_features],
        'Target Audience': [trgt_audience],
        'Use Cases': [use_cases],
        'Pricing': [pricing],
        'Platform': [platform],
        'Stage': [stage],
        'Categories': [categories]
    }

    # Save data to CSV
    save_to_csv(data)

    return data

def process_and_save_data_for_json(json_file_path):
    with open(json_file_path, 'r') as json_file:
        data_entries = json.load(json_file)

    for entry in data_entries:
        processed_data = process_and_save_data_for_json_entry(entry)
        st.success(f"Data processed and saved for {processed_data['Tool name'][0]}")

# Streamlit app
def main():
    st.title("🔍 Dataswift: The Data Maestro 🎩📊")
    st.write("Built by AJ with \u2764️")

    api_key = st.text_input("Enter your API Key:", "")
    
    # File uploader for JSON
    uploaded_file_json = st.file_uploader("Upload a JSON file", type=["json"])

    if uploaded_file_json is not None:
        st.write("JSON File Uploaded Successfully!")

        # Save the uploaded JSON file
        with NamedTemporaryFile(delete=False) as temp_file:
            temp_file.write(uploaded_file_json.read())
            json_path = temp_file.name

        # Process and save data for each entry in the JSON file
        process_and_save_data_for_json(json_path)

        # Display saved data
        st.header("Saved Data:")
        saved_data = load_data()
        if saved_data is not None:
            st.write(saved_data)
        else:
            st.info("No data saved yet.")

        # Remove the temporary JSON file
        os.remove(json_path)

if __name__ == "__main__":
    main()