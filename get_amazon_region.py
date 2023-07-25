import boto3

# Create a new session
session = boto3.session.Session()

# Get the region that the session is configured for
region = session.region_name

# Print the region
print(region)