import cv2 as cv2
import sys
import numpy as np

def fox03(img, kernel, kernelNeg, low, high, votes, min_len, max_gap):
    # raise Exception('fox')
    print("fox03: gray and blur ..." )
    gray = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
    # kernel = 5
    kernel = kernel - kernel%2 + 1 # kernel must be odd
    blur_gray = cv2.GaussianBlur(gray,(kernel, kernel),0)
    img = blur_gray
    #
    #
    if kernelNeg > 0:
        print("fox03: blur_grayDiff ...")
        kernelNeg = kernelNeg - kernelNeg%2 + 1 # kernel must be odd
        blur_grayDiff = cv2.GaussianBlur(gray,(kernelNeg, kernelNeg),0)
        cv2.subtract(blur_grayDiff, blur_gray)
        img = blur_grayDiff

    #
    # Define our parameters for Canny
    #
    low_threshold = low # 50
    high_threshold = high # 150
    edges = cv2.Canny(blur_gray, low_threshold, high_threshold)
    #
    #
    #
    rho = 1  # distance resolution in pixels of the Hough grid
    theta = np.pi / 180  # angular resolution in radians of the Hough grid
    threshold = votes # 15  # minimum number of votes (intersections in Hough grid cell)
    min_line_length = min_len # 50  # minimum number of pixels making up a line
    max_line_gap = max_gap # 20  # maximum gap in pixels between connectable line segments
    line_image = np.copy(img) * 0  # creating a blank to draw lines on

    # Run Hough on edge detected image
    # Output "lines" is an array containing endpoints of detected line segments
    print("fox03: {} {} {} {} {} {}".format(rho, theta, threshold, min_line_length, max_line_gap, edges.shape))
    lines = cv2.HoughLinesP(edges, rho, theta, threshold, np.array([]),
                            min_line_length, max_line_gap)

    if not lines is None:
        print("lines: {}".format(lines.shape))
        for line in lines:
            for x1,y1,x2,y2 in line:
                cv2.line(line_image,(x1,y1),(x2,y2),(255,0,0),5)
    #
    #
    #
    #
    # Draw the lines on the  image
    lines_edges = cv2.addWeighted(img, 0.8, line_image, 1, 0)
    print ("")
    return img
