#!/usr/bin/env python

from codebase.srv import LatencyCheck
from codebase.srv import LatencyCheckRequest
from codebase.srv import LatencyCheckResponse

import matplotlib.pyplot as plt
import numpy as np
import time
import json

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
    num_queries=1000
    num_bursts=10

    rospy.init_node('latency_check_client')

    latency_bursts=[]

    for i in range(num_bursts):
        latencies=[]
        for i in range(num_queries):
            query_time=rospy.get_rostime()
            return_time = latencycheck_client(query_time)
            current_time=rospy.get_rostime()
            latency=current_time-return_time
            print("Latency= ",latency)
            latencies.append((latency.secs*1000)+float(latency.nsecs)/(10**6))

        mean=np.mean(latencies)
        standard_dev=np.std(latencies)    

        print("Mean = ",mean)
        print("Error Bar = ",mean+standard_dev)
        print("Max = ",max(latencies))
        print("Min = ",min(latencies))

        latency_bursts.append(latencies)
        time.sleep(5)

    y=[np.mean(latencies) for latencies in latency_bursts]
    x=np.arange(1,len(y)+1,1)
    yerr=[np.std(latencies) for latencies in latency_bursts]

    latency_ROS1=dict()
    latency_ROS1["y"]=y
    latency_ROS1["x"]=x.tolist()
    latency_ROS1["yerr"]=yerr

    with open('latency_ROS1.json','w+') as json_file:
        json.dump(latency_ROS1,json_file)
    

    fig_handle=plt.figure()
    ax=plt.subplot()

    ax.errorbar(x,y,yerr)
    ax.set(xlabel='Query Number (at 5 sec intervals)',ylabel='Latency (in ms) ',title='Latency Plot')
    plt.xticks(np.arange(min(x), max(x)+1, 1.0))
    ax.grid()

    plt.show()
