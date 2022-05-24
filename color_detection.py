import cv2
import argparse
import pandas as pd
import numpy as np

#taking image from user using args and openCV
ap = argparse.ArgumentParser()
ap.add_argument('-i','--image',required=True, help="Image path")
args = vars(ap.parse_args())
img_path = args['image']
img = cv2.imread(img_path) 

#reading dataset using pandas and giving names to each columns
index = ["color", "color_name", "hex", "R", "G", "B"]
csv = pd.read_csv('colors.csv', names = index, header = None)

#declaring global variables
clicked = False
r = g = b = xpos = ypos = 0


#Calculating distance ->> d = abs(Red – ithRedColor) + (Green – ithGreenColor) + (Blue – ithBlueColor) to get name of color

def get_colorname (R,G,B):
    minimum = 10000
    for i in range(len(csv)):
        d = abs(R - int(csv.loc[i,"R"])) + abs(G - int(csv.loc[i,"G"])) + abs(B - int(csv.loc[i,"B"]))
        if d<=minimum:
            minimum = d
            cname = csv.loc[i,"color_name"]
    return cname

def draw_function(event, x, y, flags, param) :
    if event == cv2.EVENT_LBUTTONDBLCLK:
        global b, g, r, xpos, ypos, clicked 
        clicked = True
        xpos = x
        ypos = y
        b,g,r = img[y,x]
        b = int(b)
        g = int(g)
        r = int(r)


#creating a window and a "callback"
cv2.namedWindow('image')
cv2.setMouseCallback('image',draw_function)

while(1):
    cv2.imshow("image",img)
    if (clicked) :

        #creates a rectangle to display text, showing what the color is
        #cv2.rectangle(image, startpoint, endpoint, color, thickness)-1 fills entire rectangle 
        cv2.rectangle(img, (20,20), (750,60), (b,r,g) -1)

        #creating color+rgb values
        text = get_colorname(r,g,b) + 'R='+str(r) + ' G='+ str(g) +  ' B='+ str(b)

        #cv2.putText(img,text,start,font(0-7),fontScale,color,thickness,lineType )
        cv2.putText(img, text,(50,50),2,0.8,(255,255,255),2,cv2.LINE_AA)

        #for very light colors, the text shall be displayed in black color
        if r+g+b>=600:
            cv2.putText(img, text, (50,50),2,0.8,(0,0,0),2,cv2.LINE_AA)

        clicked = False

    #Break the loop is esc is pressed
    if cv2.waitKey(20) & 0xFF ==27:
        break

cv2.destroyAllWindows()
