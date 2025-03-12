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
        blur2 = cv2.GaussianBlur(blur_gray,(kernelNeg, kernelNeg),0)
        # init 1 dim array with 255
        blur_history = np.full(256,0)
        rows,cols = blur_gray.shape
        #
        diff_max = 0
        for r in range(rows):
            for c in range(cols):
                diff_max_ = abs(int(blur_gray[r][c]) - int(blur2[r][c]))
                if diff_max_ > diff_max:
                    diff_max = diff_max_
        diff_stretch = 126 / diff_max
        print("diff_max: {} diff_stretch: {}".format(diff_max, diff_stretch))
        # apply diff
        for r in range(rows):
            for c in range(cols):
                # allow negative diff
                diff = (int(blur_gray[r][c]) - int(blur2[r][c])) * diff_stretch
                # show negative diffs
                if rows < 2 and blur_gray[r][c] < blur2[r][c]:
                    print("diff: {} {} {} {} {}".format(r, c, diff, blur_gray[r][c], blur2[r][c]))
                # keep only darker pixels
                # blur2[r][c] = diff*3 if diff < 0 else 0
                blur2[r][c] = diff*3 if diff > 0 else 0
                # spread diff -
                blur_history[blur2[r][c]] += 1
        img = blur2
        # search gap in blur_history
        for i in range(255):
            if blur_history[i] > 0:
                print("blur_history[{}]: {}".format(i, blur_history[i]))
        # blur_grayDiff = cv2.subtract(blur_gray, blur2)
        # img = blur_grayDiff
    #
    print ("")
    return img
