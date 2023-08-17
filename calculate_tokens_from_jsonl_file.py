import json

# Set the path to the JSONL file
jsonl_file = "/home/eran/VitalSignAI/datasets/combined_qa_all.jsonl"

# Initialize counters for the total number of tokens in the prompts and completions
prompt_tokens = 0
completion_tokens = 0

# Loop through each line in the JSONL file
with open(jsonl_file, 'r', encoding='utf-8') as f:
    for line in f:
        # Parse the JSON object from the line
        data = json.loads(line)
        # Count the number of tokens in the prompt and add it to the prompt_tokens counter
        prompt_tokens += len(data['prompt']) // 4
        # Count the number of tokens in the completion and add it to the completion_tokens counter
        completion_tokens += len(data['completion']) // 4

# Print the total number of tokens in the prompts and completions
print("Total number of K tokens in prompts:", prompt_tokens / 1000)
print("Total number of K tokens in completions:", completion_tokens /1000)
print("Total number of K tokens in prompts and completions:", (prompt_tokens + completion_tokens) / 1000)
print("Total amount of dollars for the training datasets:", (prompt_tokens + completion_tokens) / 1000 * 0.03)