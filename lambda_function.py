import json
import boto3
import time
from urllib.parse import unquote_plus

print("Loading lambda function")
s3 = boto3.client('s3')

def lambda_handler(event, context):
    
    src_bucket = event['Records'][0]['s3']['bucket']['name']
    key = unquote_plus(event['Records'][0]['s3']['object']['key'])
    dest_bucket = 'dest-bucket-6161632' #dest bucket
    copy_src = {'Bucket':src_bucket, 'Key':key}
    
    try:
        print("waiting for the file persist in the source bucket")
        waiter = s3.get_waiter('object_exists')
        waiter.wait(Bucket= src_bucket, Key= key)
        print("copying the object from the source s3 bucket to destination s3 bucket")
        s3.copy_object(Bucket= dest_bucket, Key= key, CopySource= copy_src)
    except Exception as e:
        print(e)
        print("Error getting object {} from bucket {}. Make sure tehy exists in the bucket".format(key, src_bucket))
        raise e

    # return {
    #     'statusCode': 200,
    #     'body': json.dumps('Hello from Lambda!')
    # }