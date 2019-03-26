# -*- coding: utf-8 -*-
"""
Created on Fri Jan  4 12:37:10 2019

@author: abhinav.jhanwar
"""

import boto3

# Let's use Amazon S3
s3 = boto3.resource('s3')

# Print out bucket names
for bucket in s3.buckets.all():
    print(bucket.name)
    
# Upload a new file
data = open('3809.jpg', 'rb')
s3.Bucket('bucket').put_object(Key='group.jpg', Body=data)
