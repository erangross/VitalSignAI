import os

datasets_dir = './datasets'

for dirpath, dirnames, filenames in os.walk(datasets_dir):
    if 'combined_qa.jsonl' in filenames:
        combined_qa_path = os.path.join(dirpath, 'combined_qa.jsonl')
        os.remove(combined_qa_path)
        print(f'Removed {combined_qa_path}')