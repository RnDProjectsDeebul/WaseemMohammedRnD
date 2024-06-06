import open3d as o3d
import numpy as np

# Load the original point cloud
cloud = o3d.io.read_point_cloud("sim_ground_truth_normals_map.pcd")

# Define the offset in x-direction
offset_x = -10.0

# Get the points and normals from the cloud
points = np.asarray(cloud.points)
normals = np.asarray(cloud.normals)

# Get the curvatures from the cloud
curvatures = np.asarray(cloud.colors)  # Assuming curvature is stored in the color channel

# Print the original curvature values
print("Original Curvature Values:")
print(curvatures)
# Shift the x-coordinates of points
points[:, 0] += offset_x

# Shift the x-component of normals
normals[:, 0] += offset_x

# Create a new point cloud with shifted points and normals
shifted_cloud = o3d.geometry.PointCloud()
shifted_cloud.points = o3d.utility.Vector3dVector(points)
shifted_cloud.normals = o3d.utility.Vector3dVector(normals)


# Save the shifted point cloud to a new .pcd file
o3d.io.write_point_cloud("shifted_cloud_with_normals.pcd", shifted_cloud)
