# -*- coding: utf-8 -*-
"""
Created on Tue Jan 15 11:55:01 2019

@author: abhinav.jhanwar
"""

'''
# When you upload a file to Amazon S3, it is stored as an S3 object
# Objects consist of the file data and metadata that describes the object
# You can have an unlimited number of objects in a bucket
# The maximum size of a file that you can upload by using the Amazon S3 console is 78 GB
# can upload any file type—images, backups, data, movies
# can upload a folder which containes files
# assigns an object key name that is a combination of the uploaded file name and the folder name
'''

import boto3
import json
import glob
import os
from tqdm import tqdm

class Bucket:
    def __init__(self):
        self.s3 = boto3.resource('s3')

        # load configuration
        with open("config.json") as outFile:
            config = json.load(outFile)
        self.region = config['region']
        self.bucket = config['bucket']
        self.user_images = config['user_images']
         
    def createBucket(self):    
        # create bucket
        try:
            self.s3.create_bucket(Bucket=self.bucket, CreateBucketConfiguration={"LocationConstraint":self.region})
        except Exception as e:
            error = str(e)
            if error == "An error occurred (BucketAlreadyOwnedByYou) when calling the CreateBucket operation: Your previous request to create the named bucket succeeded and you already own it.":
                print("Bucket already available")
            else:
                print(error)
                
    def uploadImages(self):
        objects = bucket.listObjects()
        IDs=[]
        for user in glob.glob(os.path.join(self.user_images,'*')):
            IDs.append(user.split('\\')[-1])  
        print("Uploading Folders: ", IDs)
        
        for ID in tqdm(IDs):
            for user_image in glob.glob(os.path.join(self.user_images+"/%s"%ID,'*')):
                imageName = user_image.split('\\')[-1]
                objectKey = ID+"/"+imageName
                if objectKey not in objects:
                    self.s3.Object(self.bucket,ID+"/"+imageName).upload_file(Filename=user_image)
                else:
                    print('skipping object', objectKey, 'as already exists in bucket')

    def listObjects(self):
        # list all the object
        s3 = boto3.client('s3')
        kwargs = {'Bucket': self.bucket}
        keys = []
        
        while True:
            try:
                response = s3.list_objects_v2(**kwargs)
                for key in response['Contents']:
                    keys.append(key['Key'])
                try:
                    kwargs['ContinuationToken'] = response['NextContinuationToken']
                except KeyError:
                    break
            except:
                pass
            
        return keys
        
           
if __name__=="__main__":
    bucket = Bucket()
    #bucket.createBucket()
    objects = bucket.listObjects()
    print(len(objects))
    #bucket.uploadImages()


    

