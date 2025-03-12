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

def f_structure(img, kernel_open, kernel_dilation, kernel_erosion, dilerode_iterations):
    # raise Exception('fox')
    print("f_structure: gray and blur ..." )
    ## check if already gray
    if len(img.shape) != 2:
        print("f_structure: convert to gray ... (works only with gray images)")
        img = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
    # extract structure
    # https://docs.opencv.org/4.x/d9/d61/tutorial_py_morphological_ops.html
    if kernel_open >0:
        print("f_structure: open ... {}" .format(kernel_open))
        # create kernel
        kernel_open = kernel_open - kernel_open%2 + 1 # kernel must be odd
        kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (kernel_open,kernel_open))
        # create opening = remove noise
        img_open = cv2.morphologyEx(img, cv2.MORPH_OPEN, kernel)
        img = img_open
    # run loop X times
    for i in range(1, dilerode_iterations):
        if kernel_dilation >0:
            print("f_structure: dilation ... {}" .format(kernel_dilation))
            # create kernel
            kernel_size = kernel_dilation - kernel_dilation%2 + 1 # kernel must be odd
            kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (kernel_size,kernel_size))
            # create opening = remove noise
            img_open = cv2.morphologyEx(img, cv2.MORPH_DILATE, kernel, dilerode_iterations)
            img = img_open
        if kernel_erosion >0:
            print("f_structure: erosion ... {}" .format(kernel_erosion))
            # create kernel
            kernel_size = kernel_erosion - kernel_erosion%2 + 1 # kernel must be odd
            kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (kernel_size,kernel_size))
            # create opening = remove noise
            img_open = cv2.morphologyEx(img, cv2.MORPH_ERODE, kernel, dilerode_iterations)
            img = img_open
    #
    print ("")
    return img
