import cv2 as cv2
import sys
import numpy as np

def show_wait_destroy(winname, img):
    if cv2.getWindowProperty(winname, cv2.WND_PROP_VISIBLE) <= 0:
    #    cv2.destroyWindow(winname)  # destroy previous window
        cv2.imshow(winname, img)
        cv2.moveWindow(winname, 500, 0)
    else:
        cv2.imshow(winname, img)
    #cv2.waitKey(0)
    #cv2.destroyWindow(winname)

def fox04(img, kernel, kernel_backgr, backr_prozent, kernelNeg, low, high, votes, min_len, max_gap):
    # raise Exception('fox')
    print("fox04: gray and blur ..." )
    ## check if already gray
    if len(img.shape) != 2:
        gray = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
    else:
        gray = img
    # kernel = 5
    kernel = kernel - kernel%2 + 1 # kernel must be odd
    blur_gray = cv2.GaussianBlur(gray,(kernel, kernel),0)
    # invert grayscale image
    print("fox04: invert image ..." )
    show_wait_destroy("gray", blur_gray)
    blur_gray = cv2.bitwise_not(blur_gray)
    show_wait_destroy("grayNot", blur_gray)

    img = blur_gray
    if kernel_backgr > 0:
        print("fox04: blur background ..." )
        kernel_backgr = kernel_backgr - kernel_backgr%2 + 1
        blur_backgr = cv2.GaussianBlur(img,(kernel_backgr, kernel_backgr),0)
        if backr_prozent < 100:
            blur_backgr = cv2.multiply(blur_backgr, np.array([backr_prozent/100]))
            t = np.array([backr_prozent/100])
            print( "t: {}".format(t[0]))
        img2 = cv2.subtract(img, blur_backgr)
        max_val = np.amax(img2)   # find brightest pixel
        print("max_val: {} ({} - backgr: {})".format(max_val, np.amax(img), np.amax(blur_backgr)))
        # normalize image
        img = cv2.multiply(img2, np.array([255 / max_val]))

    if low > 0:
        # detect vertical lines
        print("fox04: detect vertical lines ..." )
        # iamge negative
        img = cv2.bitwise_not(img)
        edges = cv2.Canny(img, low, high)
        img = cv2.cvtColor(edges, cv2.COLOR_GRAY2BGR)


    # create matrix for vertical and horizontal lines
    kernel_v = np.array([[-1,0,1],[-2,0,2],[-1,0,1]])
    kernel_h = np.array([[-1,-2,-1],[0,0,0],[1,2,1]])
    #



    #
    print ("")
    return img
