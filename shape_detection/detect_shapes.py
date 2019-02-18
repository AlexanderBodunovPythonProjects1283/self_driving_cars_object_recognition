# USAGE
# python detect_shapes.py --image shapes_and_colors.png

# import the necessary packages
from pyimagesearch.shapedetector import ShapeDetector
import argparse
import imutils
import cv2


def grab_contours(cnts):
    # if the length the contours tuple returned by cv2.findContours
    # is '2' then we are using either OpenCV v2.4, v4-beta, or
    # v4-official
    if len(cnts) == 2:
        cnts = cnts[0]

    # if the length of the contours tuple is '3' then we are using
    # either OpenCV v3, v4-pre, or v4-alpha
    elif len(cnts) == 3:
        cnts = cnts[1]

    # otherwise OpenCV has changed their cv2.findContours return
    # signature yet again and I have no idea WTH is going on
    else:
        raise Exception(("Contours tuple must have length 2 or 3, "
            "otherwise OpenCV changed their cv2.findContours return "
            "signature yet again. Refer to OpenCV's documentation "
            "in that case"))

    # return the actual contours array
    return cnts



# construct the argument parse and parse the arguments
#ap = argparse.ArgumentParser()
#ap.add_argument("-i", "--image", required=True,
#    help="path to the input image")
#args = vars(ap.parse_args())

# load the image and resize it to a smaller factor so that
# the shapes can be approximated better
#image = cv2.imread(args["image"])

def find_countours(mask,image):
    
    #resized = imutils.resize(mask, width=300)
    ratio = image.shape[0] / float(mask.shape[0])

    # convert the resized image to grayscale, blur it slightly,
    # and threshold it
    #gray = cv2.cvtColor(mask, cv2.COLOR_BGR2GRAY)
    blurred = cv2.GaussianBlur(mask, (5, 5), 0)
    thresh = cv2.threshold(blurred, 60, 255, cv2.THRESH_BINARY)[1]

    # find contours in the thresholded image and initialize the
    # shape detector
    cnts = cv2.findContours(thresh.copy(), cv2.RETR_EXTERNAL,
        cv2.cvStartFindContours_Impl)
    #cnts = imutils.grab_contours(cnts)
    cnts=grab_contours(cnts)
    sd = ShapeDetector()

    # loop over the contours

    count__=0
    arr_contours=[]
    for c in cnts:
        if len(c)>2 and len(c)<35:
            count__+=1
            #print(count__," Contors on screen")
            # compute the center of the contour, then detect the name of the
            # shape using only the contour
            M = cv2.moments(c)
            try:
                cX = int((M["m10"] / M["m00"]) * ratio)
                cY = int((M["m01"] / M["m00"]) * ratio)
            except:
                cX = int((M["m10"] / 0.0001) * ratio)
                cY = int((M["m01"] / 0.0001) * ratio)
            shape = sd.detect(c)

            # multiply the contour (x, y)-coordinates by the resize ratio,
            # then draw the contours and the name of the shape on the image
            c = c.astype("float")
            c *= ratio
            c = c.astype("int")
            cv2.drawContours(image, [c], -1, (0, 255, 0), 2)
            cv2.putText(image, str(len(c)), (cX, cY), cv2.FONT_HERSHEY_SIMPLEX,
                0.5, (255, 255, 255), 2)
            
            arr_contours.append([cX,cY,len(c)])

            # show the output image
    print(count__," Contors on screen")
    return [image,arr_contours]
#image=cv2.imread("shapes_and_colors_1.png")
#image=find_countours(image,image)
#cv2.imshow("Image", image)
#cv2.waitKey(0)
