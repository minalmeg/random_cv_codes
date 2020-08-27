#code to detect bottle using opencv only
import cv2
import numpy as np
import imutils

cap = cv2.VideoCapture(0)
frame_width = int( cap.get(cv2.CAP_PROP_FRAME_WIDTH))

frame_height =int( cap.get( cv2.CAP_PROP_FRAME_HEIGHT))

fourcc = cv2.VideoWriter_fourcc('X','V','I','D')

out = cv2.VideoWriter("output.avi", fourcc, 30, (1280,720))
fgbg = cv2.createBackgroundSubtractorMOG2()

ret, frame1 = cap.read()
ret, frame2 = cap.read()
print(frame1.shape)
while cap.isOpened():
    diff = cv2.absdiff(frame1, frame2)
    gray = fgbg.apply(diff)
    #gray = cv2.cvtColor(diff, cv2.COLOR_BGR2GRAY)
    tot_area = gray.size
    tot_h, tot_w = gray.shape
    blur = cv2.GaussianBlur(gray, (5,5), 0)
    _, thresh = cv2.threshold(blur, 127, 255, cv2.THRESH_BINARY+cv2.THRESH_OTSU)
    dilated = cv2.dilate(thresh, None, iterations=3)
    cv2.imshow("feed1", dilated)
    contours, _ = cv2.findContours(dilated, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

    for contour in contours:
        (x, y, w, h) = cv2.boundingRect(contour)

        aspect_ratio = float(h)/w

        area = cv2.contourArea(contour)

        if 8000 < area < 14000 and 2 < aspect_ratio < 10:
            cv2.rectangle(frame1, (x, y), (x + w, y + h), (0, 255, 0), 2)
            print(aspect_ratio)
            print(area)
            print(w,h)
    #cv2.drawContours(frame1, contours, -1, (0, 255, 0), 2)

    image = cv2.resize(frame1, (1280,720))
    out.write(image)
    cv2.imshow("feed", frame1)
    frame1 = frame2
    ret, frame2 = cap.read()
    if cv2.waitKey(40) == 27:
        break

cv2.destroyAllWindows()
cap.release()
out.release()
