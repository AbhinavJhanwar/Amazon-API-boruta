# -*- coding: utf-8 -*-
"""
Created on Fri Jan  4 15:28:32 2019

@author: abhinav.jhanwar
"""

import boto3

# from s3 bucket
if __name__=="__main__":
    filename="farmer-looks-mountain-view.jpg"
    bucket="bucket"
    
    client=boto3.client('rekognition')
    
    response = client.detect_labels(Image={'S3Object':
        {'Bucket':bucket, 'Name':filename}})
    
    print('Detected labels for ' + filename)
    for label in response['Labels']:
        print(label['Name'] + ' : '+str(label['Confidence']))
        
# from local
import boto3
if __name__ == "__main__":
    imageFile='Image1.jpg'
    client=boto3.client('rekognition')
    
    # image should be base64-encoded string
    with open(imageFile, 'rb') as image:
        response = client.detect_labels(Image={'Bytes': image.read()})

    print('Detected labels in ' + imageFile)
    for label in response['Labels']:
        print (label['Name'] + ' : ' + str(label['Confidence']))
    print('Done...') 