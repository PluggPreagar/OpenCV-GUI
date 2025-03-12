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

def f_contour(img,  bright_min, bright_max,  height_min, height_max, bright_contour_min):
    # raise Exception('fox')
    print("f_contour: gray and blur ..." )
    ## check if already gray
    if len(img.shape) != 2:
        print("f_contour: not gray ... (works only with gray images)")
        img_gray = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
    else:
        img_gray = img
    # create empty image
    # extract contours
    ret, img_thresh = cv2.threshold(img_gray, bright_min, bright_max, cv2.THRESH_BINARY)
    # show_wait_destroy("img_thresh", img_thresh)
    # contours, hierarchy = cv2.findContours(img_thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)
    contours, hierarchy = cv2.findContours(img_thresh, cv2.RETR_TREE, cv2.CHAIN_APPROX_NONE)
    # create empty image
    img_contour_explain = np.zeros_like(img)
    img_contour_dummy = np.zeros_like(img)
    img_contour = np.zeros_like(img)
    i = 0
    i_selected = 0
    for contour in contours:
        i = i + 1
        # boundingrect
        x, y, w, h = cv2.boundingRect(contour)
        # check if contour touches border -
        if x == 0 or y == 0 or x+w == img.shape[1] or y+h == img.shape[0]:
            print("contour: [BORDER] {} [ {}, {} ]  [ {} x {} ] ".format(i, x, y, w, h ))
            cv2.drawContours(img_contour_explain, [contour], 0, (75, 0, 0), 1)
        # skipp small contours
        elif w < 10 or h < 10:
            # SKIPP TINY ... print("contour: [SMALL_] {} [ {}, {} ]  [ {} x {} ] ".format(i, x, y, w, h ))
            cv2.drawContours(img_contour_explain, [contour], 0, (25, 0, 0), 1)
        # assume digest are:
        #  - longest side is vertical
        #  - width is max 1/3 of height
        elif height_min < h < height_max : #  and w < h/3:
            cv2.putText(img_contour_explain, str(i), tuple(contour[0][0]), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255))
            if w < h * 0.75 :  # 69 x 97
                # check avg brightness in original image
                count_ = 0
                color_ = 0
                cv2.drawContours(img_contour_dummy, [contour], 0, (255, 255, 255), cv2.FILLED) # may be changed
                for y_ in range(y, y+h):
                    for x_ in range(x, x+w):
                        #if i == 84 :
                            # print("x: {} y: {} x_: {} y_: {} bright: {}  {}".format(x, y, x_, y_, img_contour_dummy[y_][x_], img_gray[y_][x_]))
                        if img_contour_dummy[y_][x_] > 0 :  # mask
                            count_ = count_ + 1
                            color_ = color_ + img_gray[y_][x_]
                color_ = color_ / count_ if count_ > 0 else 0
                #
                if color_ > bright_contour_min:
                    i_selected = i_selected + 1
                    print("CONTOUR: [OK____] {} [ {}, {} ]  [ {} x {} ] ".format(i, x, y, w, h ))
                    cv2.drawContours(img_contour, [contour], 0, (255, 255, 255), cv2.FILLED)
                    #img_contour[y:y+h, x:x+w] = img[y:y+h, x:x+w] # rectangle !!!
                    img_contour_explain[y:y+h, x:x+w] = img[y:y+h, x:x+w]
                    cv2.drawContours(img_contour_explain, [contour], 0, (255, 255, 255), 1)
                    # copy bounding box of contour from original image to new image
                else:
                    print("Contour: [BRIGHT_] {} [ {}, {} ]  [ {} x {} ] {} ".format(i, x, y, w, h, color_ ))
                    cv2.drawContours(img_contour_explain, [contour], 0, (150, 0, 0), 1)
            else:
                print("Contour: [PROPOR] {} [ {}, {} ]  [ {} x {} ] {} ".format(i, x, y, w, h, w/h ))
                cv2.drawContours(img_contour_explain, [contour], 0, (100, 0, 0), 1)
        else:
            print("contour: [SIZE__] {} [ {}, {} ]  [ {} x {} ] ".format(i, x, y, w, h ))
            cv2.drawContours(img_contour_explain, [contour], 0, (50, 0, 0), 1)
    #
    show_wait_destroy("img_contour", img_contour)
    show_wait_destroy("img_contour_explain", img_contour_explain)
    img_cutout = np.zeros_like(img)
    # use img_contour_explain as mask to copy selected contours to new image
    cv2.copyTo(img_gray, img_contour, img_cutout)
    #
    print ("")
    return img_cutout if i_selected > 0 else img_contour_explain
