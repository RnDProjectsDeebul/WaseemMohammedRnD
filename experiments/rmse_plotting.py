import matplotlib.pyplot as plt

# Sample data for two sets of points
optimal2d_x = [1, 3, 50, 100, 250, 500]
optimal2d_y = [0.07999, 0.06211, 0.06823, 0.07887, 0.07167, 0.07324]

optimal_x = [1, 3, 50, 100, 250, 500]
optimal_y = [0.87487, 0.26166, 0.23825, 0.22412, 0.16998, 0.1333]

amcl_02_x = [1, 3, 50, 100, 250, 500]
amcl_02_y = [5.90542, 4.30526, 4.40136, 3.00341, 3.67367, 2.7158486035]


optimal2d_y = [y * 100 for y in optimal2d_y]
optimal_y = [y * 100 for y in optimal_y]
amcl_02_y = [y * 100 for y in amcl_02_y]

# Plotting lines for each set of points

fig = plt.figure(figsize=(16, 16))
plt.plot(optimal2d_x, optimal2d_y, label='Optimal 2D particle filter')
plt.plot(optimal_x, optimal_y, label='Optimal particle filter')
plt.plot(amcl_02_x, amcl_02_y, label='AMCL')


# Adding squared dots at specific x positions

plt.scatter(optimal2d_x, optimal2d_y, marker='s')

plt.scatter(optimal_x, optimal_y, marker='s')

plt.scatter(amcl_02_x, amcl_02_y, marker='s')

# Adding equal-sized grids
plt.grid(True)
# plt.gca().set_aspect('equal', adjustable='box')

plt.yscale('log')
#plt.xscale('log')
yticks = [1, 10, 100, 1000]  # Add more values as needed
plt.yticks(yticks, [str(val) for val in yticks])


# Adding labels and title
plt.xlabel('Number of particles')
plt.ylabel('RMSE (cm)')
plt.title('Translational errors vs Number of particles')

# Adding legend
plt.legend()

# Show the plot
plt.show()
