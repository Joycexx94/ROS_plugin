#!/usr/bin/python
import rospy
from geometry_msgs.msg import Twist
from sensor_msgs.msg import Joy

class TeleopTurtle:
    def __init__(self):
        rospy.init_node('turtle_teleop_joy')
        self.linear_axis = rospy.get_param("axis_linear")
        self.angular_axis = rospy.get_param("axis_angular")
        self.linear_scale = rospy.get_param("scale_linear")
        self.angular_scale = rospy.get_param("scale_angular")

        self.twist = None
        self.joy = Joy()
        twist_pub = rospy.Publisher('turtle1/cmd_vel', Twist)
        rospy.Subscriber("joy", Joy, self.callback)
        rate = rospy.Rate(rospy.get_param('~hz', 20))

        while not rospy.is_shutdown():
            rate.sleep()
            if self.twist:
                twist_pub.publish(self.twist)

    def callback(msg):
        twist = Twist()
        twist.linear.x = linear_scale * msg.axes[linear_axis]
        twist.angular.z = angular_scale * msg.axes[angular_axis]
        self.twist = twist

if __name__ == "__main__": 
    TeleopTurtle()
