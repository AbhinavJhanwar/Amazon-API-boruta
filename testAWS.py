# -*- coding: utf-8 -*-
"""
Created on Fri Mar  8 16:34:00 2019

@author: abhinav.jhanwar
"""


import boto3
import cv2
import json
import paho.mqtt.client as mqtt
from time import time
import imutils
from PIL import ImageFont, ImageDraw, Image
import numpy as np
import os

class awsDetection:
    # categorise emotions
    positiveEmotions = ['HAPPY']
    negativeEmotions = ['DISGUSTED', 'SAD', 'ANGRY']
    neutralEmotinos = ['CONFUSED', 'CALM', 'SURPRISED']
    
    def __init__(self, camid):
        self.client = boto3.client('rekognition')
        with open('config.json') as outFile:
            config = json.load(outFile)
        self.collectionName = config["collectionName"]
        self.conf_threshold = config['conf_threshold']
        self.font_size = config['font_size']
        self.font_path = config['font_path']
        self.custom_font = config['custom_font']
        self.emotion = config['emotion']
        self.user_images = config['user_images']
        
    def searchUser(self, image):
        userDetails=[]
        try:
            response = self.client.search_faces_by_image(
            CollectionId=self.collectionName,
            Image={'Bytes': image},
            MaxFaces=1,
            FaceMatchThreshold=self.conf_threshold)
            #print(response['SearchedFaceBoundingBox'])
            
            if len(response['FaceMatches'])>0:
                confidence =  response['FaceMatches'][0]['Similarity']
                user = response['FaceMatches'][0]['Face']['ExternalImageId']
                userDetails.append({'user':user, 
                                        'confidence':float(confidence), 
                                        'BoundingBox':response['SearchedFaceBoundingBox']
                                    })
                return userDetails
            else:
                userDetails.append({'user':'1299', 
                                        'confidence':0, 
                                        'BoundingBox':response['SearchedFaceBoundingBox']
                                    })
                return userDetails
        except:
            return [None]

    def startDetection(self): 
        
        # start frames capturing timer
        start_time = time()
        frame_counter = 0
        fps=0
        
        for image in os.listdir(self.user_images):
            
            frame = cv2.imread(os.path.join(self.user_images, image))     
            
            # resize frame to increase processing speed
            #frame = imutils.resize(frame, width=400)
            (frame_height, frame_width) = frame.shape[:2]
            # encode image to be sent to aws server
            img_str = cv2.imencode('.jpg', frame)[1].tostring()
            
            # fetch user details from server
            user = self.searchUser(img_str)[0]
            #print(user)
            if user==None:
                continue
            
            box = user['BoundingBox']#faceDetail['BoundingBox']
            #print(box)
            left = int(frame_width * box['Left'])
            top = int(frame_height * box['Top'])
            width = int(frame_width * box['Width'])
            height = int(frame_height * box['Height'])
            
            bottom = top+height
            right = left+width   
            
            if self.emotion == "true":
                # fetch face details            
                response = self.client.detect_faces(Image={'Bytes': img_str},
                                    Attributes=['ALL'])
                if response['FaceDetails'] != []:
                    faceDetail = response['FaceDetails'][0]
                    emotion = sorted(faceDetail['Emotions'], key=lambda k: k['Confidence'])[-1]
                    if emotion['Confidence']<75:
                        emotion['Type'] = 'Neutral'
                    #print(emotion)
                    
                    if emotion['Type'] in self.positiveEmotions:
                        emotion['Type'] = 'Positive'
                    elif emotion['Type'] in self.negativeEmotions:
                        emotion['Type'] = 'Negative'
                    else:
                        emotion['Type'] = 'Neutral'
                       
            cv2.rectangle(frame, (left, top), (right, bottom), (255, 0, 0), 2)
            # Draw a label with a name below the face
            cv2.rectangle(frame, (left, bottom), (right, bottom+45), (255, 0, 0), cv2.FILLED)
            # put label for confidence
            cv2.rectangle(frame, (left, top-20), (right, top), (255, 0, 0), cv2.FILLED)
                
            if self.custom_font == "True":
                font = ImageFont.truetype(self.font_path, self.font_size)
                img_pil  = Image.fromarray(frame)
                draw = ImageDraw.Draw(img_pil)
                (b, g, r, a) = (255,255,255,0)
                draw.text((left+6, bottom+1), "ID: "+user['user'], font = font, fill = (b, g, r, a))
                if self.emotion=="true":
                    draw.text((left+6, bottom+21), emotion['Type'], font = font, fill = (b, g, r, a))
                draw.text((left+6, top-20), str(round(user['confidence'],2))+'%', font = font, fill = (b, g, r, a))
                frame = np.array(img_pil)
            else:
                font = cv2.FONT_HERSHEY_DUPLEX
                cv2.putText(frame, "FPS: %s"%str(round(fps,2)), (20, 20), font, 0.5, (255, 255, 255), 1)
                cv2.putText(frame, "ID: "+user['user'], (left+6, bottom+15), font, 0.5, (255, 255, 255), 1)
                if self.emotion=="true":
                    cv2.putText(frame, emotion['Type'], (left+6, bottom+30), font, 0.5, (255, 255, 255), 1)
                cv2.putText(frame, str(round(user['confidence'],2))+'%', (left+6, top-3), font, 0.5, (255, 255, 255), 1)
            
            # Display the resulting image
            cv2.imwrite('recognized_images/'+image, frame)
            # update the FPS counter
            frame_counter+=1
            fps = frame_counter / (time() - start_time)
            #print(fps)
         
        # stop the timer and display FPS information
        print("[INFO] elapsed time: {:.2f}".format(time() - start_time))
        print("[INFO] approx. FPS: {:.2f}".format(fps))
             
        
if __name__=="__main__":
    # initialize detection object
    face = awsDetection(0)
    
    # start face detection
    face.startDetection()
    