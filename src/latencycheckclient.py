#!/usr/bin/env python

from Latency_ROS.srv import LatencyCheck
from Latency_ROS.srv import LatencyCheckRequest
from Latency_ROS.srv import LatencyCheckResponse

import matplotlib.pyplot as plt
import numpy as np
import time
import json
import random
import string

import rospy
import sys

def latencycheck_client(time,load):
    rospy.wait_for_service('latency_check')
    try:
        latency_check = rospy.ServiceProxy('latency_check', LatencyCheck)
        response = latency_check(time,load)
        return (response.return_time,response.return_load)
    except rospy.ServiceException, e:
        print "Service call failed: %s"%e

if __name__ == "__main__":
    num_queries=1000
    num_bursts=10
    packet_sizes=[20,50,100,200,500,1000,10000]

    rospy.init_node('latency_check_client')

    fig_handle=plt.figure()
    ax=plt.subplot()

    for packet_size in packet_sizes:
        latency_bursts=[]

        for i in range(num_bursts):
            latencies=[]
            for i in range(num_queries):
                query_time=rospy.get_rostime()
                query_load=''.join(random.sample(string.ascii_letters*packet_size+string.digits*packet_size, k = packet_size))
                return_time,return_load = latencycheck_client(query_time,query_load)
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

        """
        In order to display ROS1 and ROS2 latencies on the same plot, uncomment the below lines which save the
        latency information in a json file.
        """

        latency_ROS1=dict()
        latency_ROS1["y"]=y
        latency_ROS1["x"]=x.tolist()
        latency_ROS1["yerr"]=yerr

        with open('latency_ROS1_{}.json'.format(packet_size),'w+') as json_file:
            json.dump(latency_ROS1,json_file)
        

        ax.errorbar(x,y,yerr,label="{} bytes".format(packet_size))
        plt.xticks(np.arange(min(x), max(x)+1, 1.0))
    
    ax.set(xlabel='Query Number (at 5 sec intervals)',ylabel='Latency (in ms) ',title='Latency Plot')
    ax.legend(loc='upper center')
    ax.grid()

    plt.show()
