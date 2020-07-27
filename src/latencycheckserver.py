#!/usr/bin/env python

from Latency_ROS.srv import LatencyCheck
from Latency_ROS.srv import LatencyCheckRequest
from Latency_ROS.srv import LatencyCheckResponse

import rospy

def handle_time(req):
    print ("Query time = ",req.query_time)
    return LatencyCheckResponse(req.query_time,req.query_load)

def time():
    rospy.init_node('latency_check')
    s = rospy.Service('latency_check', LatencyCheck, handle_time)
    print "Awaiting query time"
    rospy.spin()
    
if __name__ == "__main__":
    time()
