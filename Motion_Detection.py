#importing all dependancies
import cv2
import time
import datetime
import imutils
from astral import LocationInfo
from astral.sun import sun



def motion_detection():
    global threshold
    
    # Location parameters defined for the Astral object
    city_name = 'Cape Town'
    longitude = -33.9249
    latitude = 18.4241
    
    t = time.localtime()
    hour = t.tm_hour
    year = t.tm_year
    day = t.tm_mday
    month = t.tm_mon
    
    city = LocationInfo(city_name, "SA", "Africa/Johannesburg", longitude, latitude) #Astral city object created
    s = sun(city.observer, date=datetime.date(year, month, day),tzinfo=city.timezone) #using the city object, a sun object was created to find the various times for sunrise,noon,sunset
    
    sunrise = int(s["sunrise"].strftime("%H"))
    noon = int(s["noon"].strftime("%H"))
    sunset = int(s["sunset"].strftime("%H"))
    
    print ('\n')
    print ('Sunrise in {} is at {}:{}.'.format(city_name,sunrise,s["sunrise"].strftime("%M") ))
    print ('Noon in {} is at {}:{}.'.format(city_name,noon,s["noon"].strftime("%M")))
    print ('Sunset in {} is at {}:{}.'.format(city_name,sunset,s["sunset"].strftime("%M")))
    print ('\n')
    
    local_time = hour
    print ('local time is ',local_time)
   
    print('Camera Feed Loading...')
    time.sleep(5) 
    img_counter=0
    #video_capture = cv2.VideoCapture() # value (0) selects the devices default camera
    video_capture = cv2.VideoCapture('rtsp://admin:ISYCSY@192.168.0.108:554/H.264') # to use IPcamera, one can feed the rtsp address of the camera into VideoCapture
    print('Camera Feed loaded successfully...')
    time.sleep(2)

    first_frame = None # declares first frame, this is the unprocessed background frame against which frames will be compared.
    i=0
    
    while True:

        i+=1
        if local_time >=0 and local_time < sunrise:
            frame = video_capture.read()[1]
            threshold = 50
            
        if local_time >= sunrise and local_time < noon: # morning time
            frame = video_capture.read()[1]
            threshold = 150
            
        if local_time >= noon and local_time < noon + 4: # afternoon time
            frame = video_capture.read()[1]
            threshold = 45       
                   
        if local_time >= noon + 4 and local_time < sunset: # evening time
            frame = video_capture.read()[1]
            threshold = 55
                    
        if local_time >= sunset: #night time
            frame = video_capture.read()[1]
            threshold = 50
        
        frame = video_capture.read()[1] # stores only the second output of the read function which is the image
        text = 'Unoccupied'

        greyscale_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY) # greyscales the frame
        
        ############
        # if i == 3:
            # cv2.imwrite('grey.png', greyscale_frame)
            # cv2.imwrite('background.png', first_frame)
            
        cv2.imshow('Grey Scale Footage', frame)
        ############
        gaussian_frame = cv2.GaussianBlur(greyscale_frame, (21,21),0) # convolving the grey scale frame with 21x21 Gaussian Kernel
        blur_frame = cv2.blur(gaussian_frame, (9,9))
        greyscale_image = blur_frame 
        greyscale_image = gaussian_frame 

        if first_frame is None:
            first_frame = greyscale_image #storage of the now processed background frame into first_frame
            cv2.imwrite('background.png', greyscale_frame)
        else:
            pass

        
        frame = imutils.resize(frame, width=500) #resizes the frame 
        frame_delta = cv2.absdiff(first_frame, greyscale_image) #finding the absolute greyscale pixel difference between the background frame and present frame
        
        
        #print('threshold is :  ', threshold)
        thresh = cv2.threshold(frame_delta, threshold, 255, cv2.THRESH_BINARY)[1] # the frame difference calculated above is then passed through a threshold with the modulated threshold value
        

        dilate_image = cv2.dilate(thresh, None, iterations=2)
        # dilate = dilate,grow,expand - the effect on a binary image(black background and white foregorund) is to enlarge/expand the white 

        cnt,_ = cv2.findContours(dilate_image.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)[-2:] # OpenCV's contour functions allow the machine to draw a countour around the pixel difference. 
        
        # the loop below finds the contours created within the delta frame 
        
        for c in cnt:
        
            if cv2.contourArea(c) > 20000: # if the contour is larger than the threshold, the code detects relevant movement. this allows only significantly sized objects to trigger motion.
                text = 'Occupied'
                print(cv2.Laplacian(frame, cv2.CV_64F).var())
                 
                cv2.imwrite('Pframe.png', frame)  
                if cv2.Laplacian(frame, cv2.CV_64F).var() > 400:
                    cv2.imwrite('decent.png', frame)
            else:
                pass



        font = cv2.FONT_HERSHEY_SIMPLEX # sets the timestamp font

        cv2.putText(frame, '{+} Room Status: %s' % (text), 
            (10,20), cv2.FONT_HERSHEY_SIMPLEX , 0.3, (0, 255, 0), 1)
        # frame is the image on wich the text will go. 0.5 is size of font, (0,0,255) is R,G,B color of font, 2 on end is LINE THICKNESS! OK :)


        cv2.imshow('Security Feed', frame)
        
        key = cv2.waitKey(1) & 0xFF 
        if key == ord('q'):
            cv2.destroyAllWindows()
            break
                


if __name__=='__main__':    
    motion_detection()










