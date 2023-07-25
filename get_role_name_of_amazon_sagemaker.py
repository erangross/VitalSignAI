from sagemaker import get_execution_role

role = get_execution_role()
print(role)