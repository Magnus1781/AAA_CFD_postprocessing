import csv

# Read the data into a list of lines
with open('/Users/magnuswennemo/Library/CloudStorage/OneDrive-SINTEF/scripts/inlet_velocity_profile.csv', 'r') as file:
    reader = csv.reader(file)
    lines = list(reader)

# Filter out every second row starting with 0.01
filtered_lines = [lines[0]]  # Keep the header
filtered_lines.extend(line for i, line in enumerate(lines[1:], start=0) if i % 2 == 0)

# Write the filtered data to a new CSV file
output_file = '/Users/magnuswennemo/Library/CloudStorage/OneDrive-SINTEF/scripts/inlet_velocity_profile_half.csv'
with open(output_file, 'w', newline='') as file:
    writer = csv.writer(file)
    writer.writerows(filtered_lines)
