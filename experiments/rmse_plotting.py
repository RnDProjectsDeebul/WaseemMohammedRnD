import matplotlib.pyplot as plt

# Sample data for two sets of points
optimal_x = [1, 2, 3, 50, 100, 150, 200, 300, 400, 500]
optimal_y = [0.0582, 0.0539, 0.0525, 0.0488, 0.0422, 0.0407, 0.0382, 0.0379, 0.0384, 0.0361]

amcl_02_x = [2, 50, 100, 250, 500]
amcl_02_y = [0.451453001283911, 0.228545458847096, 0.133401830189468, 0.143923078741679, 0.121763923154334]

amcl_3_x = [2, 50, 100, 250, 500]
amcl_3_y = [1.36647134216469, 1.18983828020106, 1.18372686877504, 1.15407840951296, 1.00522771310981]

amcl_2_x = [2, 50, 100, 250, 500]
amcl_2_y = [0.986112389359831, 0.856784928907747, 0.815305672388045, 0.818914614450198, 0.800719487874905]

amcl_1_x = [2, 50, 100, 250, 500]
amcl_1_y = [1.02044530335032, 0.59820422714742, 0.495655590710975, 0.537982126205753, 0.497324468285762]


optimal_y = [y * 100 for y in optimal_y]
amcl_3_y = [y * 100 for y in amcl_3_y]
amcl_2_y = [y * 100 for y in amcl_2_y]
amcl_1_y = [y * 100 for y in amcl_1_y]
amcl_02_y = [y * 100 for y in amcl_02_y]

# Plotting lines for each set of points

fig = plt.figure(figsize=(16, 16))
plt.plot(optimal_x, optimal_y, label='Optimal particle filter')
plt.plot(amcl_3_x, amcl_3_y, label='AMCL std=3')
plt.plot(amcl_2_x, amcl_2_y, label='AMCL std=2')
plt.plot(amcl_1_x, amcl_1_y, label='AMCL std=1')
plt.plot(amcl_02_x, amcl_02_y, label='AMCL std=0.02')


# Adding squared dots at specific x positions

plt.scatter(optimal_x, optimal_y, marker='s', color='red')

plt.scatter(amcl_3_x, amcl_3_y, marker='s', color='red')
plt.scatter(amcl_2_x, amcl_2_y, marker='s', color='red')
plt.scatter(amcl_1_x, amcl_1_y, marker='s', color='red')
plt.scatter(amcl_02_x, amcl_02_y, marker='s', color='red')

# Adding equal-sized grids
plt.grid(True)
# plt.gca().set_aspect('equal', adjustable='box')

# Adding labels and title
plt.xlabel('Number of particles')
plt.ylabel('RMSE (cm)')
plt.title('Translational errors vs Number of particles')

# Adding legend
plt.legend()

# Show the plot
plt.show()
