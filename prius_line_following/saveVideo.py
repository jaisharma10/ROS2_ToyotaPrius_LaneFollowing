'''
--> Record and Save Camera footage
--> Camera sensor plug-in, "camera/image_raw" topic to obtain frames
--> Image recieved as ROS mesg type, converted to OPENCV type then saved into a video
'''

import rclpy 
import cv2 
from rclpy.node import Node 
from cv_bridge import CvBridge  # converts between ROS Image messages and OpenCV images
from sensor_msgs.msg import Image 


class getVideo(Node):
  def __init__(self):
    super().__init__('imageSubscribers')     # node name 
    
    # subscribe from camera/image_raw
    self.subscriber = self.create_subscription(Image,'/camera/image_raw',self.processFrame,10)
    
    ## save video
    self.output = cv2.VideoWriter('/home/jaisharma/frontCamera.avi',cv2.VideoWriter_fourcc('M','J','P','G'), 10, (640,480))
    self.bridge = CvBridge()  # converting ros images to opencv data
 
  ## Subscriber callback function 
  def processFrame(self, data): 
    frame = self.bridge.imgmsg_to_cv2(data)     # ROS Image messages ----> OpenCV images
    self.output.write(frame)                    # write image
    cv2.imshow("output", frame)                 # display image 
    cv2.waitKey(1)   

  
def main(args=None):
  rclpy.init(args=args)
  imageSubscriber = getVideo()
  rclpy.spin(imageSubscriber)
  rclpy.shutdown()
  
if __name__ == '__main__':
  main()