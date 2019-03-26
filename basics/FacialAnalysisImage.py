# -*- coding: utf-8 -*-
"""
Created on Fri Jan  4 16:15:45 2019

@author: abhinav.jhanwar
"""

import boto3
import io
from PIL import Image, ImageDraw, ExifTags, ImageColor

# from bucket
bucket="bucket"
photo="test.jpg"
client=boto3.client('rekognition')
# Load image from S3 bucket
s3_connection = boto3.resource('s3')
s3_object = s3_connection.Object(bucket,photo)
s3_response = s3_object.get()
stream = io.BytesIO(s3_response['Body'].read())
image=Image.open(stream)

# Call DetectFaces
response = client.detect_faces(Image={'S3Object': {'Bucket': bucket, 'Name':
photo}},
Attributes=['ALL'])
imgWidth, imgHeight = image.size
draw = ImageDraw.Draw(image)

# calculate and display bounding boxes for each detected face
print('Detected faces for ' + photo)
for faceDetail in response['FaceDetails']:
    print('Age: ' + str(faceDetail['AgeRange']['Low'])
    + ' to ' + str(faceDetail['AgeRange']['High']))
    print('Gender: ' + str(faceDetail['Gender']['Value'])+ ', Confidence: '+str(faceDetail['Gender']['Confidence']))
    emotion = sorted(faceDetail['Emotions'], key=lambda k: k['Confidence'])[-1]
    print('Emotion: '+str(emotion['Type'])+ ', Confidence: '+str(emotion['Confidence']))
    print('Smile: '+str(faceDetail['Smile']['Value'])+', Confidence: '+str(faceDetail['Smile']['Confidence']))
    
    box = faceDetail['BoundingBox']
    left = imgWidth * box['Left']
    top = imgHeight * box['Top']
    width = imgWidth * box['Width']
    height = imgHeight * box['Height']

    #print('Left: ' + '{0:.0f}'.format(left))
    #print('Top: ' + '{0:.0f}'.format(top))
    #print('Face Width: ' + "{0:.0f}".format(width))
    #print('Face Height: ' + "{0:.0f}".format(height))
    points = (
    (left,top),
    (left + width, top),
    (left + width, top + height),
    (left , top + height),
    (left, top)
    )
    draw.line(points, fill='#00d400', width=2)
    # Alternatively can draw rectangle. However you can't set line width.
    #draw.rectangle([left,top, left + width, top + height], outline='#00d400')
image.show()


'''
[{
  'Beard': {'Confidence': 79.90170288085938, 'Value': True},
  'Eyeglasses': {'Confidence': 99.99618530273438, 'Value': False},
  'EyesOpen': {'Confidence': 96.84457397460938, 'Value': True},
  'Landmarks': [{'Type': 'eyeLeft',
    'X': 0.5627356171607971,
    'Y': 0.30098459124565125},
   {'Type': 'eyeRight', 'X': 0.6174402236938477, 'Y': 0.31760984659194946},
   {'Type': 'mouthLeft', 'X': 0.5603717565536499, 'Y': 0.4088324010372162},
   {'Type': 'mouthRight', 'X': 0.6054759621620178, 'Y': 0.4223947525024414},
   {'Type': 'nose', 'X': 0.5953547358512878, 'Y': 0.357596755027771},
   {'Type': 'leftEyeBrowLeft',
    'X': 0.5402904748916626,
    'Y': 0.2736532390117645},
   {'Type': 'leftEyeBrowRight',
    'X': 0.5797439217567444,
    'Y': 0.26968157291412354},
   {'Type': 'leftEyeBrowUp',
    'X': 0.5621218085289001,
    'Y': 0.26184701919555664},
   {'Type': 'rightEyeBrowLeft',
    'X': 0.6120389103889465,
    'Y': 0.2797643542289734},
   {'Type': 'rightEyeBrowRight',
    'X': 0.6376280188560486,
    'Y': 0.30277881026268005},
   {'Type': 'rightEyeBrowUp',
    'X': 0.6270157098770142,
    'Y': 0.2809092402458191},
   {'Type': 'leftEyeLeft', 'X': 0.5519211888313293, 'Y': 0.2994045317173004},
   {'Type': 'leftEyeRight', 'X': 0.5732941627502441, 'Y': 0.3055078983306885},
   {'Type': 'leftEyeUp', 'X': 0.5634486675262451, 'Y': 0.29604533314704895},
   {'Type': 'leftEyeDown', 'X': 0.5628655552864075, 'Y': 0.30605438351631165},
   {'Type': 'rightEyeLeft', 'X': 0.6058746576309204, 'Y': 0.31518787145614624},
   {'Type': 'rightEyeRight',
    'X': 0.6248180866241455,
    'Y': 0.32064002752304077},
   {'Type': 'rightEyeUp', 'X': 0.6175230145454407, 'Y': 0.31183740496635437},
   {'Type': 'rightEyeDown', 'X': 0.6161504983901978, 'Y': 0.3215113580226898},
   {'Type': 'noseLeft', 'X': 0.5789378881454468, 'Y': 0.37135234475135803},
   {'Type': 'noseRight', 'X': 0.5983237624168396, 'Y': 0.37744641304016113},
   {'Type': 'mouthUp', 'X': 0.5875157713890076, 'Y': 0.39867475628852844},
   {'Type': 'mouthDown', 'X': 0.5837051272392273, 'Y': 0.4314306080341339},
   {'Type': 'leftPupil', 'X': 0.5627356171607971, 'Y': 0.30098459124565125},
   {'Type': 'rightPupil', 'X': 0.6174402236938477, 'Y': 0.31760984659194946},
   {'Type': 'upperJawlineLeft',
    'X': 0.5109677910804749,
    'Y': 0.3078773021697998},
   {'Type': 'midJawlineLeft',
    'X': 0.5172461867332458,
    'Y': 0.4228249490261078},
   {'Type': 'chinBottom', 'X': 0.5749937295913696, 'Y': 0.4896162748336792},
   {'Type': 'midJawlineRight',
    'X': 0.6156917214393616,
    'Y': 0.45143237709999084},
   {'Type': 'upperJawlineRight',
    'X': 0.6335182189941406,
    'Y': 0.34359297156333923}],
  'MouthOpen': {'Confidence': 82.23115539550781, 'Value': False},
  'Mustache': {'Confidence': 81.64325714111328, 'Value': False},
  'Pose': {'Pitch': 8.390246391296387,
   'Roll': 12.803567886352539,
   'Yaw': 21.33740234375},
  'Quality': {'Brightness': 51.8549919128418, 'Sharpness': 83.14741516113281},
  'Sunglasses': {'Confidence': 99.99974060058594, 'Value': False}}]'''