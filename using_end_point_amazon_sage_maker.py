import boto3
import json

# create a client for the Amazon SageMaker runtime
runtime = boto3.client('runtime.sagemaker')

# specify the endpoint name and content type
endpoint_name = 'huggingface-pytorch-tgi-inference-2023-07-24-16-14-35-437'
content_type = 'application/json'

# specify the input text to generate questions for
input_text = "The 21 countries of the North Africa and Middle East region represent " + \
             "approximately 8% of the world’s population (600 million people). " + \
             "Egypt and Iran are the two most populous countries in the region, " + \
             "with Egypt representing 16% of total inhabitants and Iran 14%."

# specify the input payload for generating a question
question_prompt = "Generate a question for the following text:"
question_text = input_text
question_payload = json.dumps({
    'inputs': question_prompt + "\n\n" + question_text
})

# invoke the endpoint with the specified payload and content type to generate a question
question_response = runtime.invoke_endpoint(
    EndpointName=endpoint_name,
    ContentType=content_type,
    Body=question_payload
)

# process the response for generating a question
question_response_body = question_response['Body'].read().decode()
question_result = json.loads(question_response_body)

# check if the result is a list or a dictionary
if isinstance(question_result, list):
    question_result = question_result[0]

# extract the generated question from the response
generated_text = question_result['generated_text']
# extract the generated question from the response
generated_question = question_result['generated_text'].split('\n\n')[2]
# specify the input payload for generating an answer
answer_prompt = f"Generate an answer for the following question: {generated_question} based on the text: {input_text}"
answer_payload = json.dumps({
    'inputs': answer_prompt
})

# invoke the endpoint with the specified payload and content type to generate an answer
answer_response = runtime.invoke_endpoint(
    EndpointName=endpoint_name,
    ContentType=content_type,
    Body=answer_payload
)

# process the response for generating an answer
answer_response_body = answer_response['Body'].read().decode()
answer_result = json.loads(answer_response_body)

# check if the result is a list or a dictionary
if isinstance(answer_result, list):
    answer_result = answer_result[0]

# extract the generated answer from the response
generated_answer = answer_result['generated_text']

# print the generated question and answer
print('Question:', generated_question)
print('Answer:', generated_answer)

