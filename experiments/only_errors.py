import csv
import matplotlib.pyplot as plt

def extract_and_plot_multiple_csv(files):
    try:
        all_values = []

        for file_path in files:
            with open(file_path, 'r') as file:
                csv_reader = csv.reader(file)

                # Lists to store values for plotting
                file_values = []

                # Loop through each row, concatenate values, and stop when a blank row is encountered
                for row in csv_reader:
                    if not row:
                        # Stop processing when a blank row is encountered
                        break

                    # Convert values to float for plotting
                    row_values = [float(value) for value in row]

                    # Concatenate the values to create a continuous line for each file
                    file_values.extend(row_values)

                # Append values for the current file to the overall list
                all_values.append(file_values)

        # Plot all six lines on the same plot
        for i, values in enumerate(all_values):
            if i==0:
                plt.plot(values, label='1 particle')
            if i==1:
                plt.plot(values, label='3 particles')
            if i==2:
                plt.plot(values, label='50 particles')
            if i==3:
                plt.plot(values, label='100 particles')
            if i==4:
                plt.plot(values, label='250 particles')
            if i==5:
                plt.plot(values, label='500 particles')

        # Add labels and legend
        plt.xlabel('Index')
        plt.ylabel('errors (m)')
        plt.legend()
        plt.title('Optimal Filter')

        # Add grid
        plt.grid(True)

        # Set y-axis limits for smaller scale
        plt.ylim(0, 2)  # Adjust the limits according to your data range

        # Show the plot
        plt.show()

    except FileNotFoundError as e:
        print(f"File not found: {e.filename}")
    except Exception as e:
        print(f"An error occurred: {e}")

# Replace the list with the actual file paths
file1 = '/home/waseem/Documents/HBRS/RnD/catkin_ws/src/experiments/kidnap_test/random/optimal/optimal_1_particles.csv'
file2 = '/home/waseem/Documents/HBRS/RnD/catkin_ws/src/experiments/kidnap_test/random/optimal/optimal_3_particles.csv'
file3 = '/home/waseem/Documents/HBRS/RnD/catkin_ws/src/experiments/kidnap_test/random/optimal/optimal_50_particles.csv'
file4 = '/home/waseem/Documents/HBRS/RnD/catkin_ws/src/experiments/kidnap_test/random/optimal/optimal_100_particles.csv'
file5 = '/home/waseem/Documents/HBRS/RnD/catkin_ws/src/experiments/kidnap_test/random/optimal/optimal_250_particles.csv'
file6 = '/home/waseem/Documents/HBRS/RnD/catkin_ws/src/experiments/kidnap_test/random/optimal/optimal_500_particles.csv'
file_paths = [file1, file2, file3, file4,file5, file6]
extract_and_plot_multiple_csv(file_paths)
