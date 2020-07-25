#!/usr/bin/env python

from codebase.srv import LatencyCheck
from codebase.srv import LatencyCheckRequest
from codebase.srv import LatencyCheckResponse

import matplotlib.pyplot as plt
import numpy as np
import pickle as pl

import rospy
import sys

def latencycheck_client(time):
    rospy.wait_for_service('latency_check')
    try:
        latency_check = rospy.ServiceProxy('latency_check', LatencyCheck)
        response = latency_check(time)
        return response.return_time
    except rospy.ServiceException, e:
        print "Service call failed: %s"%e

if __name__ == "__main__":
    num_queries=10000
    latencies=[]
    rospy.init_node('latency_check_client')
    for i in range(num_queries):
        query_time=rospy.get_rostime()
        return_time = latencycheck_client(query_time)
        current_time=rospy.get_rostime()
        latency=current_time-return_time
        print("Latency= ",latency)
        latencies.append((latency.secs*1000)+float(latency.nsecs)/(10**6))

    mean=sum(latencies[1:])/len(latencies[1:])
    standard_dev=sum([((x - mean) ** 2) for x in latencies[1:]]) / len(latencies[1:])    

    print("Mean = ",mean)
    print("Error Bar = ",mean+standard_dev)
    print("Max = ",max(latencies[1:]))
    print("Min = ",min(latencies[1:]))
    

    #fig_handle = pl.load(open('/home/arusarka/dev_ws/src/devel_space/devel_space/ros2_latency.pickle','rb'))
    #x_old = fig_handle.axes[0].lines[0].get_data()[0]
    #y_old = fig_handle.axes[0].lines[0].get_data()[1]

    ax=plt.subplot()

    #ax.plot(x_old,y_old)

    ax.plot(latencies)
    ax.set(xlabel='Query Number',ylabel='Latency (in ms) ',title='Latency Plot')
    plt.xticks(np.arange(0, len(latencies)+1, len(latencies)/20))
    ax.grid()

    plt.show()
