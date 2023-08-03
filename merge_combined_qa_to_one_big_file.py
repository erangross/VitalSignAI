import glob
import os

def main():
    # Set the parent directory containing the subdirectories with JSONL files
    parent_dir = "./datasets"

    # Create a new file to hold the combined data
    output_filename = os.path.join(parent_dir, "combined_qa_all.jsonl")
    with open(output_filename, 'w', encoding='utf-8') as output_file:
        # Loop through all the subdirectories in the parent directory
        for subdir in os.listdir(parent_dir):
            subdir_path = os.path.join(parent_dir, subdir)
            if os.path.isdir(subdir_path):
                # Get a list of all the "combined_qa.jsonl" files in the subdirectory
                file_list = glob.glob(os.path.join(subdir_path, "combined_qa.jsonl"))
                # Loop through each file and append its contents to the output file
                for filename in file_list:
                    with open(filename, 'r', encoding='utf-8') as input_file:
                        for line in input_file:
                            output_file.write(line)



# Main function
if __name__ == "__main__":
    main()
    

