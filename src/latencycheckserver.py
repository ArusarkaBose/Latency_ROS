#!/usr/bin/env python

from codebase.srv import LatencyCheck
from codebase.srv import LatencyCheckRequest
from codebase.srv import LatencyCheckResponse

import rospy

def handle_time(req):
    print ("Query time = ",req.query_time)
    return LatencyCheckResponse(req.query_time)

def time():
    rospy.init_node('latency_check')
    s = rospy.Service('latency_check', LatencyCheck, handle_time)
    print "Awaiting query time"
    rospy.spin()
    
if __name__ == "__main__":
    time()
