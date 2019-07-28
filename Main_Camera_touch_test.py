# USAGE
# python opencv_object_tracking.py
# python opencv_object_tracking.py --video dashcam_boston.mp4 --tracker csrt

# import the necessary packages
from imutils.video import VideoStream
#from imutils.video import FPS
import argparse
import imutils
import time
import cv2
import numpy as np
import Contours
import socket
#import threading
#import Keyboard_Controller_test

#from threading import Thread, Lock
HOST = '192.168.43.214'
PORT = 8090
cmd_M = '0'

def send():
    global HOST, cmd_M

    #for i in range(3):
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.connect((HOST,PORT))
    sent = client_socket.send(cmd_M.encode('utf-8'))
        #time.sleep(0.001)

#t = threading.Thread(target = Keyboard_Controller_test.control)
#t.start()
#keyboard_lock = Lock()





# # construct the argument parser and parse the arguments
# ap = argparse.ArgumentParser()
# ap.add_argument("-v", "--video", type=str,
# 	help="path to input video file")
# ap.add_argument("-t", "--tracker", type=str, default="csrt",
# 	help="OpenCV object tracker type")
# args = vars(ap.parse_args())

# # extract the OpenCV version info
# (major, minor) = cv2.__version__.split(".")[:2]

# # if we are using OpenCV 3.2 OR BEFORE, we can use a special factory
# # function to create our object tracker
# if int(major) == 3 and int(minor) < 3:
# 	tracker = cv2.Tracker_create(args["tracker"].upper())
# 	jun = 1

# otherwise, for OpenCV 3.3 OR NEWER, we need to explicity call the
# approrpiate object tracker constructor:
#else:
	# initialize a dictionary that maps strings to their corresponding
	# OpenCV object tracker implementations
##OPENCV_OBJECT_TRACKERS = {
##	"csrt": cv2.TrackerCSRT_create,
##	"kcf": cv2.TrackerKCF_create,
##	"boosting": cv2.TrackerBoosting_create,
##	"mil": cv2.TrackerMIL_create,
##	"tld": cv2.TrackerTLD_create,
##	"medianflow": cv2.TrackerMedianFlow_create,
##	"mosse": cv2.TrackerMOSSE_create
##}

# grab the appropriate object tracker using our dictionary of
# OpenCV object tracker objects
#tracker = OPENCV_OBJECT_TRACKERS[args["tracker"]]()
tracker_type = "medianflow"
tracker = cv2.TrackerMedianFlow_create()

# initialize the bounding box coordinates of the object we are going
# to track
initBB = None

# if a video path was not supplied, grab the reference to the web cam
#if not args.get("video", False):
print("[INFO] starting video stream...")
vs = VideoStream(src=0).start()
time.sleep(1.0)

# otherwise, grab a reference to the video file
# else:
# 	vs = cv2.VideoCapture(args["video"])

# initialize the FPS throughput estimator
#fps = None

#Region Setting
Region = None

############################ Mouse Event Processing ####################################################################
drawing=False
check = False
BB_check = False
BB_s = (0,0)
BB_e = (0,0)
mouse_counter = 0  
pts = []
pts_n = np.array(pts)

                


def mouse(event,x,y,flags,param):
        global pts, pts_n, drawing, check, Region,  contour, mouse_counter, initBB, fps, BB_s, BB_e, BB_check

        if event == cv2.EVENT_LBUTTONDOWN:
                if mouse_counter == 1:
                        drawing = True
                elif mouse_counter == 3:
                        BB_s = (x,y)
##                        initBB = cv2.selectROI("Frame", frame, fromCenter=False, showCrosshair=True)
##                        tracker.init(frame, initBB)
                        #fps = FPS().start()

        elif event == cv2.EVENT_MOUSEMOVE:
                if (drawing == True)and(check == True):
                        temp_pts = [x,y]
                        pts.append(temp_pts)
                elif BB_check == True:
                        BB_e = (x,y)


        elif event == cv2.EVENT_LBUTTONUP:
                if mouse_counter == 0:
                        check = True
                
##                cv2.imshow("Region Setting",frame)

                if (drawing == True)and(check == True):
                        pts_n = np.array(pts)
                        pts_n = pts_n.reshape((-1,1,2))
                        #cv2.polylines(img, [pts_n], isClosed = True, color = (255,0,0))
                        drawing = False
                        check = False
                        Region = True

                        contour = Contours.makeContour(frame,pts_n)

                        cv2.destroyWindow("Region Setting")

                if mouse_counter == 2:
                        BB_check = True
                        
                elif mouse_counter == 3:
                        BB_e = (x,y)
                        w = BB_e[0] - BB_s[0]
                        h = BB_e[1] - BB_s[1]
                        initBB = (BB_s[0], BB_s[1], w, h)
                        tracker.init(frame,initBB)
                        BB_check = False


                mouse_counter = mouse_counter + 1




#################################################################################################################33


##########################LOOP START###################################################################################

stopflag = 0
outflag = 0
# loop over frames from the video stream
while True:

        # grab the current frame, then handle if we are using a
        # VideoStream or VideoCapture object
        frame = vs.read()
        frame = frame #if args.get("video", False) else frame

        # check to see if we have reached the end of the stream
        if frame is None:
                break

        # resize the frame (so we can process it faster) and grab the
        # frame dimensions
        frame = imutils.resize(frame, width=500)
        (H, W) = frame.shape[:2]
        # print(len(frame))
        # print(len(frame[0]))



        # Check
        if check == True:
                cv2.putText(frame, "Region Setting Mode", (10,10), cv2.FONT_HERSHEY_SIMPLEX, 0.75, (0,0,255),2)

        elif BB_check == True:
                cv2.putText(frame, "Object Setting Mode", (10,10), cv2.FONT_HERSHEY_SIMPLEX, 0.75, (0,0,255),2)

                if (BB_s[0] != 0)and(BB_s[1] != 0):
                        cv2.rectangle(frame,BB_s,BB_e,(0,255,0))
                
        elif (initBB is not None)and(Region is not None):
                cv2.polylines(frame, [pts_n], isClosed = True, color = (255,0,0))
                #cv2.rectangle(frame, (Region[0],Region[1]), (Region[0] + Region[2],Region[1] + Region[3]), (255,0,0), 2)	
        # grab the new bounding box coordinates of the object
                (success, box) = tracker.update(frame)

                # check to see if the tracking was a success
                if success:
                        (x, y, w, h) = [int(v) for v in box]
                        cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)	# tracking box
                        center = ((2*x + w)/2, (2*y + h)/2)
                        
                        
                        if (Contours.pointTest(center,contour) == False) and (stopflag==0):
                                out = Contours.pointTest(center,contour)
                                cv2.putText(frame, "Out!!!!!!!!!!!!", (10,10), cv2.FONT_HERSHEY_SIMPLEX, 0.75, (0,0,255),2)
                                cmd_M = 'S'
                                stopflag=1
                                send()
                               #Keyboard_Controller_test.cmd = 'LLLL'
                                print(out)
                        elif (Contours.pointTest(center,contour) == True) and (outflag == 1) :
                                stopflag = 0
                                outflag = 0
                                cmd_M = 'I'
                                send()
                                cmd_M = 'S'
                                send()
                        if (stopflag==1) and (outflag==0):
                                cmd_M = 'O'
                                send()
                                outflag = 1
                                cv2.putText(frame, "Out!!!!!!!!!!!!", (10,10), cv2.FONT_HERSHEY_SIMPLEX, 0.75, (0,0,255),2)
                                
                                


                # update the FPS counter
                #fps.update()
                #fps.stop()

                # initialize the set of information we'll be displaying on
                # the frame
                info = [
                        ("Tracker", tracker_type),
                        ("Success", "Yes" if success else "No"),
                        #("FPS", "{:.2f}".format(fps.fps())),
                ]

                # loop over the info tuples and draw them on our frame
                for (i, (k, v)) in enumerate(info):
                        text = "{}: {}".format(k, v)
                        cv2.putText(frame, text, (10, H - ((i * 20) + 20)),
                                cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 0, 255), 2)


        elif Region is not None:
                cv2.polylines(frame, [pts_n], isClosed = True, color = (255,0,0))

        # check to see if we are currently tracking an object
        elif initBB is not None:
                # grab the new bounding box coordinates of the object
                (success, box) = tracker.update(frame)

                # check to see if the tracking was a success
                if success:
                        (x, y, w, h) = [int(v) for v in box]
                        cv2.rectangle(frame, (x, y), (x + w, y + h),
                                (0, 255, 0), 2)         # tracking box

                # update the FPS counter
                #fps.update()
                #fps.stop()

                # initialize the set of information we'll be displaying on
                # the frame
                info = [
                        ("Tracker", tracker_type),
                        ("Success", "Yes" if success else "No"),
                        #("FPS", "{:.2f}".format(fps.fps())),
                ]

                # loop over the info tuples and draw them on our frame
                for (i, (k, v)) in enumerate(info):
                        text = "{}: {}".format(k, v)
                        cv2.putText(frame, text, (10, H - ((i * 20) + 20)),
                                cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 0, 255), 2)



                




        # show the output frame		

        cv2.imshow("Frame", frame)
        cv2.setMouseCallback("Frame",mouse)
        key = cv2.waitKey(1) & 0xFF

        # if the 's' key is selected, we are going to "select" a bounding
        # box to track
        if key == ord("s"):
                # select the bounding box of the object we want to track (make
                # sure you press ENTER or SPACE after selecting the ROI)
                initBB = cv2.selectROI("Frame", frame, fromCenter=False,
                        showCrosshair=True)

                # start OpenCV object tracker using the supplied bounding box
                # coordinates, then start the FPS throughput estimator as well
                tracker.init(frame, initBB)
                #fps = FPS().start()

        elif key == ord("r"):  
                #Region = cv2.selectROI("Frame", frame, showCrosshair=True)
                #fps = FPS().start()
                
                check = True
                cv2.putText(frame, "Region Setting Mode", (10,10), cv2.FONT_HERSHEY_SIMPLEX, 0.75, (0,0,255),2)
                cv2.imshow("Region Setting",frame)

                cv2.setMouseCallback("Region Setting",mouse)

                
        # if the `q` key was pressed, break from the loop
        if key == ord("q"):
                break
		
##################################LOOP EXIT###########################################################################

# # if we are using a webcam, release the pointer
# if not args.get("video", False):
# 	vs.stop()

# # otherwise, release the file pointer
# else:
# 	vs.release()

# close all windows
cv2.destroyAllWindows()
