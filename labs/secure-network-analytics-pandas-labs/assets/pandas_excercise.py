import pandas as pd
import json
import os
import numpy as np

## Hands-on excercise: import dataset with Python
script_directory = os.path.dirname(__file__) #absolute dir of script
file_name_json = 'flow-results.json'
abs_file_path_json = os.path.join(script_directory, file_name_json)
file_name_csv = 'flow-results.csv'
abs_file_path_csv = os.path.join(script_directory, file_name_csv)

def obtain_df_from_dict():
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

## Hands-on excercise: Calculate average bytes per flow
## Average bytes per flow    
def text_to_num(text, bad_data_val = 0):
    letter_to_number_dict = {
        'K': 1000,
        'M': 1000000,
        'B': 1000000000
    }
    if not isinstance(text, str):
        # Non-strings are missing data 
        return bad_data_val
    elif '--' in text:
        return bad_data_val
    elif text[-1] in letter_to_number_dict:
        # separate out the K, M, or B
        num, letter = text[:-2], text[-1]
        return int(float(num) * letter_to_number_dict[letter])
    else:
        return float(text)

def average_bytes_per_flow(df):
    df['Total Bytes'] = df['Total Bytes'].apply(text_to_num)
    average = df['Total Bytes'].mean()
    return average

## Hands-on excercise: calculate average bytes per flow per host group
## Calculate avereage bytes per flow per hostgroup

def strip_host_groups(text):
    split_string_array = text.split(",")
    first_host_group = split_string_array[0]
    return first_host_group

def average_bytes_per_flow_per_hostgroup(df):
    aggregates_dict = {}
    for _, row in df.iterrows():
        subject_peer_pair = row['Subject Host Groups'] + ":" + row['Peer Host Groups']
        if subject_peer_pair in aggregates_dict:
            aggregates_dict[subject_peer_pair].append(row['Total Bytes'])
        else:
            aggregates_dict[subject_peer_pair] = [row['Total Bytes']]

    averages_dict = {}
    for key in aggregates_dict:
        total_bytes_per_hostgroup = aggregates_dict[key]
        average_bytes_per_flow_per_hostgroup = np.mean(total_bytes_per_hostgroup)
        averages_dict[key] = average_bytes_per_flow_per_hostgroup

    return averages_dict

def aggregate_bytes_per_hostgroup_sent_or_received(df, sent_or_received):
    if sent_or_received == "sent":
        peer_or_subject_bytes = "Subject Bytes"
    elif sent_or_received == "received":
        peer_or_subject_bytes = "Peer Bytes"
    else:
        raise Exception("Only 'sent' or 'received' allowed")

    aggregates_dict = {}
    for _, row in df.iterrows():
        subject_host_group = row['Subject Host Groups']
        number_of_bytes = row[peer_or_subject_bytes]
        if not subject_host_group in aggregates_dict:
            aggregates_dict[subject_host_group] = [number_of_bytes]
        else:
            aggregates_dict[subject_host_group].append(number_of_bytes)
    return aggregates_dict

def average_bytes_per_hostgroup_sent_or_received(df, sent_or_received):
    aggregates_dict = aggregate_bytes_per_hostgroup_sent_or_received(df, sent_or_received)
    results_dict = {}
    for hostgroup in aggregates_dict:
        total_bytes = aggregates_dict[hostgroup]
        average_bytes = np.mean(total_bytes)
        results_dict[hostgroup] = average_bytes
    return results_dict


## Hands-on excercise: detect above-average flows
## Detect above-average flows

def plot_flows(aggregates_dict, sent_or_received):
    for subject_host_group in aggregates_dict:
        plt.figure()
        x = np.arange(len(aggregates_dict[subject_host_group]))
        y = np.array(aggregates_dict[subject_host_group])

        plt.plot(x,y)
        plt.title(f'The number of bytes {sent_or_received} from {subject_host_group}')
        plt.ylabel('Bytes')
        
        plt.show()

def detect_above_average_flows(df_baseline, df_test):
    baseline_dict = average_bytes_per_flow_per_hostgroup(df_baseline)
    test_dict = average_bytes_per_flow_per_hostgroup(df_test)

    results_dict = {}

    for subject_peer_pair in test_dict:
        # subject peer pair does not exist
        if not subject_peer_pair in baseline_dict:
            results_dict[subject_peer_pair] = -1
        # flow is less than or equal to baseline
        if test_dict[subject_peer_pair] <= baseline_dict[subject_peer_pair]:
            results_dict[subject_peer_pair] = 0 
        # flow is more than the baseline
        else:
            results_dict[subject_peer_pair] = 1

    return results_dict


def main():
    # Hands-on excercise: import dataset with Python
    #TODO df = obtain_df_from_dict()
    #TODO print(df.head())
    #TODO print(df.tail())

    # Hands-on excercise: Calculate average bytes per flow
    #TODO df['Total Bytes'] =  df['Total Bytes'].apply(text_to_num)
    #TODO df['Subject Bytes'] =  df['Subject Bytes'].apply(text_to_num)
    #TODO df['Peer Bytes'] =  df['Peer Bytes'].apply(text_to_num)
    #TODO print("The average bytes per flow is ", df['Total Bytes'].mean())

    # Hands-on excercise: calculate average bytes per flow per host group
    #TODO df['Subject Host Groups'] =  df['Subject Host Groups'].apply(strip_host_groups)
    #TODO df['Peer Host Groups'] =  df['Peer Host Groups'].apply(strip_host_groups)

    #TODO total_sent = aggregate_bytes_per_hostgroup_sent_or_received(df, 'sent')
    #TODO total_received = aggregate_bytes_per_hostgroup_sent_or_received(df, 'received')
    #TODO print(average_bytes_per_hostgroup_sent_or_received(df, 'sent'))
    #TODO print(average_bytes_per_hostgroup_sent_or_received(df, 'received'))

    # Hands-on excercise: detect above-average flows
    #TODO plot_flows(total_sent, 'sent')
    #TODO plot_flows(total_received, 'received)
    



if __name__ == '__main__':
    main()
