import cv2
import numpy as np
import math

sqrt_values = []
unique_sqrt_values = []

dict_cnt = {}
def color2gray(img):
    imgray = cv2.cvtColor(im, cv2.COLOR_BGR2GRAY)
    return imgray

def smoothen(img):
    img = cv2.GaussianBlur(imgray, (3, 3), 0)
    return img

def edge(img):
    img = cv2.Laplacian(img, cv2.CV_8U)
    ret, thresh = cv2.threshold(img, 7, 255, cv2.THRESH_BINARY)
    return thresh

def detectCircle(thresh):
    p = -1
    contours, hierarchy = cv2.findContours(thresh,cv2.RETR_TREE,cv2.CHAIN_APPROX_NONE)
    for cnt in contours: #looping through every contour in the image
        p = p+1 #storing position of contour
        #calculating center
        M = cv2.moments(cnt)
        if M['m00'] == 0:
            cx = int(M['m10'])
            cy = int(M['m01'])
        else:
            cx = int(M['m10'] / M['m00'])
            cy = int(M['m01'] / M['m00'])
        for i in cnt: #looping through the co-ordinates of each contour
            x,y = i[0,0],i[0,1] #x and y coordinates of the point on the contour
            #calculating distance from center(cx,cy) to the x and y coordinate aka radius if it's a circle
            t = (x-cx)*(x-cx)+(y-cy)*(y-cy)
            k = int(math.sqrt(t))
            sqrt_values.append(k)
        #finding the distinct values in the array
        for f in sqrt_values:
            if f not in unique_sqrt_values:
                unique_sqrt_values.append(f)
        #the value of k remains almost same for a circle whereas with other shapes it varies significantly
        #the contour with minimum no. of distinct values of k (radius) is a circle!
        o = len(unique_sqrt_values)
        dict_cnt[p] = o
    temp = min(dict_cnt.values())
        #retreiving position of contour with minimum variation
    res = [key for key in dict_cnt if dict_cnt[key] <= temp]
    for y in res:
        res = y
        #drawing the contour
    cnt = contours[res]
    img = cv2.drawContours(im, [cnt], 0, (0, 255, 0), 3)
    return img




    

im = cv2.imread('input1.jpg')
imgray = color2gray(im)
res = smoothen(imgray)
res = edge(res)
img = detectCircle(res)
cv2.imshow("", img)
cv2.waitKey()
cv2.imwrite("output.jpg",img)