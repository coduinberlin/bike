import time
import pandas as pd
import numpy as np


#First section
DATA_FILES = {
    'chicago': 'chicago.csv',
    'nyc': 'new_york_city.csv',
    'dc': 'washington.csv'
}

def request_user_input():
    print('Welcome! Ready to dive into US bikeshare data?')
    while True:
        selected_city = input("Enter the city (Chicago, NYC, DC): ").lower()
        if selected_city in DATA_FILES:
            break
        print("Please enter a valid city name: Chicago, NYC, or DC.")

#explaining months
    valid_months = ['january', 'february', 'march', 'april', 'may', 'june', 'all']
    while True:
        selected_month = input("Choose a month to filter by (January to June or 'all'): ").lower()
        if selected_month in valid_months:
            break
        print("Invalid choice. Select a month from January to June or type 'all'.")

    valid_days = ['monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday', 'sunday', 'all']
    while True:
        selected_day = input("Choose a day to filter by (Monday to Sunday or 'all'): ").lower()
        if selected_day in valid_days:
            break
        print("Invalid choice. Select a day from Monday to Sunday or type 'all'.")

    print('-'*40)
    return selected_city, selected_month, selected_day

def fetch_data(selected_city, selected_month, selected_day):
    data_frame = pd.read_csv(DATA_FILES[selected_city])
    data_frame['Start Time'] = pd.to_datetime(data_frame['Start Time'])
    data_frame['month'] = data_frame['Start Time'].dt.month
    data_frame['week_day'] = data_frame['Start Time'].dt.day_name()

    if selected_month != 'all':
        month_index = valid_months.index(selected_month) + 1
        data_frame = data_frame[data_frame['month'] == month_index]

    if selected_day != 'all':
        data_frame = data_frame[data_frame['week_day'] == selected_day.title()]

    return data_frame

def travel_time_stats(data_frame):
    print('\nEvaluating Most Frequent Travel Times...\n')
    start_time = time.time()

    popular_month = data_frame['month'].mode()[0]
    print('Most Popular Month:', popular_month)

    popular_day = data_frame['week_day'].mode()[0]
    print('Most Popular Day:', popular_day)

    data_frame['hour'] = data_frame['Start Time'].dt.hour
    popular_hour = data_frame['hour'].mode()[0]
    print('Most Popular Start Hour:', popular_hour)

    print("\nTime elapsed: %s seconds." % (time.time() - start_time))
    print('-'*40)

def station_statistics(data_frame):
    print('\nCalculating Station Popularity...\n')
    start_time = time.time()

    common_start = data_frame['Start Station'].mode()[0]
    print('Most Common Start Station:', common_start)

    common_end = data_frame['End Station'].mode()[0]
    print('Most Common End Station:', common_end)

    common_trip = data_frame.groupby(['Start Station', 'End Station']).size().nlargest(1)
    print('Most Common Trip:', common_trip.index[0])

    print("\nTime elapsed: %s seconds." % (time.time() - start_time))
    print('-'*40)

def duration_statistics(data_frame):
    print('\nCalculating Trip Durations...\n')
    start_time = time.time()

    total_duration = data_frame['Trip Duration'].sum()
    print('Total Duration of Trips:', total_duration)

    average_duration = data_frame['Trip Duration'].mean()
    print('Average Duration of Trips:', average_duration)

    print("\nTime elapsed: %s seconds." % (time.time() - start_time))
    print('-'*40)

def demographics_statistics(data_frame):
    print('\nCalculating Demographic Information...\n')
    start_time = time.time()

    if 'User Type' in data_frame:
        user_types = data_frame['User Type'].value_counts()
        print('User Types:', user_types)

    if 'Gender' in data_frame:
        gender_distribution = data_frame['Gender'].value_counts()
        print('Gender Distribution:', gender_distribution)

    if 'Birth Year' in data_frame:
        earliest_birth = int(data_frame['Birth Year'].min())
        recent_birth = int(data_frame['Birth Year'].max())
        common_birth = int(data_frame['Birth Year'].mode()[0])
        print('Earliest Birth Year:', earliest_birth)
        print('Most Recent Birth Year:', recent_birth)
        print('Most Common Birth Year:', common_birth)

    print("\nTime elapsed: %s seconds." % (time.time() - start_time))
    print('-'*40)

def raw_data_display(data_frame):
    index = 0
    show_data = input('\nWould you like to see raw data? Enter yes or no.\n')
    while show_data.lower() == 'yes':
        print(data_frame.iloc[index:index+5])
        index += 5
        show_data = input('\nWould you like to see more raw data? Enter yes or no.\n')
        if index >= len(data_frame):
            print("No more data to display.")
            break

def main():
    while True:
        selected_city, selected_month, selected_day = request_user_input()
        data_frame = fetch_data(selected_city, selected_month, selected_day)

        travel_time_stats(data_frame)
        station_statistics(data_frame)
        duration_statistics(data_frame)
        demographics_statistics(data_frame)
        raw_data_display(data_frame)

        restart = input('\nDo you want to restart the data program? Enter yes or no.\n')
        if restart.lower() != 'yes':
            break

if __name__ == "__main__":
    main()
