import rospy
from sensor_msgs.msg import LaserScan
from normal_estimation.msg import PointsWithNormal
from geometry_msgs.msg import Point32, Vector3
import numpy as np
from sklearn.neighbors import NearestNeighbors
import matplotlib.pyplot as plt

class LaserProcessor:
    def __init__(self):
        rospy.init_node('laser_processor', anonymous=True)
        self.subscriber = rospy.Subscriber("/scan", LaserScan, self.callback)
        self.points = []
        self.normals = []

        # Publisher for the normals
        self.points_with_normals_publisher = rospy.Publisher("/points_with_normals", PointsWithNormal, queue_size=10)

    def callback(self, data):
        ranges = np.array(data.ranges)
        angles = np.linspace(data.angle_min, data.angle_max, len(ranges))
        x = ranges * np.cos(angles)
        y = ranges * np.sin(angles)

        # Filter out invalid values (inf, nan)
        valid_indices = np.isfinite(x) & np.isfinite(y)
        self.points = np.column_stack((x[valid_indices], y[valid_indices]))
        self.header = data.header

    def compute_normal(self, point, previous_point, next_point, robot_position):
        # Compute direction vectors
        direction_prev = point - previous_point
        direction_next = next_point - point

        # Calculate the average direction
        direction = 0.5 * (direction_prev + direction_next)

        # Rotate direction vector by 90 degrees
        normal = np.array([direction[1], -direction[0]])

        # Check if normal points towards the robot
        robot_to_point = point - robot_position
        angle_diff = np.arccos(np.dot(normal, robot_to_point) / (np.linalg.norm(normal) * np.linalg.norm(robot_to_point)))
        if angle_diff < np.pi / 2:  # Angle less than 90 degrees means normal points towards the robot
            normal *= -1  # Reverse direction

        # Normalize the normal vector
        return normal / np.linalg.norm(normal)

    def process_points(self):
        if len(self.points) == 0:
            return

        # Get robot's position (assuming it's at the origin)
        robot_position = np.array([0, 0])

        # Clear the normals list before processing new points
        self.normals = []

        # Iterate over points and their neighbors
        for i, point in enumerate(self.points):
            # Ensure indices are within the valid range
            prev_index = max(0, i - 1)
            next_index = min(len(self.points) - 1, i + 1)

            previous_point = self.points[prev_index]
            next_point = self.points[next_index]

            # Compute the normal at the current point
            normal = self.compute_normal(point, previous_point, next_point, robot_position)

            # Append the computed normal to the list
            self.normals.append(normal)

        # Publish the computed normals as a list message
        self.publish_normals()

    def publish_normals(self):
        # Create a PointsWithNormal message
        points_with_normals_msg = PointsWithNormal()

        points_with_normals_msg.header = self.header

        # Populate the message with points and normals
        points_with_normals_msg.points_x = [point[0] for point in self.points]
        points_with_normals_msg.points_y = [point[1] for point in self.points]
        points_with_normals_msg.normals_x = [normal[0] for normal in self.normals]
        points_with_normals_msg.normals_y = [normal[1] for normal in self.normals]

        # Publish the message
        self.points_with_normals_publisher.publish(points_with_normals_msg)

if __name__ == '__main__':
    laser_processor = LaserProcessor()
    rate = rospy.Rate(10)  # Adjust the rate according to your data publishing rate
    while not rospy.is_shutdown():
        laser_processor.process_points()
        rate.sleep()
