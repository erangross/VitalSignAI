import os


def merge_all_jsonl_files(input_folder_path):
    # Get a list of all the subdirectories in the input folder
    subdirectories = [d for d in os.listdir(input_folder_path) if os.path.isdir(os.path.join(input_folder_path, d))]
    # Merge all the JSONL files in each subdirectory into a single JSONL file
    for subdirectory in subdirectories:
        jsonl_file_paths = [os.path.join(input_folder_path, subdirectory, f) for f in os.listdir(os.path.join(input_folder_path, subdirectory)) if f.endswith('.jsonl')]
        if len(jsonl_file_paths) > 0:
            merged_jsonl_file_path = os.path.join(input_folder_path, subdirectory, subdirectory + '_merged.jsonl')
            with open(merged_jsonl_file_path, 'w') as merged_jsonl_file:
                for jsonl_file_path in jsonl_file_paths:
                    with open(jsonl_file_path, 'r') as jsonl_file:
                        merged_jsonl_file.write(jsonl_file.read())

if __name__ == '__main__':
    merge_all_jsonl_files('./datasets')