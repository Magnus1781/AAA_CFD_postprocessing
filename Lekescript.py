import pandas as pd

# Define input and output file names
input_file = "IR_flow_average_data.txt"      # Replace with your actual filename
output_file = "negative_IR_flow_average_data.txt"

# Load the dataset from the file
df = pd.read_csv(input_file, delim_whitespace=True)

# Change the sign of the flow_rate column
df['flow_rate'] *= -1

# Save the modified dataset to a new file
df.to_csv(output_file, index=False, sep=' ')

# Print confirmation
print(f"Modified dataset saved to {output_file}")
