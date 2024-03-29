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
#include <normal_estimation/NormalList.h>

laser_geometry::LaserProjection projector_;
ros::Publisher cloud_pub;
ros::Publisher scan_cloud_pub;

pcl::PointCloud<pcl::Normal>::Ptr cloud_normals(new pcl::PointCloud<pcl::Normal>);

template<typename T>
void publishCloud(T& cloud, ros::Publisher& publisher, std_msgs::Header header){
    sensor_msgs::PointCloud2 output;
    pcl::toROSMsg(*cloud, output);
    output.header.frame_id = header.frame_id;
    output.header.stamp = header.stamp;
    publisher.publish(output);
}

void publishNormals(const pcl::PointCloud<pcl::PointXYZ>::Ptr& pcl_cloud, const std_msgs::Header& header) {
    // Publish cloud with normals
    PointCloudNormal::Ptr cloud_with_normals(new PointCloudNormal());
    std::cout << "\npcl_cloud: " << pcl_cloud->points.size() <<"\n";
    std::cout << "\ncloud_normals: " << cloud_normals->points.size() <<"\n";
    pcl::concatenateFields(*pcl_cloud, *cloud_normals, *cloud_with_normals);
    publishCloud(cloud_with_normals, cloud_pub, header);
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
}

void normalsCallback(const normal_estimation::NormalList::ConstPtr& normals_msg)  {
    // Clear previous normals
    cloud_normals->clear();

    // Fill in the received normal vectors
    for (size_t i = 0; i < normals_msg->x.size(); ++i) {
        pcl::Normal normal;
        normal.normal_x = normals_msg->x[i];
        normal.normal_y = normals_msg->y[i];
        normal.normal_z = 0.0; // Assuming 2D, so setting z component to 0
        cloud_normals->push_back(normal);
    }
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
    sensor_msgs::PointCloud cloud;
    projector_.transformLaserScanToPointCloud("/base_footprint", *scan_in, cloud, listener_);


    pcl::PointCloud<pcl::PointXYZ>::Ptr pcl_cloud(new pcl::PointCloud<pcl::PointXYZ>);

    // Convert sensor_msgs::PointCloud to pcl::PointCloud<pcl::PointXYZ>
    for (const auto& point : cloud.points) {
        pcl::PointXYZ pcl_point;
        pcl_point.x = point.x;
        pcl_point.y = point.y;
        pcl_point.z = point.z;  // Keep the original Z value
        pcl_cloud->push_back(pcl_point);
    }
    std::cout << *pcl_cloud << std::endl;
    std::cout << "\npcl_cloud: " << pcl_cloud->points.size() <<"\n";
    publishCloud(pcl_cloud, scan_cloud_pub, scan_in->header);
    publishNormals(pcl_cloud, scan_in->header);

}

int main(int argc, char **argv)
{
    ros::init(argc, argv, "normal_estimation_2d");
    ros::NodeHandle nh("~");

    ros::Subscriber scan_sub = nh.subscribe("/scan", 1, scanCallback);
    ros::Subscriber normals_sub = nh.subscribe("/normals", 1, normalsCallback);
    cloud_pub = nh.advertise<sensor_msgs::PointCloud2> ("/lidar_point_normals", 1);
    scan_cloud_pub = nh.advertise<sensor_msgs::PointCloud2>("/rslidar_points", 1); 

    ros::spin();

    return 0;
}