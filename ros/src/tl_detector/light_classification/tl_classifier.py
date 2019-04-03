from styx_msgs.msg import TrafficLight
import numpy as np
import cv2
import os

class TLClassifier(object):
    def __init__(self):
        #TODO load classifier
        self.img_counter = 0
        """self.recorded_imgs_directory = '../../../recorded_imgs_classifier/'
            not os.path.exists(self.recorded_imgs_directory):
                edirs(self.recorded_imgs_directory)"""

    def get_classification(self, cv_image):
        """Determines the color of the traffic light in the image
        Args:
            image (cv2 image): image containing the traffic light
        Returns:
            int: ID of traffic light color (specified in styx_msgs/TrafficLight)
        """
        MIN_ACCEPTANCE_NUM_PIXELS = 50
        RED_MIN_ACCEPTANCE_NUM_PIXELS = 100
        
        font = cv2.FONT_HERSHEY_SIMPLEX
        cimg = cv_image
        hsv = cv2.cvtColor(cimg, cv2.COLOR_BGR2HSV)
        
        # color range
        lower_red_1 = np.array([0,100,100], dtype = "uint8")
        upper_red_1 = np.array([10,255,255], dtype = "uint8")
        
        lower_red_2 = np.array([160,100,100], dtype = "uint8")
        upper_red_2 = np.array([180,255,255], dtype = "uint8")
        
        lower_green = np.array([40,50,50], dtype = "uint8")
        upper_green = np.array([90,255,255], dtype = "uint8")
        
        lower_yellow = np.array([15,150,150], dtype = "uint8")
        upper_yellow = np.array([35,255,255], dtype = "uint8")
        
        red_mask_1 = cv2.inRange(hsv, lower_red_1, upper_red_1)
        red_mask_2 = cv2.inRange(hsv, lower_red_2, upper_red_2)
        
        green_mask = cv2.inRange(hsv, lower_green, upper_green)
        yellow_mask = cv2.inRange(hsv, lower_yellow, upper_yellow)
        red_mask = cv2.add(red_mask_1, red_mask_2)
        
        size = cimg.shape
        
        # hough circle detect
        r_circles = cv2.HoughCircles(red_mask, cv2.HOUGH_GRADIENT, 1, 80,
                                     param1=50, param2=10, minRadius=0, maxRadius=30)
        
        g_circles = cv2.HoughCircles(green_mask, cv2.HOUGH_GRADIENT, 1, 60,
                                     param1=50, param2=10, minRadius=0, maxRadius=30)
        
        y_circles = cv2.HoughCircles(yellow_mask, cv2.HOUGH_GRADIENT, 1, 30,
                                     param1=50, param2=5, minRadius=0, maxRadius=30)
        
        # traffic light detect
        r = 5
        bound = 4.0 / 10
        traffic_state = TrafficLight.UNKNOWN
        
        if r_circles is not None:
            r_circles = np.uint16(np.around(r_circles))

            for i in r_circles[0, :]:
                if i[0] > size[1] or i[1] > size[0]or i[1] > size[0]*bound:
                    continue

                h, s = 0.0, 0.0
                for m in range(-r, r):
                    for n in range(-r, r):
                        if (i[1]+m) >= size[0] or (i[0]+n) >= size[1]:
                            continue
                        h += red_mask[i[1]+m, i[0]+n]
                        s += 1
                        
                if h / s > MIN_ACCEPTANCE_NUM_PIXELS:
                    print("Traffic State RED")
                    traffic_state = TrafficLight.RED	
                    """cv2.circle(cimg, (i[0], i[1]), i[2]+10, (0, 255, 0), 2)
                    cv2.circle(red_mask, (i[0], i[1]), i[2]+30, (255, 255, 255), 2)
                    cv2.putText(cimg,'RED',(i[0], i[1]), font, 1,(255,0,0),2,cv2.LINE_AA)"""
                    
        elif g_circles is not None:
            g_circles = np.uint16(np.around(g_circles))

            for i in g_circles[0, :]:
                if i[0] > size[1] or i[1] > size[0] or i[1] > size[0]*bound:
                    continue

                h, s = 0.0, 0.0
                for m in range(-r, r):
                    for n in range(-r, r):
                        if (i[1]+m) >= size[0] or (i[0]+n) >= size[1]:
                            continue
                        h += green_mask[i[1]+m, i[0]+n]
                        s += 1
                
                if h / s > RED_MIN_ACCEPTANCE_NUM_PIXELS:
                    print("Traffic State Green")
                    traffic_state = TrafficLight.GREEN
        
        elif y_circles is not None:
            y_circles = np.uint16(np.around(y_circles))

            for i in y_circles[0, :]:
                if i[0] > size[1] or i[1] > size[0] or i[1] > size[0]*bound:
                    continue

                h, s = 0.0, 0.0
                for m in range(-r, r):
                    for n in range(-r, r):
                        if (i[1]+m) >= size[0] or (i[0]+n) >= size[1]:
                            continue
                        h += yellow_mask[i[1]+m, i[0]+n]
                        s += 1
                
                if h / s > MIN_ACCEPTANCE_NUM_PIXELS:
                    print("Traffic State Yellow")
                    traffic_state = TrafficLight.YELLOW
 
        else:
            print(" UNKOWN, Maybe RED")  #In Case we Can't Detect the right colour
            self.img_counter += 1 
            traffic_state = TrafficLight.RED

        return traffic_state
