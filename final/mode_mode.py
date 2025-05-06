import pandas as pd
import numpy as np
from scipy.stats import mode

# Load the CSV files
# df2 = pd.read_csv('predictions.csv')
# df1 = pd.read_csv('../CNN_predictions.csv')

df2 = pd.read_csv('presentation_predictions.csv')
df1 = pd.read_csv('../presentation_CNN_predictions.csv')

# Ensure we're working with the last column
last_col_index = -1

# Number of rows per chunk
chunk_size = 20

new_labels = []

# Create a new list to store the average mode values for each chunk
new_column_values = []

# Iterate over chunks of 20 rows
for start in range(0, len(df1), chunk_size):
    end = min(start + chunk_size, len(df1))  # Handle the last chunk which may be smaller than 20
    chunk1_last_col = df1.iloc[start:end, last_col_index]
    chunk2_last_col = df2.iloc[start:end, last_col_index]

    # Calculate the mode of the last column for both chunks
    mode1_result = mode(chunk1_last_col)
    mode2_result = mode(chunk2_last_col)

    # Check if mode result is empty, and default to 0 if it is
    # mode1 = mode1_result.mode[0] if mode1_result.mode.size > 0 else 0
    # mode2 = mode2_result.mode[0] if mode2_result.mode.size > 0 else 0
    
    mode1 = mode1_result.mode
    mode2 = mode2_result.mode

    # print(mode1, mode2)

    # Calculate the average of the two modes
#     avg_mode = (mode1 + mode2) / 2
#     new_column_values.extend([avg_mode] * (end - start)).astype(int)  # Repeat the average mode for the chunk length

# # Add the new column to df1
# df1['Attack_label'] = new_column_values[:len(df1)]  # Slice to match df1 length

# # Save or display the updated dataframe
# # print(df1.head())
# df1.to_csv('updated_file1.csv', index=False)

    # Average of the modes and round to 0 or 1
    avg_label = round((mode1 + mode2) / 2)
    
    # Append the same label for each row in the chunk
    new_labels.extend([avg_label] * (end - start))

# Assign the new labels to the last column of df1 (or create a new column)
df1 = df1.iloc[:len(new_labels)].copy()
df1['Attack_label'] = np.array(new_labels).astype(int)  # Convert to int

# Save result
df1.to_csv('mode_mode.csv', index=False)
print("Labeled output saved to 'mode_mode.csv'")