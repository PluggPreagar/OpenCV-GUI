import cv2 as cv 
import sys
import numpy as np

def fox(image, operation_type, morph_type, kernel_size, iterations, edge_threshold, blob_removal_threshold):

    print("Fox - convert image to gray")
    rows,cols,_ = image.shape

    # gray
    for i in range(rows):
        for j in range(cols):
            k = image[i,j]
            x = (int(k[0]) + int(k[1]) + int(k[2])) / 3
            image[i][j] = [ x, x, x]
    # open cv blur image

    img2 = None
    if kernel_size > 1:
        print("fox - blur image {}x{}".format(kernel_size, kernel_size))
        # img2=cv.blur(img2, (kernel_size, kernel_size))
        img2=cv.GaussianBlur(image, (kernel_size*2+1, kernel_size*2+1), 0)
        for r in range(rows):
            for c in range(cols):
                l = image[r][c][0] - img2[r][c][0]
                # hard black or white
                l = 0 if l < 126 else 255
                image[r][c] = [ l, l, l]
    else:
        print("fox - no blur")
        img2 = image
    print ("")

    # enlarge white areas
    print("fox - enlarge white areas")
    # Detect edges using Canny
    if edge_threshold > 0 and blob_removal_threshold > 0:
        canny_output = cv.Canny(image, edge_threshold, edge_threshold * 2)
        contours, hierarchy = cv.findContours(canny_output, cv.RETR_EXTERNAL, cv.CHAIN_APPROX_NONE)
        # create empty output image with will contain only the biggest components
        img_onylBiggest = np.zeros_like(image)
        for contour in contours:
            area = cv.contourArea(contour)
            # print("contour: {}".format(contour))
            if area > blob_removal_threshold:
                print("Area: {} {}".format(area, contour.shape[0]))
                # fill the contour with white color
                cv.fillPoly(img_onylBiggest, [contour], [255, 255, 255])
                # remove the contour from the original image
                cv.fillPoly(image, [contour], [0, 0, 0])
            else:
                print("Area: {} - removed".format(area))
    else:
        img_onylBiggest = image


    return img2 if img2 is not None else image
