# Research and Development (R&D) Project Overview
This repository is developed as a part of an ongoing research and development (R&D) project aimed at advancing LiDAR-based indoor localization using particle filters. Particle filters offer a robust approach to estimating robot position and orientation within various environments, but challenges such as particle degeneracy and accuracy-robustness trade-offs need to be addressed. Drawing inspiration from existing advancements in integrating surface normals in 3D systems [1], this project seeks to extend these principles to a 2D framework, enhancing the precision and reliability of indoor localization.

# Key Objectives
The core objectives of this R&D project encompass both theoretical and practical aspects of integrating surface normal constraints into 2D LiDAR-based particle filters. The research will focus on designing novel methodologies to incorporate surface normals in a 2D context while addressing challenges unique to this scenario. These methodologies will be rigorously benchmarked and tested, assessing their impact on the accuracy and performance of the localization system. This comparative analysis will provide empirical evidence of the benefits derived from surface normal incorporation in the 2D LiDAR setting, highlighting its potential to enhance indoor localization precision and dependability.

# Repository Usage
This repository provides comprehensive instructions on setting up and running optimal particle filter in 3D environment within the Gazebo simulation. It also covers the creation of a 3D model, the mapping process, and the integration of noisy odometry for precise localization, all utilizing the Robot Operating System (ROS).

# Gazebo Simulation and Mapping README

This repository provides instructions on how to set up a Gazebo simulation, create a 3D model, perform mapping, and add noisy odometry for localization using ROS (Robot Operating System).

## Data Collection

1. **Create 3D Model**: Use the Gazebo Building Editor to create a 3D model. Save the world file in the "velodyne_simulator/velodyne_description/world/" directory. Example world files can be found in the same folder.

    ```shell
    export World="world_name"
    roslaunch velodyne_description simulation.launch
    rosrun velodyne_description teleop_twist_keyboard.py
    rosbag record /rslidar_points /ground_truth_odom /ground_truth_pose /tf /tf_static
    ```

## Mapping

1. **Launch Mapping Node**: Launch the simulation mapping node to start the mapping process.

    ```shell
    roslaunch simulation_mapping simulation_mapping.launch
    rosbag play --clock map_bag_file.bag
    ```

    The map will be saved to the "/tmp" folder as a PCD file when the mapping node is closed. You can view it using pcl_viewer. The file "/tmp/sim_ground_truth_normals_map.pcd" can be used with `mcl_optimal`.

## Add Noisy Odometry for Localization

1. **Add Noisy Odometry Topic**: To simulate noisy odometry data for localization, use the provided Python script to add an "odom" topic to the bag files collected from the Gazebo simulation with drift.

    ```shell
    python add_odom_noise.py bag_file.bag
    ```

---

# Reference 
[1] [LiDAR-based Indoor Localization with Optimal Particle Filters using Surface Normal Constraints](https://ieeexplore.ieee.org/document/10160274)
