#!/usr/bin/env python

import rospy
from sensor_msgs.msg import CompressedImage
import matplotlib.pyplot as plt
import numpy as np


latencies=[]
def image_callback(ros_image):
    print 'got an image'
    now=rospy.get_rostime()
    delay_ms = (now - ros_image.header.stamp)
    print(delay_ms)
    latency=(delay_ms.secs*(1000))+(delay_ms.nsecs/(10**6))
    latencies.append(latency)


def main():
    rospy.init_node("image_latency_subscriber",anonymous=True)
    image_sub=rospy.Subscriber("/usb_cam/image_raw/compressed",CompressedImage,image_callback)
    rospy.spin()
    ax=plt.subplot()
    ax.plot(latencies)
    ax.set(xlabel='Query Number',ylabel='Latency (in ms) ',title='Latency Plot')
    plt.xticks(np.arange(0, len(latencies)+1, len(latencies)/20))
    ax.grid()

if __name__ == '__main__':
    main()
