"""

Process input camera frame using openCV
Implement lane detection and lane following algorithm

"""


import cv2
import numpy 
import rclpy
from rclpy.node import Node 
from cv_bridge import CvBridge 
from sensor_msgs.msg import Image 
from geometry_msgs.msg import Twist

class laneFollowing(Node):
    def __init__(self):
        super().__init__('Lane_follower')
        
        # subscribe raw camera data, publish corrected velocities
        self.subscriber = self.create_subscription(Image,'/camera/image_raw',self.processFrame,10)
        self.bridge = CvBridge()                                    
        self.publisher = self.create_publisher(Twist, '/cmd_vel', 40)    #periodic publisher call
        
        timer_period = 0.2
        self.timer = self.create_timer(timer_period, self.updateVel)
        
        # Global Variables
        self.velocity = Twist()
        self.error = 0
        self.action = ""

    ## Publisher Call back --> update velocity    
    def updateVel(self):
        
        self.velocity.linear.x = 0.90  # constant linear velocity
        
        # correct path, update angular velocity
        if(self.error > 0):             
            self.velocity.angular.z = 0.15
            self.action="Go Left"
        else :                          
            self.velocity.angular.z = -0.15
            self.action="Go Right"

        self.publisher.publish(self.velocity) # Publishing updated velocities


    ## Subscriber Call Back --> process input camera frame
    
    def processFrame(self, data): 
        frame = self.bridge.imgmsg_to_cv2(data)  # get 1 frame
        # print("Image Size: ", frame.shape)
        height = frame.shape[0]
        width = frame.shape[1]

        ##### Segmentation
        light_line = numpy.array([20,20,20])
        dark_line = numpy.array([120,120,120])
        maskImg = cv2.inRange(frame, light_line,dark_line)
        
        ##### Boundaries Extraction
        cannyImg = cv2.Canny(maskImg,40,20)       
        r1=150;c1=0
        img = cannyImg[r1:r1+161,c1:c1+640]  # crop image

        ##### Finding a midpoint between lane edges
        edge=[]
        for i in range (width):
            if(img[160,i]==255): 
                edge.append(i)
        print("List of Edges: ", edge)

        if(len(edge)==4): # 4 edges recorded
            edge[0]=edge[0]
            edge[1]=edge[2]
            
        if(len(edge)==3): # 3 edges recorded
            for i in range(len(edge)):
                if(edge[1]-edge[0] > 5): 
                    edge[0]=edge[0]
                    edge[1]=edge[1]
                else:
                    edge[0]=edge[0]
                    edge[1]=edge[2]
                    
        if(len(edge) < 2): # 1 or 0 edges recorded
            edge=[240,440]
        
        ## Apllying a white pixel to final line mid point found
        mid_area =(edge[-1]-edge[0])
        lane_middle = int(edge[0] + (mid_area/2))
        frame_middle = int(width/2)                   # middle of camera frame
        self.error = frame_middle - lane_middle       # orientation error

        ## Writing on the Frame as output for better understanding
        finalImg = cv2.putText(img, self.action, (20,30), cv2.FONT_HERSHEY_SIMPLEX, 1, (255,0,0), 2, cv2.LINE_AA)
        finalImg = cv2.line(finalImg, (lane_middle,20), (lane_middle,140), (128,0,255), 5) 
        finalImg = cv2.line(finalImg, (lane_middle - 20,80), (lane_middle + 20,80), (128,128,0), 5)
        finalImg = cv2.line(finalImg, (frame_middle,80+27), (frame_middle,80-27), (255,255,255), 3) 
        finalImg = cv2.line(finalImg, (frame_middle - 27,80), (frame_middle + 27,80), (255,255,255), 3)  
        finalImg = cv2.circle(finalImg, (frame_middle, 80), 22, (255,255,255), 3)
        (finalImg, (lane_middle - 20,80), (lane_middle + 20,80), (128,128,0), 5) 

        
        cv2.imshow('Output Image',finalImg)
        cv2.waitKey(1)
        
    cv2.waitKey(0)
    cv2.destroyAllWindows()


def main(args=None):
  rclpy.init(args=args)
  image_subscriber = laneFollowing()
  rclpy.spin(image_subscriber)
  rclpy.shutdown()
  
if __name__ == '__main__':
  main()