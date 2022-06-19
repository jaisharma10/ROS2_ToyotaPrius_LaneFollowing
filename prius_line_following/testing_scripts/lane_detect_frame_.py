
import cv2
import numpy 

image = cv2.imread('/home/jaisharma/Pictures/imageRoad.png')

print("Image Size: ", image.shape)


##### Segmentation
light_line = numpy.array([10,10,10])
dark_line = numpy.array([153,153,153])
mask = cv2.inRange(image, light_line,dark_line)


##### Boundaries Extraction
canny= cv2.Canny(mask,20,200)
r1=600; c1=0
img = canny[r1:r1+161,c1:c1+1499]

cv2.imshow('output image',img)


# ##### Finding Line  Mid point
edge=[]
for i in range (1499):
    if(img[160,i]==255):
        edge.append(i)
print("Edges: ", edge)

# ## We only need two points # one from left line # second from right line # When values are 4
if(len(edge)==4):
    edge[0]=edge[0]
    edge[1]=edge[2]
    
# ## When Values are 3 and if they are 2 we donot need to process them. If the values of pixels is greater then 5 then they are adjecent to eachother
if(len(edge)==3):
    for i in range(len(edge)):
        if(edge[1] - edge[0] > 5):        ## meaning idx(0) and idx(1) are ok [193, 506, 507 ]
            edge[0]=edge[0]
            edge[1]=edge[1]
        else:                             #[193, 194, 507 ]
            edge[0]=edge[0]
            edge[1]=edge[2]
            
# ## Apllying a white pixel to final line mid point found
mid_area=(edge[1]-edge[0])
laneMid = int(edge[0] + (mid_area/2))
img[160,int(laneMid)] = 255

# ##### Finding Frame Mid point
midFrame = int(image.shape[1]/2)

# ##### Controlling the car process
error = midFrame - laneMid 
if(error < 0):## go left
    action="Go Right"
else :
    action="Go Left"

# ## Writing on the Frame as output for better understanding
finalImg = cv2.putText(img, action, (50,50), cv2.FONT_HERSHEY_SIMPLEX, 1, (255,0,), 2, cv2.LINE_AA)
finalImg = cv2.line(finalImg, (midFrame,20), (midFrame,140), (128,128,0), 5) 
finalImg = cv2.line(finalImg, (midFrame - 10,80), (midFrame + 10,80), (128,128,0), 5) 
finalImg = cv2.line(finalImg, (laneMid,20), (laneMid,140), (128,0,255), 5) 
finalImg = cv2.line(finalImg, (laneMid - 10,80), (laneMid + 10,80), (128,128,0), 5) 

print("Error:",error," || Middle of Camera Frame:",midFrame,"  ||  Middle of Lane:",laneMid)

im_rgb = cv2.cvtColor(finalImg, cv2.COLOR_RGB2BGR)
cv2.imshow('final output image',finalImg)
cv2.waitKey(0)
cv2.destroyAllWindows()
