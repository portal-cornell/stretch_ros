import argparse as ap
import rospy
from std_msgs.msg import String
from geometry_msgs.msg import Point
from visualization_msgs.msg import MarkerArray
from visualization_msgs.msg import Marker
import math
import hello_helpers.hello_misc as hm
import roslib
roslib.load_manifest('visualization_marker_tutorials')

# p1, p2, p3 are the rigid body points
global p1
global p2
global p3

# create an object called line_segment_1 and line_segment_2, each with two rigid bodies


class ArmNode(hm.HelloNode):

    def __init__(self, p1, p2, p3):
        self.x1 = p1.x
        self.y1 = p1.y
        self.z1 = p1.z
        self.x2 = p2.x
        self.y2 = p2.y
        self.z2 = p2.z
        self.x3 = p3.x
        self.y3 = p3.y
        self.z3 = p3.z

    def create_line_segment(self, p1, p2):
        markerArray = MarkerArray()
        count = 0

        marker1 = Marker()
        marker1.id = count
        marker1.lifetime = rospy.Duration()
        marker1.header.frame_id = "/"
        marker1.type = marker1.SPHERE
        marker1.action = marker1.ADD
        marker1.scale.x = 0.2
        marker1.scale.y = 0.2
        marker1.scale.z = 0.2
        marker1.color.a = 1.0
        marker1.color.r = 1.0
        marker1.color.g = 1.0
        marker1.color.b = 0.0
        marker1.pose.orientation.w = 1.0
        marker1.pose.position.x = p1.x
        marker1.pose.position.y = p1.y
        marker1.pose.position.z = p1.z
        markerArray.markers.append(marker1)
        count += 1

        marker2 = Marker()
        marker2.id = count
        marker2.lifetime = rospy.Duration()
        marker2.header.frame_id = "/"
        marker2.type = marker2.SPHERE
        marker2.action = marker2.ADD
        marker2.scale.x = 0.2
        marker2.scale.y = 0.2
        marker2.scale.z = 0.2
        marker2.color.a = 1.0
        marker2.color.r = 1.0
        marker2.color.g = 1.0
        marker2.color.b = 0.0
        marker2.pose.orientation.w = 1.0
        marker2.pose.position.x = p2.x
        marker2.pose.position.y = p2.y
        marker2.pose.position.z = p2.z
        markerArray.markers.append(marker2)

        line = Marker()
        line.id = count
        line.lifetime = rospy.Duration()
        line.header.frame_id = "/"
        line.type = line.LINE_STRIP
        line.action = line.ADD
        line.scale.x = 0.4
        line.color.a = 1.0
        line.color.b = 1.0
        line.pose.orientation.w = 1.0
        line.pose.position.x = 0
        line.pose.position.y = 0
        line.pose.position.z = 0
        line.points = []
        for i in range(100):
            p = Point()
            # p = start_point + i/100*(end_point-start_point)
            p.x = marker1.pose.position.x + i/100 * \
                (marker2.pose.position.x - marker1.pose.position.x)
            p.y = marker1.pose.position.y + i/100 * \
                (marker2.pose.position.y - marker1.pose.position.y)
            p.z = marker1.pose.position.z + i/100 * \
                (marker2.pose.position.z - marker1.pose.position.z)
            line.points.append(p)
        # for i in range(10):
        #     p = Point()
        #     p.x = i/2
        #     p.y = i*math.sin(i/3)
        #     p.z = 0
        #     line.points.append(p)
        markerArray.markers.append(line)  # add linestrip to markerArray
        return markerArray

    def callback1(self, data):
        rospy.loginfo(rospy.get_caller_id() + "I heard %s", data.data)

    def callback2(self, data):
        rospy.loginfo(rospy.get_caller_id() + "I heard %s", data.data)

    def callback3(self, data):
        rospy.loginfo(rospy.get_caller_id() + "I heard %s", data.data)

    def main(self):
        rospy.init_node('register', anonymous=True)
        rospy.Subscriber(topic, MarkerArray, self.callback1)
        rospy.Subscriber(topic, MarkerArray, self.callback2)
        rospy.Subscriber(topic, MarkerArray, self.callback3)
        rospy.spin()

        publisher = rospy.Publisher("arm_publisher", MarkerArray)
        rate = rospy.Rate(10)
        while not rospy.is_shutdown():
            wrist_to_elbow = self.create_line_segment(p1, p2)
            rospy.loginfo(wrist_to_elbow)
            publisher.publish(wrist_to_elbow)
            elbow_to_shoulder = self.create_line_segment(p2, p3)
            rospy.loginfo(elbow_to_shoulder)
            publisher.publish(elbow_to_shoulder)
            rate.sleep()


if __name__ == '__main__':
    try:
        parser = ap.ArgumentParser(description='Create line segments')
        args, unknown = parser.parse_known_args()
        node = ArmNode()
        node.main()
    except rospy.ROSInterruptException:
        pass
