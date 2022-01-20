# MotionSensor
Low-cost motion detection with Deep Learning for home security.

Project consists of 2 elements, the first being a Python script that conducts motion detection (Motion_Detection.py) and a Python notebook file (yolov4_webcam.ipynb) which conducted the object detection via Deep Learning Neural Network.

Motion_Detection.py:
Opens the IP camera feed as an input stream object using OpenCV. The first frame is captured as the background image and is used as the reference image for background subtraction algorithm. Once the background image is captured, the camera feed is then processed using various image filtering techniques to reduce noise and omit unneccessary data. Any deviance in feed material relative to what is seen in the background frame will be picked up by the pixel difference function which subtracts pixel values from the grey-scale background image and the grey-scale camera feed. Each pixel difference is compared to a threshold value where pixel differences exceeding the threshold value are triggered to 255 (White). The threshold value is modulated according to the time of day to account for lighting. This efffectively creates a silhouette around the intrusive body. OpenCV's contour function is used to then determine whether the silhouette is large enough to constitute a human being, in the case that it is large enough, the camera feed is captured as a .PNG file. Finally, OpenCV's Laplacian function is used to determine the blurriness of the image captured as it compares frame by frame the footage of the intrusive element to determine the least blurry image to store.

yolov4_webcam.ipynb
This Python Notebook script was used to train the YOLOv4 neural network on 12000 images of humans and common household pets. 

