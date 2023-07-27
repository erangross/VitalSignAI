import fitz
import openai
import json
import os
import time
# Load the PDF file
# Define the directory containing the JSON files
# Keep track of the current page number and the total number of pages
current_page = None
total_pages = 0
# Define the directory containing the JSON files
directory = "/home/erangross/MedicalChatGPT/datasets/atlas-of-nuclear-cardiology"
# Load the PDF file
pdf_file_name = "atlas-of-nuclear-cardiology.pdf"
pdf_file = fitz.open(pdf_file_name)

# Iterate through all JSON files in the directory
for filename in os.listdir(directory):
    if filename.endswith(".json"):
        filepath = os.path.join(directory, filename)
        # Load the questions and answers from the JSON file
        try:
            with open(filepath, "r") as f:
                qa_list = json.load(f)
        except json.decoder.JSONDecodeError:
            print(f"Error: Empty or invalid JSON file '{filename}'. Skipping file.")
            continue
        # Extract the page number from the filename
        page_number = filename.split("_")[2]
        # Iterate through the questions and answers
        for qa_dict in qa_list:
            # Extract the question and answer from the dictionary
            question = qa_dict.get("prompt")
            answer = qa_dict.get("completion")
            # Extract the text from the page
            page = pdf_file[page_number]
            page_text = page.get_text()
                # Define the conversation history as a list of messages
            conversation = [
                {"role": "system", "content": f"Please check if the answer '{answer}' for the question '{question}' is correct. Return 'yes' or 'no'."},
                {"role": "user", "content": page_text},
            ]
            # Use OpenAI's GPT-3 to generate a prompt and completion
            while True:
                try:
                    completion = openai.ChatCompletion.create(
                        model="gpt-3.5-turbo",
                        messages=conversation,
                        max_tokens=300,
                        temperature=0.1  # Adjust this value to control the randomness of the output
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
            if completion:
                # Extract the prompt and completion from the response
                response = completion.choices[0].message["content"]
     
            # Check if the generated answer is correct according to the page text
            if response.lower() == "yes":
                print(f"The generated answer '{answer}' is correct according to the page text.")
            elif response.lower() == "no":
                print(f"The generated answer '{answer}' is incorrect according to the page text.")
                # Rewrite the answer based on the text in the PDF file
                # ...
            else:
                print("Unable to verify if the generated answer is correct according to the page text.")
                # Rewrite the answer based on the text in the PDF file
                
