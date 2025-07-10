# importing libraries
import pandas as pd




# loading data
def load_data(input_file_path):
    return pd.read_csv(input_file_path)

# loading data
def save_data(data, output_file_path):
    data.to_csv(output_file_path, index=False)