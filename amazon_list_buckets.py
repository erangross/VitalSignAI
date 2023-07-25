import boto3

# Create an S3 client with the endpoint URL for the us-east-1 region
s3 = boto3.client('s3', endpoint_url='https://s3.us-east-1.amazonaws.com')

# Call S3 to list current buckets
response = s3.list_buckets()

# Get a list of all bucket names from the response
buckets = [bucket['Name'] for bucket in response['Buckets']]

# Check if the bucket already exists
if 'my-bucket-name' in buckets:
    print("Bucket already exists")


# Print out the bucket list
print("Bucket List: %s" % buckets)