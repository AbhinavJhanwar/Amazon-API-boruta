# -*- coding: utf-8 -*-
"""
Created on Mon Jan  7 12:29:23 2019

@author: abhinav.jhanwar
"""

import boto3
from PIL import Image, ImageDraw, ExifTags, ImageColor

sourceFile='Image1.jpg'
targetFile='Image2.jpg'
client=boto3.client('rekognition')

imageSource = open(sourceFile,'rb')
imageTarget = open(targetFile,'rb')
response = client.compare_faces(SimilarityThreshold=70,
                                SourceImage={'Bytes': imageSource.read()},
                                TargetImage={'Bytes': imageTarget.read()})

for faceMatch in response['FaceMatches']:
    position = faceMatch['Face']['BoundingBox']
    confidence = str(faceMatch['Face']['Confidence'])
    print('The face at ' +
    str(position['Left']) + ' ' +
    str(position['Top']) +
    ' matches with ' + confidence + '% confidence')
    imageSource.close()
    imageTarget.close()