import streamlit as st
import openai
import pandas as pd

openai.api_key = "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"

def process_user_input(user_input, prompt_1, prompt_2, prompt_3, prompt_4, prompt_5, prompt_6,prompt_7,prompt_8,prompt_9):
    separator = "###"  # Use a unique separator

    combined_prompt = f"{user_input}\n\n{separator}\n{prompt_1}\n\n{separator}\n{prompt_2}\n\n{separator}\n{prompt_3}\n\n{separator}\n{prompt_4}\n\n{separator}\n{prompt_5}\n\n{separator}\n{prompt_6}\n\n{separator}\n{prompt_7}\n\n{separator}\n{prompt_8}\n\n{separator}\n{prompt_9}"

    response = openai.ChatCompletion.create(
        model="gpt-4",
        messages=[
            {"role": "system", "content": "You are a helpful assistant."},
            {"role": "user", "content": combined_prompt},
        ],
    )

    generated_text = response['choices'][0]['message']['content'].strip()

    # Add three line breaks at the end of the generated text
    generated_text_with_line_breaks = f"{generated_text}\n\n\n"
    # Print API usage for debugging
    usage = response['usage']

    # Return the generated_text with line breaks
    return generated_text_with_line_breaks, usage



def calculate_cost(usage):
    input_tokens = usage.get('prompt_tokens', 0)
    output_tokens = usage.get('total_tokens', 0)
    
    # Replace with the actual cost rates
    input_cost_rate = 0.0000010  # Cost per input token
    output_cost_rate = 0.0000020  # Cost per output token
    
    total_cost = (input_tokens * input_cost_rate) + (output_tokens * output_cost_rate)
    return total_cost


# Function to split the generated text into parts based on specific titles
def split_generated_text(generated_text):
    # Split the text into parts based on specific titles
    titles = ["One Line Description","Long Description","Key Features and Functionalities","Target Audience","Use Cases","Pricing","Platform","Stage","Categories"]
    parts = []

    for i in range(len(titles) - 1):
        title = titles[i]
        if title in generated_text:
            title_start = generated_text.index(title) + len(title)
            title_end = generated_text.index(titles[i + 1], title_start) if titles[i + 1] in generated_text[title_start:] else len(generated_text)
            part = generated_text[title_start:title_end].strip()
            parts.append(part)

    # Handle the last part
    last_title = titles[-1]
    if last_title in generated_text:
        last_title_start = generated_text.index(last_title)
        last_part = generated_text[last_title_start:].strip()
        parts.append(last_part)

    return parts