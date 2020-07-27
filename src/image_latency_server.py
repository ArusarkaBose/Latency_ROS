#!/usr/bin/env python

from Latency_ROS.srv import ImageLatency
from Latency_ROS.srv import ImageLatencyRequest
from Latency_ROS.srv import ImageLatencyResponse

import rospy

def handle_time(req):
    print ("Query time = ",req.query_time)
    return ImageLatencyResponse(req.query_image,req.query_time)

def time():
    rospy.init_node('image_latency_server')
    s = rospy.Service('image_latency_check', ImageLatency, handle_time)
    print "Awaiting query time"
    rospy.spin()
    
if __name__ == "__main__":
    time()
