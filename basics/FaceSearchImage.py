# -*- coding: utf-8 -*-
"""
Created on Mon Jan  7 13:40:39 2019

@author: abhinav.jhanwar
"""

import boto3
from PIL import Image, ImageDraw, ExifTags, ImageColor
import glob, os
import cv2
from imutils.video import FPS

def initializeRekognition():
    client=boto3.client('rekognition')
    return client

# create collection for each application user
def createCollection(client, ID):
    response = client.create_collection(
    CollectionId=ID
    )
    return response

# delete collection
def deleteCollection(client, ID):
    response = client.delete_collection(
    CollectionId=ID
    )
    return response

# add images of an application user  
def addImages(client, ID, imageName):
    with open(imageName, 'rb') as image:
       response = client.index_faces(
            CollectionId=ID,
            Image={'Bytes': image.read()},
            ExternalImageId=ID,
            DetectionAttributes=[
                'DEFAULT',
            ],
            MaxFaces=123,
            QualityFilter='AUTO'
        )
    return response

# add application users
def addUsers(client, ID, user_images):
    createCollection(client, ID)
    for user in glob.glob(os.path.join(user_images,'*')):
        addImages(client, ID, user)

def searchUser(client, image):
    userDetails=[]

    Users = client.list_collections(
    MaxResults=123
    )['CollectionIds']
    #with open('Image1.jpg', 'rb') as image:
    #   image = image.read()
    for user in Users:
        response = client.search_faces_by_image(
            CollectionId=user,
            Image={'Bytes': image},
            MaxFaces=1,
            FaceMatchThreshold=70
        )
        
        if len(response['FaceMatches'])>0:
            confidence =  response['FaceMatches'][0]['Similarity']
            userDetails.append({'user':user, 
                                   'confidence':float(confidence), 
                                   'BoundingBox':response['FaceMatches'][0]['Face']['BoundingBox']
                                   })
    return userDetails

# training
def trainUsers(client):
    user_images = "data/"
    names=[]
    for user in glob.glob(os.path.join(user_images,'*')):
        names.append(user.split('\\')[-1])        
       
    for name in names:
        addUsers(client, name, "data/%s"%name)


# detection
users = searchUser('Image1.jpg')
user = sorted(users, key=lambda k: k['confidence'])[-1]
print(user)

users = searchUser('Image2.jpg')
user = sorted(users, key=lambda k: k['confidence'])[-1]
print(user)

users = searchUser('Image3.jpg')
user = sorted(users, key=lambda k: k['confidence'])[-1]
print(user)

users = searchUser('Image4.jpg')
user = sorted(users, key=lambda k: k['confidence'])[-1]
print(user)

users = searchUser('Image5.jpg')
user = sorted(users, key=lambda k: k['confidence'])[-1]
print(user)

users = searchUser('Image6.jpg')
user = sorted(users, key=lambda k: k['confidence'])[-1]
print(user)

def startDetection(client, camid=0):   
    video_capture = cv2.VideoCapture(camid)
    fps = FPS().start()
    while True:
        ret, frame = video_capture.read()   
        # validate if image is captured, else stop video capturing
        if ret!=True:
            print("\nCamera not detected")
            video_capture.release()
            cv2.destroyAllWindows()
            break
        
        (frame_height, frame_width) = frame.shape[:2]
        img_str = cv2.imencode('.jpg', frame)[1].tostring()
        
        users = searchUser(client, img_str)
        user = sorted(users, key=lambda k: k['confidence'])[-1]
        print("User: ",user['user'])
        
        response = client.detect_faces(Image={'Bytes': img_str},
                                        Attributes=['ALL'])
        # try with cropped face
        faceDetail = response['FaceDetails'][0]
        print('Age: ' + str(faceDetail['AgeRange']['Low'])
                + ' to ' + str(faceDetail['AgeRange']['High']))
        print('Gender: ' + str(faceDetail['Gender']['Value'])+ ', Confidence: '+str(faceDetail['Gender']['Confidence']))
        emotion = sorted(faceDetail['Emotions'], key=lambda k: k['Confidence'])[-1]
        print('Emotion: '+str(emotion['Type'])+ ', Confidence: '+str(emotion['Confidence']))
        print('Smile: '+str(faceDetail['Smile']['Value'])+', Confidence: '+str(faceDetail['Smile']['Confidence']))
        
        box = faceDetail['BoundingBox']
        left = int(frame_width * box['Left'])
        top = int(frame_height * box['Top'])
        width = int(frame_width * box['Width'])
        height = int(frame_height * box['Height'])
        
        bottom = top+height
        right = left+width
        
        cv2.rectangle(frame, (left, top), (right, bottom), (255, 0, 0), 2)
        
        # Draw a label with a name below the face
        cv2.rectangle(frame, (left, bottom), (right, bottom+20), (255, 0, 0), cv2.FILLED)
        font = cv2.FONT_HERSHEY_DUPLEX
        cv2.putText(frame, user['user'], (left + 6, bottom+15), font, 0.5, (255, 255, 255), 1)
        
        if user['user']!='Unknown':
            # put label for confidence
            cv2.rectangle(frame, (left, top-20), (right, top), (255, 0, 0), cv2.FILLED)
            cv2.putText(frame, str(round(user['confidence'],2))+'%', (left + 6, top-3), font, 0.5, (255, 255, 255), 1)
            
        # Display the resulting image
        #cv2.imwrite('out.jpg', frame)
        cv2.imshow('Face Recognition', frame)
    
        # Hit 'q' on the keyboard to quit!
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
        
        # update the FPS counter
        fps.update()
         
    # stop the timer and display FPS information
    fps.stop()
    print("[INFO] elapsed time: {:.2f}".format(fps.elapsed()))
    print("[INFO] approx. FPS: {:.2f}".format(fps.fps()))
         
    # Release handle to the webcam
    video_capture.release()
    cv2.destroyAllWindows()

startDetection(initializeRekognition())