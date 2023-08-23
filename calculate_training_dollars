import json
def calculate_tokens_and_cost(merged_jsonl_file_path):
    # Calculate the number of tokens and cost for each user input, assistant output, and system static line in the merged JSONL file
    num_tokens = 0
    num_lines = 0
    with open(merged_jsonl_file_path, 'r') as merged_jsonl_file:
        for line in merged_jsonl_file:
            try:
                qa_dict = json.loads(line)
                messages = qa_dict['messages']
                for message in messages:
                    if message['role'] == 'user':
                        num_tokens += len(message['content']) // 4
                    elif message['role'] == 'assistant':
                        num_tokens += len(message['content']) // 4
                    elif message['role'] == 'system':
                        num_tokens += len(message['content']) // 4
                num_lines += 1
            except json.JSONDecodeError:
                # Skip empty lines or lines that are not in the expected format
                pass
    cost = num_tokens  / 1000 * 0.0080
    # Print the total number of tokens, number of lines, and cost for the merged JSONL file
    print(f'Total number of tokens: {num_tokens}')
    print(f'Total number of lines: {num_lines}')
    print(f'Total cost: ${cost:.2f}')

if __name__ == '__main__':
    merged_jsonl_file_path = './datasets/merged.jsonl'
    calculate_tokens_and_cost(merged_jsonl_file_path)