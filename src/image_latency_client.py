#!/usr/bin/env python

from codebase.srv import ImageLatency
from codebase.srv import ImageLatencyRequest
from codebase.srv import ImageLatencyResponse

import matplotlib.pyplot as plt
import numpy as np
import cv2
from cv_bridge import CvBridge, CvBridgeError

import rospy
import sys

bridge=CvBridge()

def latencycheck_client(frame,time):
    rospy.wait_for_service('image_latency_check')
    try:
        latency_check = rospy.ServiceProxy('image_latency_check', ImageLatency)
        response = latency_check(frame,time)
        return (response.return_image,response.return_time)
    except rospy.ServiceException, e:
        print "Service call failed: %s"%e
    

if __name__ == "__main__":
    num_queries=20
    latencies=[]
    for i in range(num_queries):
        rospy.init_node('image_latency_client')
        query_time=rospy.get_rostime()
        video_capture=cv2.VideoCapture(0)
        ret,frame=video_capture.read()
        video_capture.release()
        if(ret):
            try:
                query_frame=bridge.cv2_to_imgmsg(frame,"bgr8")
            except CvBridgeError as e:
                print(e)
        cv2.destroyAllWindows()
        return_frame,return_time = latencycheck_client(query_frame,query_time)
        current_time=rospy.get_rostime()
        latency=current_time-return_time
        print("Latency= ",latency)
        latencies.append(float(latency.nsecs)/(10**6))

    ax=plt.subplot()
    ax.plot(latencies)
    ax.set(xlabel='Query Number',ylabel='Latency (in ms) ',title='Latency Plot')
    plt.xticks(np.arange(0, len(latencies)+1, len(latencies)/20))
    ax.grid()

    plt.show()


cv2.destroyAllWindows()
