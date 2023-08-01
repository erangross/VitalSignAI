import fitz
import openai
import os
import time
import json
# Set up OpenAI API credentials
openai.api_key = os.environ.get("OPENAI_API_KEY")

# Load the PDF file
pdf_file = fitz.open('The-Brain-That-Changes-Itself.pdf')

# Create a new PDF file for the summarized content
new_pdf = fitz.open()

p = fitz.Point(50, 72)  # start point of 1st line


# Iterate through each page# Define the conversation history as a list of messages

for page_num in range(pdf_file.page_count):
    # Extract the text content of the page
    page = pdf_file.load_page(page_num)
    text = page.get_text()
    conversation = [
        {"role": "system", "content": f"Please summerize each page with simple english for high school student for {page} of the {pdf_file.name} document."},
        {"role": "user", "content": text},
    ]
# Use OpenAI's GPT-3 to generate a prompt and completion
    while True:
    # Use GPT-3 to generate a summary
        try:
            completion = openai.ChatCompletion.create(
                model="gpt-3.5-turbo",
                messages=conversation,
                temperature=0.1,
                max_tokens=256
            )
            break
        except (openai.error.ServiceUnavailableError, 
                    openai.error.APIConnectionError, openai.error.InvalidRequestError) as e:
                print(f"OpenAI API error: {e}")
                if "This model's maximum context" in str(e):
                    print("skip...moving to next page")
                    break # skip this page
                else:
                    print("Retrying in 1 minute...")
                    time.sleep(60) 
        
    # Extract the prompt and completion from the response
    content_string = completion.choices[0].message["content"]
    # Replace the Unicode characters with their corresponding characters
    content_string = content_string.replace('\u201c', '"').replace('\u201d', '"')
    # Write the summary to a new text file
    # Save the questions and answers to a JSON file
    output_file_name = f"{os.path.splitext(pdf_file.name)[0]}_page_{page}.txt"
    with open(output_file_name, 'w') as f:
        f.write(content_string)
    # Print the name of the page and the output file
    print(f"Page {page} saved to {output_file_name}")
    