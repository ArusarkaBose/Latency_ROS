#!/usr/bin/env python
import rospy
from std_msgs.msg import String

def chatter_callback(message):
    pub = rospy.Publisher('rebound_chatter', String, queue_size=0)
    rate = rospy.Rate(100) # 1hz
    #keep publishing until a Ctrl-C is pressed
    pub.publish(message.data)

def listener():

    rospy.init_node('listener', anonymous=True)

    rospy.Subscriber("chatter", String, chatter_callback)

    # spin() simply keeps python from exiting until this node is stopped
    rospy.spin()


if __name__ == '__main__':
    listener()
