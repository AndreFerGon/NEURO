import pandas as pd
import matplotlib.pyplot as plt

# Step 1: Read the TSV file into a DataFrame
tsv_file = 'Protocol#1_202007965_21_Male_16Hz.csv'  # Specify the path to your TSV file

try:
    # Read the TSV file with tab delimiter and without specifying headers
    eeg_data = pd.read_csv(tsv_file, sep='\t', header=None)
except FileNotFoundError:
    print(f"Error: File '{tsv_file}' not found.")
    exit(1)
except pd.errors.EmptyDataError:
    print(f"Error: File '{tsv_file}' is empty.")
    exit(1)
except pd.errors.ParserError as e:
    print(f"Error: Unable to parse '{tsv_file}': {e}")
    exit(1)

# Step 2: Transpose the DataFrame to rearrange rows and columns
eeg_data_transposed = eeg_data.T  # Transpose DataFrame

# Step 3: Plot EEG data
plt.figure(figsize=(12, 6))  # Adjust figure size if needed

# Extract time values from the index (convert to string)
time_values = eeg_data_transposed.index.astype(str)

# Plot each EEG channel (convert values to float for plotting)
for i in range(1, eeg_data_transposed.shape[1]):  # Start from column 1 (index 1)
    channel_values = eeg_data_transposed[i].astype(float)  # Convert channel values to float
    plt.plot(time_values, channel_values, label=f'channel{i}')

# Add labels and title
plt.xlabel('Time')  # Assuming time values are represented by DataFrame index
plt.ylabel('EEG Amplitude')
plt.title('EEG Data Plot')

# Add legend
plt.legend()

# Show plot
plt.show()
