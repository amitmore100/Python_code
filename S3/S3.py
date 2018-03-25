import boto3
import uuid

s3client = boto3.client('s3')
bucket_name = 'python-sdk-sample{}'.format(uuid.uuid4())
print('Creating new bucket with name: {}'.format(bucket_name))
s3client.create_bucket(Bucket=bucket_name)
list_buckets_resp = s3client.list_buckets()
for bucket in list_buckets_resp['Buckets']:
	if bucket['Name'] == bucket_name:
		print('(Just created) --> {} - there since {}'.format(
			bucket['Name'], bucket['CreationDate']))

object_key = 'python_sample_key.txt'
print('Uploading some data to {} with key: {}'.format(
	bucket_name,object_key))
s3client.put_object(Bucket=bucket_name, Key=object_key, Body=b'Hello World..!!')

url = s3client.generate_presigned_url(
	'get_object', {'Bucket': bucket_name, 'Key': object_key})
print('\n Try this URL in your browser to download the object:')
print(url)

try:
	input = raw_input
except NameError:
	pass
input("\n Press enter to continue...")

print('\nNow using Resource API')
s3resource = boto3.resource('s3')
bucket = s3resource.Bucket(bucket_name)
obj = bucket.Object(object_key)
print('Bucket name. {}'.format(bucket.name))
print('Object key: {}'.format(obj.key))
print('Object content length:{}'.format(obj.content_length))
print('Object body: {}'.format(obj.get()['Body'].read()))
print('Object last modified: {}'.format(obj.last_modified))

print('\nDeleting all objects in bucket {}'.format(bucket_name))
delete_responces = bucket.objects.delete()
for delete_response in delete_responces:
	for deleted in delete_response['Deleted']:
		print('\t Deleted: {}'.format(deleted['Key']))

print('\nDeleting the bucket.')
bucket.delete()
