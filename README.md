# MotionSensor

**Abstract**:

Home security is a concerning topic in a country like South Africa with its high crime rate. The security industry has many products available for end-users and this project aims to improve one of the most common ones which are motion detection systems. These systems rely on consistently accurate and fast computational algorithms to alert end-users of any intrusive bodies in their homes or whatever rooms they wish to monitor. These sensors in reality struggle with sensitivity issues and thus must be improved upon for the sake of the South African quality of life.
This project was implemented through the use of a camera with night vision capabilities alongside two python scripts. The first would handle a motion detector and the second would be a Deep Learning based object detector on the YOLOv4 model. The motion detector was tasked with detecting motion and then capturing an image of the intrusive body and sending that image to the object detector for further analysis. Through various tests and experiments, various image processing techniques and a background subtraction technique were applied to the motion detection algorithm to enhance the accuracy and robustness of the detector. The testing conducted on the YOLO model showed how robust the model on image quality is as well its exceptional inference time thus making it an effective solution for home security object detection.

Project consists of 2 elements, the first being a Python script that conducts motion detection (Motion_Detection.py) and a Python notebook file (yolov4_webcam.ipynb) which conducted the object detection via Deep Learning Neural Network.

**Motion_Detection.py**:

Opens the IP camera feed as an input stream object using OpenCV. The first frame is captured as the background image and is used as the reference image for background subtraction algorithm. Once the background image is captured, the camera feed is then processed using various image filtering/processing techniques to reduce noise and omit unneccessary data. Any deviance in feed material relative to what is seen in the background frame will be picked up by the pixel difference function which subtracts pixel values from the grey-scale background image and the grey-scale camera feed. Each pixel difference is compared to a threshold value where pixel differences exceeding the threshold value are triggered to 255 (White). The threshold value is modulated according to the time of day to account for lighting. This efffectively creates a silhouette around the intrusive body. OpenCV's contour function is used to then determine whether the silhouette is large enough to constitute a human being, in the case that it is large enough, the camera feed is captured as a .PNG file. Finally, OpenCV's Laplacian function is used to determine the blurriness of the image captured as it compares frame by frame the footage of the intrusive element to determine the least blurry image to store.

**yolov4_webcam.ipynb**:

This Python Notebook script was used to train the YOLOv4 neural network on 12000 images of humans and common household pets. The network trained upon was the pre-trained network from https://github.com/AlexeyAB which uses https://github.com/pjreddie/darknet Darknet53 Neural Network Model as a backbone. The model was trained on Google Colab using their backend NVIDIA Tesla K80 GPU and was trained till the model reached accuracy of 85%. To the credit of https://www.youtube.com/c/TheAIGuy/about, who provided code for testing out a trained model on images in Google Colab, I was able to conduct validation testing of my model with satisfactory results.

**Credits**:

https://github.com/AlexeyAB - For his guide on how to train a model on Google Colab as well as the YOLOv4 paper he co-published.
https://github.com/pjreddie/darknet - For open-sourcing the backbone DarkNet53 Neural Network upon which YOLOv4 operates.
https://www.youtube.com/c/TheAIGuy/about - For code to test out detection on images in Google Colab

The full project document along with all relevant literature is included in this repository. For any questions/queries, please feel free to contact me at bmtaki335@gmail.com

