# Amazon-API-boruta
implementation of boruta package from Amazon

################################################################################################################
################### Steps to setup AI environment ##############################################################
################################################################################################################

1) Download AI installer and install required softwares and libraries
	libraries installed - 	
		a) dlib
		b) imutils
		c) face_recognition
		d) opencv-python
		e) tqdm
		f) paho-mqtt
2) install aws sdk/api-
	a) open anaconda prompt 
		a) "pip install boto3"
		b) "pip install awscli"
		c) for details, visit - "https://docs.aws.amazon.com/cli/latest/userguide/install-windows.html"
3) configure aws-
	a) open anaconda prompt
	b) write command : "aws configure"
	c) enter following details as asked:
		i)   Access Key ID
		ii)  Secret Access Key
		iii) Default region name: 'ap-south-1'
		iv)  Default output format : 'json'
	d) for details, visit = "https://docs.aws.amazon.com/cli/latest/userguide/cli-configure-files.html"
4) For more details about aws api/sdk, visit - "https://docs.aws.amazon.com/rekognition/latest/dg/what-is.html"
							
################################################################################################################


################################################################################################################
################## Training face detection #####################################################################
################################################################################################################

1) Create folder 'data'
2) Add folders with images of persons to be trained inside data folder as following-
	a) Suppose persons to be trained are 'David' and 'Smith'
	b) Create two folders with names 'David' and 'Smith'
	c) Add all images of 'David' in folder 'David' and all images of 'Smith' in folder 'Smith'
3) open 'config.json' file and update the following configuration-
	a) "user_images" : "data"
	b) "bucket" : name of bucket to be created where all the user images will be stored
	c) "collectionName": name of collection to be created where all the images after encoding will be saved
4) run command to deploy images on bucket: 'python uploadImagesBucket.py'
5) run command to train images from bucket: 'python faceTraining.py'

################################################################################################################


################################################################################################################
################## Start face detection ########################################################################
################################################################################################################

1) open 'config.json' file and update the following configuration-
	a) "emotion":"true" for fetching user emotions otherwise "false"
3) open anaconda command prompt
4) run command: 'python FaceDetection.py'

################################################################################################################