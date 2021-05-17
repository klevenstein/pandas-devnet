import numpy as np
import pandas as pd
import json
import os

script_directory = os.path.dirname(__file__) #absolute dir of script
file_name_json = 'flow-results.json'
abs_file_path_json = os.path.join(script_directory, file_name_json)
file_name_csv = 'flow-results.csv'
abs_file_path_csv = os.path.join(script_directory, file_name_csv)

def obtain_df():
    with open(abs_file_path_json) as file:
        flow_data = json.load(file)
    df = pd.DataFrame.from_dict(flow_data)
    return df

def obtain_df_from_json():
    df = pd.read_json(abs_file_path_json)
    return df

def obtain_df_from_csv():
    df = pd.read_csv(abs_file_path_csv)
    return df

if __name__ == '__main__':
    df = obtain_df()
    print(df.head())
