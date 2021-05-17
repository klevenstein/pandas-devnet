import numpy as np
import pandas as pd
import json
import os

def obtain_df():
    script_directory = os.path.dirname(__file__) #absolute dir of script
    file_name = 'flow-results.json'
    abs_file_path = os.path.join(script_directory, file_name)
    with open(abs_file_path) as file:
        flow_data = json.load(file)
    df = pd.DataFrame.from_dict(flow_data)
    return df

if __name__ == '__main__':
    df = obtain_df()
    print(df.head())
