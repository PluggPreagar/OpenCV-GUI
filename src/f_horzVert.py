import cv2 as cv2
import sys
import numpy as np
import matplotlib.pyplot as plt


def show_wait_destroy(winname, img):
    if cv2.getWindowProperty(winname, cv2.WND_PROP_VISIBLE) <= 0:
    #    cv2.destroyWindow(winname)  # destroy previous window
        cv2.imshow(winname, img)
        cv2.moveWindow(winname, 500, 0)
    else:
        cv2.imshow(winname, img)
    #cv2.waitKey(0)
    #cv2.destroyWindow(winname)

def f_horzVert(img,  bright_min, bright_max,  horiz_size, vert_size, contour_rect):
    # raise Exception('fox')
    print("f_horzVert: gray and blur ..." )
    ## check if already gray
    if len(img.shape) != 2:
        print("f_horzVert: not gray ... (works only with gray images)")
        img_gray = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
    else:
        img_gray = img
    # create empty image
    # extract contours
    ret, img_thresh = cv2.threshold(img_gray, bright_min, bright_max, cv2.THRESH_BINARY)
    #
    # vertical lines kernel
    if horiz_size > 0:
        print("f_horzVert: erode and dilate horizontal lines {} ...".format(horiz_size))
        horizontalStructure = cv2.getStructuringElement(cv2.MORPH_RECT,(horiz_size,1) )
        img_horiz = cv2.erode(img_thresh, horizontalStructure)
        img_horiz = cv2.dilate(img_horiz, horizontalStructure)
    if vert_size > 0:
        print("f_horzVert: erode and dilate vertical lines {} ...".format(vert_size))
        verticalStructure = cv2.getStructuringElement(cv2.MORPH_RECT,(1,    vert_size) )
        img_vert = cv2.erode(img_thresh, verticalStructure)
        img_vert = cv2.dilate(img_vert, verticalStructure)
    # merge 2 images
    if horiz_size > 0 and vert_size > 0:
        print("f_horzVert: merge horizontal and vertical lines ...")
        img_thresh = cv2.bitwise_or(img_horiz, img_vert)
    elif horiz_size > 0:
        img_thresh = img_horiz
    elif vert_size > 0:
        img_thresh = img_vert
    # create contours - to draw rectangles
    if contour_rect:
        print("f_horzVert: draw rectangles ...{}".format(contour_rect))
        if horiz_size > 0:
            contours, hierarchy = cv2.findContours(img_horiz, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
            for i in range(len(contours)):
                x, y, w, h = cv2.boundingRect(contours[i])
                cv2.rectangle(img_thresh, (x, y), (x+w, y+h), (255, 255, 255), 1)
        #
        if vert_size > 0:
            contours, hierarchy = cv2.findContours(img_vert, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
            for i in range(len(contours)):
                x, y, w, h = cv2.boundingRect(contours[i])
                cv2.rectangle(img_thresh, (x, y), (x+w, y+h), (255, 255, 255), 1)
    print ("")
    return img_thresh
