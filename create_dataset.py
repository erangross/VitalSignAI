import os
import json
import re
import fitz  # PyMuPDF
import openai
import time

# This is a helper function to load the OpenAI API key from the environment variable
def load_openai_api_key(api_key):
    openai.api_key = api_key

# This is a helper function to create the output folder if it doesn't exist
def return_output_folder_name(pdf_file_name):
    # Get the base name of the PDF file
    file_name = pdf_file_name.split('.')[0]
    # Define the output folder
    output_folder = f"./output/{file_name}/"
    # Create the output folder if it doesn't exist
    if not os.path.exists(output_folder):
        os.mkdir(output_folder)
    # Return the output folder
    return output_folder

# This is a helper function to generate questions and answers from a page of text
def generate_question_answers(pdf_file_name, page_text, page_number):
    # Clean the page text by removing extra spaces
    page_text = re.sub(r'\s+', ' ', page_text)

    # Define the conversation history as a list of messages
    conversation = [
        {"role": "system", "content": f"Please create four questions and answers based on the content of the page only, Generate questions that have clear answers from the page text. {page_number} of the {pdf_file_name} document."},
        {"role": "user", "content": page_text},
    ]
    # Use OpenAI's GPT-3 to generate a prompt and completion
    while True:
        try:
            completion = openai.ChatCompletion.create(
                model="gpt-3.5-turbo-0613",
                messages=conversation,
                max_tokens=320,
                temperature=0.1  # Adjust this value to control the randomness of the output
            )
            break
        except (openai.error.ServiceUnavailableError, 
                openai.error.APIConnectionError, openai.error.InvalidRequestError) as e:
            print(f"OpenAI API error: {e}")
            if "This model's maximum context" in str(e):
                print("skip...moving to next page")
                return # skip this page
            else:
                print("Retrying in 1 minute...")
                time.sleep(60)
    # Extract the prompt and completion from the response
    content_string = completion.choices[0].message["content"]

    # Replace the Unicode characters with their corresponding characters
    content_string = content_string.replace('\u201c', '"').replace('\u201d', '"')

    # Split the content string into a list of lines
    content_lines = content_string.split("\n")

    # Initialize lists for questions and answers
    questions = []
    answers = []

    # Iterate through the content lines and identify questions and answers
    for line in content_lines:
        line = line.strip()

        if re.match(r'^\d+\.', line):  # If the line starts with a number followed by a period
            questions.append(line)
        elif line:
            # Remove the leading '-' from the answer
            answer = line.lstrip('-').strip()
            answers.append(answer)

    # Return the questions and answers as a dictionary
    return {
        "questions": questions,
        "answers": answers,
    }
# This is a helper function to check if a PDF file has already been processed
def should_skip_pdf_file(pdf_file, output_folder):
    # Get the base name of the PDF file
    pdf_file_name = os.path.basename(pdf_file)
    # Get the base name of the JSON file
    json_file_name = f"{os.path.splitext(pdf_file_name)[0]}_page_0_qa.json"
    # Get the path to the JSON file
    json_file_path = os.path.join(output_folder, json_file_name)
    # Check if the JSON file exists
    if os.path.exists(json_file_path):
        # If the JSON file exists, get the list of existing JSON files
        existing_json_files = [f for f in os.listdir(output_folder) if f.endswith('.json')]
        # Get the last processed page number
        last_page_number = max([int(f.split('_')[2]) for f in existing_json_files])
        # Return the list of existing JSON file names and the last processed page number
        return [os.path.basename(f) for f in existing_json_files], last_page_number
    else:
        # If the JSON file does not exist, return an empty list and page number 0
        return [], 0
    
# This is the main function that processes the PDF files
def process_pdf_files():
    print("Processing PDF files...")
    # Iterate through the files in the current directory
    for pdf_file_name in os.listdir():
        print(f"Checking file '{pdf_file_name}'...")
        if not pdf_file_name.endswith(".pdf"):
            print(f"Skipping non-PDF file '{pdf_file_name}'.")
            continue
        # Create the output folder if it doesn't exist
        output_folder = return_output_folder_name(pdf_file_name)
        # Check if the PDF file has already been processed
        existing_json_files, last_page_number = should_skip_pdf_file(pdf_file_name, output_folder)
        # Open the PDF file
        try:
            pdf_document = fitz.open(pdf_file_name)
        except Exception as e:
            print(f"Error processing '{pdf_file_name}': {e}")
            continue
        #Starting with the last page number + 1
        if existing_json_files:
            starting_page = last_page_number + 1
        else:
            starting_page = 0
        # Iterate through the pages in the PDF file
        current_page = starting_page
        while current_page < pdf_document.page_count:
            # Load the page text
            try:
                page = pdf_document.load_page(current_page)
                page_text = page.get_text("text")
            except Exception as e:
                print(f"Error loading page {current_page} of '{pdf_file_name}': {e}")
                # If there was an error loading the page, retry the connection
                pdf_document.close()
                pdf_document = fitz.open(pdf_file_name)
                continue
            # Generate questions and answers from the page text
            # Try to generate questions and answers from the page text using OpenAI API
            try:
                qa_dict = generate_question_answers(pdf_file_name, page_text, current_page + 1)
            # Catch OpenAI API errors and retry after 1 minute
            except (openai.error.APIError, openai.error.APIConnectionError, openai.error.InvalidRequestError) as e:
                print(f"OpenAI API error: {e}")
                print("Retrying in 1 minute...")
                time.sleep(60)
            # If no questions and answers were generated, move on to the next page
            if not qa_dict:
                print(f"No questions and answers generated for page {current_page} of '{filpdf_file_namee_name}'")
                current_page += 1
                continue
            # If questions and answers were generated, extract them from the dictionary
            if 'questions' in qa_dict and 'answers' in qa_dict:
                questions = qa_dict['questions']
                answers = qa_dict['answers']
            # If no questions and answers were generated, set empty lists for questions and answers
            else:
                questions = []
                answers = []
            # Save the questions and answers to a JSON file
            output_file_name = f"{os.path.splitext(pdf_file_name)[0]}_page_{current_page}_qa.json"
            # Create the output file path
            output_file_path = os.path.join(output_folder, output_file_name)
            # Save the questions and answers to the output file
            with open(output_file_path, 'w') as output_file:
                # Save the questions and answers to the output file
                output_file.write("[\n")
                # Iterate through the questions and answers
                for i, (question, answer) in enumerate(zip(questions, answers)):
                    qa_dict = {"prompt": question, "completion": answer}
                    # Save the questions and answers to the output file
                    output_file.write(json.dumps(qa_dict, indent=4))
                    # Add a comma after each question and answer
                    if i < len(questions) - 1:
                        output_file.write(",\n")
                output_file.write("\n]\n")
            print(f"Questions and answers generated for page {current_page} of '{pdf_file_name}' and saved in '{output_folder}' directory.")
            current_page += 1
        # Close the PDF document
        pdf_document.close()
        # Finish processing the book message.
        print(f"Finish processing the book\n")
    print("Finished processing PDF files.")



# This is the main function that is executed when the script is run
if __name__ == "__main__":
    # Load the OpenAI API key from the environment variable
    api_key = os.environ.get("OPENAI_API_KEY")
    # If the OpenAI API key is not set, raise an error
    if not api_key:
        raise ValueError("Please set the OPENAI_API_KEY environment variable")
    # Load the OpenAI API key
    load_openai_api_key(api_key)
    # Process the PDF files
    process_pdf_files()