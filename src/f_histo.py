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

def f_histo(img, bright_low, bright_mid, bright_high):
    # raise Exception('fox')
    print("f_histo: gray and blur ..." )
    ## check if already gray
    if len(img.shape) != 2:
        print("f_histo: not gray ... (works only with gray images)")
        img_gray = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
    else:
        img_gray = img
    # create histogram of gray image
    # calc min, max and mean
    min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(img_gray)
    mean_val = cv2.mean(img_gray)
    print("min: {} mean: {} max: {}".format(min_val, mean_val, max_val))
    hist = cv2.calcHist(img_gray, [0], None, [256], [0, 256])
    # rescale brightness
    #   - bright_low and lower to 0
    #   - bright_high and higher to 255
    #   - bright_mid to 127
    #   - interpolate between bright_low and bright_high
    # clone image
    img_grayRescale = img_gray.copy()
    hist2 = None
    if bright_mid > 0 and True:
        # Create a matrix with the same size as the image, filled with the fixed value
        # Subtract the fixed value from the image
        img_sub = np.full(img_gray.shape, bright_low, dtype=np.uint8)
        img_grayRescale = cv2.subtract(img_gray, img_sub)
        # multiply each pixel
        img_grayRescale = cv2.multiply(img_grayRescale, 255 / (bright_high - bright_low))
        # recalibrate
        # miss rescale Mid
    if bright_mid > 0 and False :
        # new_image[y,x,c] = np.clip(alpha*image[y,x,c] + beta, 0, 255)
        img_grayRescale = cv2.convertScaleAbs(img_gray, 255 / (bright_high - bright_low), -bright_low)
        # modify mid of brightness


    if bright_low > 0 and False:
        # rescale brightness - manual
        rows, cols = img_gray.shape
        for r in range(rows):
            for c in range(cols):
                if img_grayRescale[r][c] < bright_low:
                    img_grayRescale[r][c] = 0
                elif img_grayRescale[r][c] > bright_high:
                    img_grayRescale[r][c] = 255
                else:
                    img_grayRescale[r][c] = int(255 * (img_grayRescale[r][c] - bright_low) / (bright_high - bright_low))
        #
    if img_grayRescale is not None:
        min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(img_grayRescale)
        mean_val = cv2.mean(img_grayRescale)
        print("min: {} mean: {} max: {}  (img_grayRescale)".format(min_val, mean_val, max_val))
        hist2 = cv2.calcHist(img_grayRescale, [0], None, [256], [0, 256])
        img = img_grayRescale
    # Plot the histogram
    # if figure already exists, keep it
    if not plt.fignum_exists(1):
        plt.figure()
    else:
        plt.clf()
    plt.title("Grayscale Histogram")
    plt.xlabel("Bins")
    plt.ylabel("# of Pixels")
    plt.plot(hist , color='gray')
    if bright_low > 0:
        plt.axvline(x=bright_low, color='gray', linestyle='dashed', linewidth=1)
        plt.axvline(x=bright_mid, color='gray', linestyle='dashed', linewidth=1)
        plt.axvline(x=bright_high, color='gray', linestyle='dashed', linewidth=1)
    if hist2 is not None:
        plt.plot(hist2 , color='red')
    plt.xlim([0, 256])
    plt.draw()
    plt.pause(0.001)
    plt.show()
    #

    #
    print ("")
    return img
