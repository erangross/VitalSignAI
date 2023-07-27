import json
import glob


# Create an empty list to hold all the non-empty question-answer pairs
all_qa_pairs = []

# Loop through all the files in the output directory that match the pattern
for filename in glob.glob("neonatal-cardiology_page_*_qa.json"):
    # Check if the file contains any JSON data
    with open(filename, 'r') as f:
        try:
            data = json.load(f)
        except json.decoder.JSONDecodeError:
            continue
    # Replace "Answer not found" with actual answers and remove answer from prompt
    for qa_pair in data:
        if qa_pair['completion'] == "Answer not found.":
            # Extract the answer from the prompt
            answer_start = qa_pair['prompt'].find("Answer: ")
            if answer_start != -1:
                answer = qa_pair['prompt'][answer_start+len("Answer: "):].strip()
                qa_pair['completion'] = answer
                qa_pair['prompt'] = qa_pair['prompt'][:answer_start].strip()
            else:
                qa_pair['completion'] = ""
        else:
            # Remove the answer from the prompt
            answer_start = qa_pair['prompt'].find("\nAnswer:")
            if answer_start != -1:
                qa_pair['prompt'] = qa_pair['prompt'][:answer_start].strip()
    # Remove the number from each prompt
    for qa_pair in data:
        if '. ' in qa_pair['prompt']:
            qa_pair['prompt'] = qa_pair['prompt'].split('. ', 1)[1]
        if qa_pair['prompt'].startswith(':'):
            qa_pair['prompt'] = qa_pair['prompt'][2:].strip()
        if qa_pair['completion'].startswith('Answer: '):
            qa_pair['completion'] = qa_pair['completion'][8:].strip()
    # Add all the non-empty question-answer pairs to the list
    non_empty_qa_pairs = [qa_pair for qa_pair in data if qa_pair['prompt'] and qa_pair['completion']]
    all_qa_pairs.extend(non_empty_qa_pairs)

# Write the combined list of non-empty question-answer pairs to a new file in JSONL format
with open("combined_qa.jsonl", 'w', encoding='utf-8') as f:
    for qa_pair in all_qa_pairs:
        json.dump(qa_pair, f, ensure_ascii=False)
        f.write('\n')