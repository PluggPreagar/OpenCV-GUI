import cv2 as cv 
import sys

def fox(image, operation_type, morph_type, kernel_size, iterations, edge_threshold, blob_removal_threshold):
    # raise Exception('fox')
    print("fox: " + str(kernel_size))
    # img2 = cv.GaussianBlur(image, (kernel_size, kernel_size), 0)
    rows,cols,_ = image.shape
    # init array x_last_up with size of len(cols)
    x_last_up = [0] * rows

    # gray
    for i in range(rows):
        for j in range(cols):
            k = image[i,j]
            x = (int(k[0]) + int(k[1]) + int(k[2])) / 3
            image[i][j] = [ x, x, x]
    print("fox: grayed DONE" )
    # clone image
    img2 = image.copy()
    for i in range(rows):
        for j in range(cols):
            # avg color in 9x9 around pixel
            v = 0
            for l in range(-10,10):
                for m in range(-10,10):
                    # sum up brightness around pixel
                    if i+l >= 0 and i+l < rows and j+m >= 0 and j+m < cols:
                        v += image[i+l][j+m][1]
                    else:
                        v += image[i][j][1]
            v /= 11*11                  # avg brightness
            v = img2[i][j][0] - v       # color - avg brightness
            img2[i][j] = [ v, v, v]     # set pixel to color - avg brightness
    print("fox: black-white DONE" )
    print ("")
    return img2
