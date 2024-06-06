import rospy
from nav_msgs.msg import Odometry
from geometry_msgs.msg import PoseArray
import numpy as np

class ParticlePoseRMSEChecker:
    def __init__(self):
        rospy.init_node('particle_pose_rmse_checker')
        
        self.odom_pose = None
        self.particle_within_range = False
        
        # Subscribe to particle pose array topic
        rospy.Subscriber('/mcl_optimal_node/particles', PoseArray, self.particles_callback)
        
        # Subscribe to odometry topic
        rospy.Subscriber('/odom', Odometry, self.odom_callback)
        
    def odom_callback(self, odom_msg):
        # Store odometry pose
        self.odom_pose = odom_msg.pose.pose
        
    def get_odom_pose(self):
        # Function to get odometry pose
        return self.odom_pose
        
    def particles_callback(self, particles_msg):
        if self.odom_pose is None:
            rospy.logwarn("Odometry data is not available yet.")
            return
        
        # Extract particle poses from PoseArray message
        particle_poses = particles_msg.poses
        
        for pose in particle_poses:
            # Calculate RMSE between particle pose and odometry pose
            rmse = np.sqrt((pose.position.x - self.odom_pose.position.x)**2 +
                           (pose.position.y - self.odom_pose.position.y)**2 +
                           (pose.position.z - self.odom_pose.position.z)**2)
            # Check if any particle is within the range of 1 meter
            if rmse <= 1:
                self.particle_within_range = True
                break
        
        # If no particle is within the range of 1 meter, print True and stop the node
        if not self.particle_within_range:
            rospy.loginfo("True")
            rospy.signal_shutdown("No particles within the range of 1 meter.")

    def run(self):
        rospy.spin()

if __name__ == '__main__':
    particle_pose_checker = ParticlePoseRMSEChecker()
    particle_pose_checker.run()
