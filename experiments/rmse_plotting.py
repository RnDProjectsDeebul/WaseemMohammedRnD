import matplotlib.pyplot as plt

# Sample data for two sets of points
optimal_x = [1, 3, 50, 100, 250, 500]
optimal_y = [0.8748, 0.2616, 0.2382, 0.2241, 0.1333, 0.1699]

amcl_02_x = [1, 3, 50, 100, 250, 500]
amcl_02_y = [5.9054, 4.3052, 4.4013, 3.0034, 3.6736, 2.7158]


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

#plt.yscale('log')
#plt.xscale('log')
#yticks = [1, 10, 100, 1000]  # Add more values as needed
#plt.yticks(yticks, [str(val) for val in yticks])


# Adding labels and title
plt.xlabel('Number of particles')
plt.ylabel('RMSE (cm)')
plt.title('Errors vs Number of particles')

# Adding legend
plt.legend()

# Show the plot
plt.show()
