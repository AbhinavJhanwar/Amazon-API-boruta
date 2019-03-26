# -*- coding: utf-8 -*-
"""
Created on Mon Jan  7 13:40:39 2019

@author: abhinav.jhanwar
"""

import boto3
import glob, os
import json
from tqdm import tqdm
import cv2
import imutils
from uploadImagesBucket import Bucket

class awsTraining():
    def __init__(self):
        self.client=boto3.client('rekognition')
        
        with open('config.json') as outFile:
            config = json.load(outFile)
        self.user_images = config['user_images']
        self.collectionName = config['collectionName']

    # create collection for each application user
    def createCollection(self):
        try:
            response = self.client.create_collection(
            CollectionId=self.collectionName
            )
            # reinitialize client to update collections
            self.client=boto3.client('rekognition')
            return response
        except:
            return None

    # delete collection
    def deleteCollection(self):
        response = self.client.delete_collection(
        CollectionId=self.collectionName
        )
        return response

    # add images of an application user  
    def addImages(self, ID, user_image):
        image = cv2.imread(user_image)
        image = imutils.resize(image, width=640)
        encode_param = [int(cv2.IMWRITE_JPEG_QUALITY), 90]
        image = cv2.imencode('.jpg', image,encode_param)[1].tostring()
        
        response = self.client.index_faces(
            CollectionId=self.collectionName,
            Image={'Bytes': image},
            ExternalImageId=ID,
            DetectionAttributes=[
                'DEFAULT',
            ],
            MaxFaces=1,
            QualityFilter='AUTO'
        )
        return response

    # add application users
    def addUsers(self, ID):
        for user_image in glob.glob(os.path.join(self.user_images+"/%s"%ID,'*')):
            self.addImages(ID, user_image)
            
    # training
    def trainUsers(self):
        IDs=[]
        for user in glob.glob(os.path.join(self.user_images,'*')):
            IDs.append(user.split('\\')[-1])  
        print("Training: ", IDs)
        
        # create collection to store images
        self.createCollection()
        
        # add users in collection
        for ID in tqdm(IDs):
            self.addUsers(ID)
    
    def trainUsersBucket(self):
        bucket = Bucket()
        # fetch all the images in bucket
        objects = bucket.listObjects()
                
        # create collection to store images
        self.createCollection()
        
        # fetch all the people already trained
        faces = aws.countFaces()['Faces']
        skipFaces = []
        for face in faces:
            skipFaces.append(face['ExternalImageId'])
        print("[INFO] Skipping Objects:", set(skipFaces))
            
        object_name=''
        for filename in tqdm(objects):
            if object_name == filename.split('/')[0]:
                pass
            else:
                object_name = filename.split('/')[0]
                print("[INFO] Processing Object:", object_name)
            
            if object_name in skipFaces:
                continue
                
            response = self.client.index_faces(
                CollectionId=self.collectionName,
                Image={'S3Object':
                                {'Bucket':bucket.bucket, 'Name':filename}
                            },
                ExternalImageId=object_name,
                DetectionAttributes=[
                    'DEFAULT',
                ],
                MaxFaces=1,
                QualityFilter='AUTO'
            )
            
        return objects
    
    def countFaces(self):
        response=self.client.list_faces(CollectionId=self.collectionName,
                           MaxResults=2000)
        print('Faces in collection:', len(response['Faces']))
        return response

if __name__=="__main__":
    # initialize training object
    aws = awsTraining()
    #aws.deleteCollection()
    # start training application users
    #aws.trainUsers()
    objects = aws.trainUsersBucket()
    # count faces
    faces = aws.countFaces()
    

