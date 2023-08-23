import os
import json
import re
def convert_all_json_files_to_jsonl(input_folder_path):
    # Get a list of all the JSON files in the input folder and its subfolders
    json_file_paths = []
    for root, dirs, files in os.walk(input_folder_path):
        for file in files:
            if file.endswith('.json'):
                json_file_paths.append(os.path.join(root, file))
    # Convert each JSON file to a JSONL file and delete the original JSON file
    for input_file_path in json_file_paths:
        # Load the questions and answers from the input file
        with open(input_file_path, 'r') as input_file:
            try:
                qa_list = json.load(input_file)
            except json.decoder.JSONDecodeError:
                continue
        # Convert the questions and answers to the new format
        qa_list_new = []
        for qa_dict in qa_list:
            question = qa_dict["prompt"]
            # Remove the numbering from the question
            question = re.sub(r'^\d+\.\s*', '', question)
            answer = qa_dict["completion"]
            # Remove the "Answer:" prefix from the answer
            answer = re.sub(r'^Answer:\s*', '', answer)
            qa_dict_new = {"messages": [{"role": "system", "content": "You are a professional medical doctor"}, {"role": "user", "content": question}, {"role": "assistant", "content": answer}]}
            qa_list_new.append(qa_dict_new)
        # Save the questions and answers to the output file as a JSONL file
        output_file_path = os.path.splitext(input_file_path)[0] + '.jsonl'
        with open(output_file_path, 'w') as output_file:
            for qa_dict_new in qa_list_new:
                output_file.write(json.dumps(qa_dict_new) + "\n")
        # Delete the original JSON file
        os.remove(input_file_path)

if __name__ == '__main__':
    # Convert all the JSON files in the input folder and its subfolders to JSONL files with the new format
    input_folder_path = './datasets'
    convert_all_json_files_to_jsonl(input_folder_path)