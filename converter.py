import streamlit as st
import pandas as pd
import json
import io

def update_json_with_tool_name(json_data, csv_content, identifier_column):
    # Load CSV data into a DataFrame
    df_csv = pd.read_csv(io.StringIO(csv_content.decode("utf-8")))

    # Convert JSON data to a list of dictionaries
    json_list = json.loads(json_data)

    # Update each dictionary with the 'tool_name' from the CSV
    for entry in json_list:
        identifier_value = entry.get(identifier_column)
        tool_name = df_csv[df_csv[identifier_column] == identifier_value]['tool_name'].values
        if tool_name:
            entry['tool_name'] = tool_name[0]

    # Convert the updated list of dictionaries back to JSON
    updated_json_data = json.dumps(json_list, indent=2)
    return updated_json_data

def mainC():
    st.title("Update JSON with Tool Name from CSV")

    uploaded_file_json = st.file_uploader("Upload an existing JSON file", type=["json"])
    uploaded_file_csv = st.file_uploader("Upload a CSV file with tool_name", type=["csv"])

    if uploaded_file_json is not None and uploaded_file_csv is not None:
        st.subheader("Existing JSON Content")
        json_content = uploaded_file_json.read()
        st.code(json_content)

        st.subheader("CSV Content")
        csv_content = uploaded_file_csv.read()
        st.code(csv_content)

        identifier_column = st.text_input("Enter the common identifier column name:")

        if st.button("Update JSON with Tool Name"):
            updated_json_data = update_json_with_tool_name(json_content, csv_content, identifier_column)

            st.subheader("Updated JSON Output")
            st.code(updated_json_data, language="json")

            # Download button for the updated JSON
            st.download_button(
                label="Download Updated JSON",
                data=updated_json_data,
                file_name="scraped_output.json",
                key="download-json-updated",
            )

if __name__ == "__main__":
    mainC()
