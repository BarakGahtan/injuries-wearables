import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from sklearn.preprocessing import StandardScaler
from sklearn.cluster import KMeans
from collections import defaultdict
def generate_stats(df):
    # Assuming your DataFrame is named df and the column is 'timestamp_column'
    # Convert the 'timestamp_column' to pandas datetime format
    df['startTimeDate'] = pd.to_datetime(df['startTimeDate'])
    date_counts = df['startTimeDate'].dt.date.value_counts()
    unique_days = len(date_counts)
    data_points_per_day = df.groupby(df['startTimeDate'].dt.date)['startTimeDate'].nunique()
    # Calculate the average number of timings per day
    average_data_points_per_day = data_points_per_day.mean()
    return unique_days, average_data_points_per_day


def hist_visualize_stats_per_all(data_dict):
    x_values = [inner_dict['deep_sleep_avg_datapoints_per_day'] for inner_dict in data_dict.values()]
    # Create a histogram to visualize the distribution
    plt.hist(x_values, bins=50, edgecolor='black')
    plt.xlabel(' deep_sleep_avg_datapoints_per_day')
    plt.ylabel('soldiers count')
    plt.title('Distribution of deep_sleep_avg_datapoints_per_day per day')
    plt.savefig('Distribution of deep_sleep_avg_datapoints_per_day per day.png', dpi=300)
    plt.show()

def preprocess_data(data):
    data['epoch'] = data['epoch'][['userId','userAccessToken','summaryId','activeKilocalories','steps','distanceInMeters','activeTimeInSeconds', 'startTimeInSeconds']]
    data['deep_sleep']['totalSeconds'] = data['deep_sleep']['endTimeInSeconds'] - data['deep_sleep']['startTimeInSeconds']
    data['light_sleep']['totalSeconds'] = data['light_sleep']['endTimeInSeconds'] - data['light_sleep']['startTimeInSeconds']
    data['awake_sleep']['totalSeconds'] = data['awake_sleep']['endTimeInSeconds'] - data['awake_sleep']['startTimeInSeconds']
    data['epoch']['startTimeDate'] = pd.to_datetime(data['epoch']['startTimeInSeconds'], unit='s')
    data['deep_sleep']['startTimeDate'] = pd.to_datetime(data['deep_sleep']['startTimeInSeconds'], unit='s')
    data['light_sleep']['startTimeDate'] = pd.to_datetime(data['light_sleep']['startTimeInSeconds'], unit='s')
    data['awake_sleep']['startTimeDate'] = pd.to_datetime(data['awake_sleep']['startTimeInSeconds'], unit='s')
    unique_ids = data['heart_rate_daily']['userId'].unique()
    unique_dict_ids = {}
    for id in unique_ids:
        filtered_light_sleep = data['light_sleep'][data['light_sleep']['userId'] == id].reset_index().drop(columns=['index','summaryId'],inplace=False)
        filtered_awake_sleep = data['awake_sleep'][data['awake_sleep']['userId'] == id].reset_index().drop(columns=['index','summaryId'],inplace=False)
        filtered_deep_sleep = data['deep_sleep'][data['deep_sleep']['userId'] == id].reset_index().drop(columns=['index','summaryId'],inplace=False)
        filtered_epoch = data['epoch'][data['epoch']['userId'] == id].reset_index().drop(columns=['index','userAccessToken','summaryId'],inplace=False)
        filtered_hr = data['heart_rate_daily'][data['heart_rate_daily']['userId'] == id].reset_index().drop(columns=['index','dailiessummaryId'],inplace=False)
        epoch_unique_days, epoch_avg_datapoints__per_day = generate_stats(filtered_epoch)
        deep_sleep_unique_days, deep_sleep_avg_datapoints__per_day = generate_stats(filtered_deep_sleep)
        awake_sleep_unique_days, awake_sleep_avg_datapoints_per_day = generate_stats(filtered_awake_sleep)
        light_sleep_unique_days, light_sleep_avg_datapoints_per_day = generate_stats(filtered_light_sleep)
        unique_dict_ids[id] = {'light_sleep': filtered_light_sleep, 'awake_sleep':filtered_awake_sleep, 'deep_sleep':filtered_deep_sleep,
                               'epoch':filtered_epoch, 'heart_rate':filtered_hr,'epoch_unique_days': epoch_unique_days,
                               'epoch_avg_datapoints__per_day': epoch_avg_datapoints__per_day,
                               'deep_sleep_unique_days': deep_sleep_unique_days, 'deep_sleep_avg_datapoints_per_day':deep_sleep_avg_datapoints__per_day,
                               'awake_sleep_unique_days':awake_sleep_unique_days, 'awake_sleep_avg_datapoints_per_day': awake_sleep_avg_datapoints_per_day,
                               'light_sleep_unique_days': light_sleep_unique_days, 'light_sleep_avg_datapoints_per_day': light_sleep_avg_datapoints_per_day}
        hist_visualize_stats_per_all(unique_dict_ids)

