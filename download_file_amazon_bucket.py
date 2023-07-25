import boto3

def download_file(bucket_name, object_name, file_name):
    """Download a file from an S3 bucket

    :param bucket_name: Bucket to download from
    :param object_name: S3 object name to download
    :param file_name: Local file name to save the downloaded file as
    :return: True if file was downloaded, else False
    """

    # Download the file
    s3_client = boto3.client('s3')
    try:
        s3_client.download_file(bucket_name, object_name, file_name)
    except Exception as e:
        print(e)
        return False
    return True

if __name__ == '__main__':
    if (download_file('eran-test-bucket', 'test.txt', 'downloaded_test.txt')):
        print('File was downloaded')
    else:
        print('File was not downloaded')