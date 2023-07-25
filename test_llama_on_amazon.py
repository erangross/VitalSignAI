# import necessary libraries
import json
import sagemaker
import boto3
from sagemaker.huggingface import HuggingFaceModel, get_huggingface_llm_image_uri

# try to get the execution role for SageMaker
# if it fails, get the role from IAM
try:
    role = sagemaker.get_execution_role()
except ValueError:
    iam = boto3.client('iam')
    role = iam.get_role(RoleName='SageMaker-Eran')['Role']['Arn']

# Hub Model configuration. https://huggingface.co/models
# set the configuration for the Hugging Face model
hub = {
    'HF_MODEL_ID':'meta-llama/Llama-2-13b-chat-hf',
    'SM_NUM_GPUS': json.dumps(1),
    'HF_API_TOKEN': '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'
}

# create Hugging Face Model Class
# create an instance of the HuggingFaceModel class with the specified image URI, environment variables, and execution role
huggingface_model = HuggingFaceModel(
    image_uri=get_huggingface_llm_image_uri("huggingface",version="0.8.2"),
    env=hub,
    role=role,
)

# deploy model to SageMaker Inference
# deploy model to SageMaker Inference with question and answer response format
predictor = huggingface_model.deploy(
    initial_instance_count=1,
    instance_type="ml.g5.2xlarge",
    container_startup_health_check_timeout=300,
    ModelDataDownloadTimeoutInSeconds = 300, # Specify the model download timeout in seconds.
    default_request_content_type='application/json',
    default_response_content_type='application/json',
    target_model='question-answering',
)

# send request
# send a request to the deployed model with the specified input
predictor.predict({
    "inputs": "what is the capital of France?",
    "outputs": "Paris"
})