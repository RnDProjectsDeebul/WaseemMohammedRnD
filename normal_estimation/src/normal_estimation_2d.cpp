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
ros::Publisher scan_cloud_pub;

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
        "/base_footprint",
        scan_in->header.stamp + ros::Duration().fromSec(scan_in->ranges.size() * scan_in->time_increment),
        ros::Duration(1.0))) {
        return;
    }
    ROS_INFO("hehee");

    sensor_msgs::PointCloud cloud;
    projector_.transformLaserScanToPointCloud("/base_footprint", *scan_in, cloud, listener_);


    pcl::PointCloud<pcl::PointXYZ>::Ptr pcl_cloud(new pcl::PointCloud<pcl::PointXYZ>);

    // Convert sensor_msgs::PointCloud to pcl::PointCloud<pcl::PointXYZ>
    for (const auto& point : cloud.points) {
        pcl::PointXYZ pcl_point;
        pcl_point.x = point.x;
        pcl_point.y = point.y;
        pcl_point.z = point.z;
        pcl_cloud->push_back(pcl_point);
    }
    publishCloud(pcl_cloud, scan_cloud_pub, scan_in->header);

    // Create the normal estimation class
    pcl::NormalEstimation<pcl::PointXYZ, pcl::Normal> ne;
    ne.setInputCloud(pcl_cloud);

    // Create a KdTree for normal estimation
    pcl::search::KdTree<pcl::PointXYZ>::Ptr tree(new pcl::search::KdTree<pcl::PointXYZ>());
    ne.setSearchMethod(tree);

    // Output dataset for normals
    pcl::PointCloud<pcl::Normal>::Ptr cloud_normals(new pcl::PointCloud<pcl::Normal>);

    // Set the radius for normal estimation
    ne.setRadiusSearch(0.3); //TODO know how it effects and fix it

    // Compute the normals
    ne.compute(*cloud_normals);

    // Combine the points and normals into a single PointCloudNormal object
    PointCloudNormal::Ptr cloud_with_normals(new PointCloudNormal());
    pcl::concatenateFields(*pcl_cloud, *cloud_normals, *cloud_with_normals);
    ROS_INFO("hehee");
    
    ROS_INFO("IN!!!!1:");
    // Print pcl_cloud (point coordinates)
    std::cout << "pcl_cloud:\n";
    for (size_t i = 0; i < pcl_cloud->points.size(); ++i) {
        std::cout << "Point " << i << ": "
                  << "(" << pcl_cloud->points[i].x << ", "
                  << pcl_cloud->points[i].y << ", "
                  << pcl_cloud->points[i].z << ")\n";
    }
    
    // Print cloud_normals (normal vectors)
    std::cout << "\ncloud_normals:\n";
    for (size_t i = 0; i < cloud_normals->points.size(); ++i) {
        std::cout << "Normal " << i << ": "
                  << "(" << cloud_normals->points[i].normal_x << ", "
                  << cloud_normals->points[i].normal_y << ", "
                  << cloud_normals->points[i].normal_z << ")\n";
    }
    
    // Print cloud_with_normals (combined cloud)
    std::cout << "\ncloud_with_normals:\n";
    for (size_t i = 0; i < cloud_with_normals->points.size(); ++i) {
        std::cout << "Point " << i << ": "
                  << "(" << cloud_with_normals->points[i].x << ", "
                  << cloud_with_normals->points[i].y << ", "
                  << cloud_with_normals->points[i].z << ") - "
                  << "Normal: "
                  << "(" << cloud_with_normals->points[i].normal_x << ", "
                  << cloud_with_normals->points[i].normal_y << ", "
                  << cloud_with_normals->points[i].normal_z << ")\n";
    }


    publishCloud(cloud_with_normals, cloud_pub, scan_in->header);



}

int main(int argc, char **argv)
{
    ros::init(argc, argv, "normal_estimation_2d");
    ros::NodeHandle nh("~");

    ros::Subscriber scan_sub = nh.subscribe("/scan", 1, scanCallback);
    cloud_pub = nh.advertise<sensor_msgs::PointCloud2> ("/lidar_point_normals", 1);
    scan_cloud_pub = nh.advertise<sensor_msgs::PointCloud2>("/rslidar_points", 1); 

    ros::spin();

    return 0;
}
