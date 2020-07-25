#!/usr/bin/env python

import rospy
from std_msgs.msg import String
import matplotlib.pyplot as plt
import numpy as np

prev=""
latencies=[]
def rebound_chatter_callback(message):
    global prev
    now=rospy.get_rostime()
    if(message.data!=prev):
        prev=message.data
        pub_time=int(message.data)
        rec_time=now.nsecs+(now.secs*(10**9))
        latency=rec_time-pub_time
        #rospy.loginfo("Message = %s ",message.data)
        latencies.append(float(latency)/(10**6))
        rospy.loginfo("Latency = %d ",latency)
    return 

def talker():
    pub = rospy.Publisher('chatter', String, queue_size=0) 
    rospy.init_node('talker', anonymous=True)
    #set the loop rate
    rate = rospy.Rate(1) # 1hz
    #keep publishing until a Ctrl-C is pressed
    num_publish=100
    for i in range(num_publish+1):
        now=rospy.get_rostime()
        hello_str="%d" % (now.nsecs+(now.secs*(10**9)))
        pub.publish(hello_str)
        rospy.Subscriber("rebound_chatter", String, rebound_chatter_callback)
        rate.sleep()
        i=i+1
    ax=plt.subplot()
    ax.plot(latencies)
    ax.set(xlabel='Query Number',ylabel='Latency (in ms) ',title='Latency Plot')
    plt.xticks(np.arange(0, len(latencies)+1, len(latencies)/20))
    ax.grid()
    plt.show()



if __name__ == '__main__':
    try:
        talker()
    except rospy.ROSInterruptException:
        pass
