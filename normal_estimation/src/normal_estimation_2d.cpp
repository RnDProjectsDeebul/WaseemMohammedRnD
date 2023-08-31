#include <ros/ros.h>
#include <sensor_msgs/LaserScan.h>
#include <sensor_msgs/PointCloud.h>
#include <laser_geometry/laser_geometry.h>
#include <tf/transform_listener.h>
#include <pcl/point_types.h>
#include <pcl/features/normal_3d.h>
#include <pcl/search/kdtree.h>
#include "pcl_ros/point_cloud.h"
#include <normal_estimation/normal_estimation.h>

laser_geometry::LaserProjection projector_;
ros::Publisher cloud_pub;

template<typename T>
void publishCloud(T& cloud, ros::Publisher& publisher, std_msgs::Header header){
    sensor_msgs::PointCloud2 output;
    pcl::toROSMsg(*cloud, output);
    output.header.frame_id = header.frame_id;
    output.header.stamp = header.stamp;
    publisher.publish(output);
}

void scanCallback(const sensor_msgs::LaserScan::ConstPtr& scan_in)
{

    // sensor_msgs::PointCloud cloud;
    // projector_.projectLaser(*scan_in, cloud);
    tf::TransformListener listener_;
    if (!listener_.waitForTransform(
        scan_in->header.frame_id,
        "/base_link",
        scan_in->header.stamp + ros::Duration().fromSec(scan_in->ranges.size() * scan_in->time_increment),
        ros::Duration(1.0))) {
        return;
    }

    sensor_msgs::PointCloud cloud;
    projector_.transformLaserScanToPointCloud("/base_link", *scan_in, cloud, listener_);
    ROS_INFO("IN!!!!");


    pcl::PointCloud<pcl::PointXYZ>::Ptr pcl_cloud(new pcl::PointCloud<pcl::PointXYZ>);

    // Convert sensor_msgs::PointCloud to pcl::PointCloud<pcl::PointXYZ>
    for (const auto& point : cloud.points) {
        pcl::PointXYZ pcl_point;
        pcl_point.x = point.x;
        pcl_point.y = point.y;
        pcl_point.z = point.z;
        pcl_cloud->push_back(pcl_point);
    }

    // Create the normal estimation class
    pcl::NormalEstimation<pcl::PointXYZ, pcl::Normal> ne;
    ne.setInputCloud(pcl_cloud);

    // Create a KdTree for normal estimation
    pcl::search::KdTree<pcl::PointXYZ>::Ptr tree(new pcl::search::KdTree<pcl::PointXYZ>());
    ne.setSearchMethod(tree);

    // Output dataset for normals
    pcl::PointCloud<pcl::Normal>::Ptr cloud_normals(new pcl::PointCloud<pcl::Normal>);

    // Set the radius for normal estimation
    ne.setRadiusSearch(0.03);

    // Compute the normals
    ne.compute(*cloud_normals);

    // Combine the points and normals into a single PointCloudNormal object
    PointCloudNormal::Ptr cloud_with_normals(new PointCloudNormal());
    pcl::concatenateFields(*pcl_cloud, *cloud_normals, *cloud_with_normals);
    
     ROS_INFO("IN!!!!1:");


    publishCloud(cloud_with_normals, cloud_pub, scan_in->header);



}

int main(int argc, char **argv)
{
    ros::init(argc, argv, "normal_estimation_2d");
    ros::NodeHandle nh("~");

    ros::Subscriber scan_sub = nh.subscribe("/sk/laser/scan", 1, scanCallback);
    cloud_pub = nh.advertise<sensor_msgs::PointCloud2> ("/lidar_point_normals", 1);

    ros::spin();

    return 0;
}
