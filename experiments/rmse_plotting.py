import matplotlib.pyplot as plt

# Sample data for two sets of points
optimal_x = [1, 3, 50, 100, 250, 500]
optimal_y = [0.12656, 0.11854, 0.07688, 0.07231, 0.07638, 0.08475]

amcl_02_x = [1, 3, 50, 100, 250, 500]
amcl_02_y = [0.55304, 0.55862, 0.54471, 0.22662, 0.25815, 0.17293]


optimal_y = [y * 100 for y in optimal_y]
amcl_02_y = [y * 100 for y in amcl_02_y]

# Plotting lines for each set of points

fig = plt.figure(figsize=(16, 16))
plt.plot(optimal_x, optimal_y, label='Optimal particle filter')
plt.plot(amcl_02_x, amcl_02_y, label='AMCL')


# Adding squared dots at specific x positions

plt.scatter(optimal_x, optimal_y, marker='s', color='red')

plt.scatter(amcl_02_x, amcl_02_y, marker='s', color='red')

# Adding equal-sized grids
plt.grid(True)
# plt.gca().set_aspect('equal', adjustable='box')

# plt.yscale('log')
#plt.xscale('log')
# yticks = [1, 10, 100, 1000]  # Add more values as needed
# plt.yticks(yticks, [str(val) for val in yticks])


# Adding labels and title
plt.xlabel('Number of particles')
plt.ylabel('RMSE (cm)')
plt.title('Translational errors vs Number of particles')

# Adding legend
plt.legend()

# Show the plot
plt.show()
