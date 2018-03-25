import boto3
import re
s3r = boto3.resource('s3')
s3c = boto3.client('s3')

sizelimit = 1000000

response = s3c.list_buckets()

def formatnumber(item):
    return re.sub(r'(\d{3})(?=\d)',r'\1,',str(item)[::-1])[::-1]

for bucket in response['Buckets']:
    paginator = s3c.get_paginator('list_objects_v2')
    pageresponse = paginator.paginate(Bucket = bucket['Name'])
    for pageobject in pageresponse:
        if 'Contents' in pageobject.keys():
            for file in pageobject['Contents']:
                if file['StorageClass']!= 'Glacier':
                    itemtocheck = s3r.ObjectSummary(bucket['Name'],file['Key'])
                    if itemtocheck.size > sizelimit:
                        newlargeobject = dict()
                        newlargeobject['bucket'] = bucket['Name']
                        newlargeobject['file'] = file['Key']
                        newlargeobject['size'] = formatnumber(itemtocheck.size)
                        print(newlargeobject)
