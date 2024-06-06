import rospy
from nav_msgs.msg import Odometry
from geometry_msgs.msg import Twist, Quaternion
from tf.transformations import euler_from_quaternion
from math import pi, fabs

class MoveRotateMove:
    def __init__(self):
        rospy.init_node('move_rotate_move_node', anonymous=True)
        self.odom_sub = rospy.Subscriber('/odom', Odometry, self.odom_callback)
        self.vel_pub = rospy.Publisher('/cmd_vel', Twist, queue_size=10)
        self.rate = rospy.Rate(10)  # 10 Hz

        self.target_yaw = pi / 2  # 90 degrees in radians
        self.yaw_tolerance = 0.02  # 2.86 degrees in radians
        self.linear_speed = 0.3  # m/s
        self.angular_speed = 0.2  # rad/s
        self.distance_to_travel_y = 6.0  # meters for y-axis movement
        self.distance_to_travel_x = 21.0  # meters for x-axis movement
        self.current_x = 0.0
        self.current_y = 0.0
        self.current_yaw = 0.0

        # PID parameters for rotation control
        self.Kp_rotation = 1.0
        self.Ki_rotation = 0.01
        self.Kd_rotation = 0.5
        self.prev_error_rotation = 0.0
        self.error_integral_rotation = 0.0

        # PID parameters for position control
        self.Kp_position = 1.1
        self.Ki_position = 0.0
        self.Kd_position = 0.6
        self.prev_error_position = 0.0
        self.error_integral_position = 0.0

    def odom_callback(self, odom_msg):
        orientation_quaternion = odom_msg.pose.pose.orientation
        orientation_list = [orientation_quaternion.x, orientation_quaternion.y, orientation_quaternion.z, orientation_quaternion.w]
        _, _, self.current_yaw = euler_from_quaternion(orientation_list)
        self.current_x = odom_msg.pose.pose.position.x
        self.current_y = odom_msg.pose.pose.position.y

    def rotate(self, target_yaw):
        print("here")
        while not rospy.is_shutdown():
            print(target_yaw *180 / pi, self.current_yaw * 180 / pi, fabs(target_yaw - self.current_yaw) * 180/pi)
            if fabs(target_yaw - self.current_yaw) <= self.yaw_tolerance:
                rospy.loginfo("Reached target orientation.")
                break
            else:
                twist_msg = Twist()
                twist_msg.angular.z = self.angular_speed
                self.vel_pub.publish(twist_msg)
                self.rate.sleep()

        # Stop the rotation
        stop_msg = Twist()
        self.vel_pub.publish(stop_msg)

    def move_forward(self, dir, distance_to_travel, pid_dir = None):
        if dir == "y":
            self.initial_y = self.current_y
            self.initial_x = self.current_x
            while not rospy.is_shutdown():
                if fabs(self.current_y - self.initial_y) >= distance_to_travel:
                    rospy.loginfo("Reached destination.")
                    break
                error = self.current_x - self.initial_x
                twist_msg = Twist()
                twist_msg.linear.x = self.linear_speed
                if fabs(error) >= 0.01:  # Tolerance for position control
                    angular_speed = self.Kp_position * error + self.Ki_position * self.error_integral_position + self.Kd_position * (error - self.prev_error_position)
                    self.error_integral_position += error
                    self.prev_error_position = error
                    if pid_dir == "minus":
                        twist_msg.angular.z = -angular_speed
                    else:
                        twist_msg.angular.z = angular_speed
                self.vel_pub.publish(twist_msg)
                self.rate.sleep()
        if dir == "x":
            self.initial_x = self.current_x
            self.initial_y = self.current_y
            while not rospy.is_shutdown():
                print("should be here")
                if fabs(self.current_x - self.initial_x) >= distance_to_travel:
                    rospy.loginfo("Reached destination.")
                    break
                error = self.initial_y - self.current_y
                twist_msg = Twist()
                twist_msg.linear.x = self.linear_speed
                print(self.initial_y, self.current_y, error)

                if fabs(error) >= 0.01:  # Tolerance for position control
                    # Calculate control output
                    angular_speed = self.Kp_position * error + self.Ki_position * self.error_integral_position + self.Kd_position *1.3 * (error - self.prev_error_position)
                    self.error_integral_position += error
                    self.prev_error_position = error
                    twist_msg.angular.z = angular_speed
                self.vel_pub.publish(twist_msg)
                self.rate.sleep()
        stop_msg = Twist()
        self.vel_pub.publish(stop_msg)

if __name__ == '__main__':
    try:
        move_rotate_move_obj = MoveRotateMove()
        # move_rotate_move_obj.rotate(target_yaw=pi / 2)
        move_rotate_move_obj.move_forward(dir="x", distance_to_travel=104.0)
        # move_rotate_move_obj.rotate(target_yaw=pi)
        # move_rotate_move_obj.move_forward(dir="x", distance_to_travel=20.0)
        # move_rotate_move_obj.rotate(target_yaw=-pi / 2)
        # move_rotate_move_obj.move_forward(dir="y", distance_to_travel=6.0, pid_dir = "minus")
    except rospy.ROSInterruptException:
        pass
