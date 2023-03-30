#1 Popular times of travel (i.e., occurs most often in the start time)
#    most common month
#    most common day of week
 #   most common hour of day


import pandas as pd

def main():
    # load the data for the three cities
    chicago = pd.read_csv('chicago.csv')
    new_york_city = pd.read_csv('new_york_city.csv')
    washington = pd.read_csv('washington.csv')

    # concatenate the data for the three cities
    df = pd.concat([chicago, new_york_city, washington])

    # convert the Start Time column to datetime
    df['Start Time'] = pd.to_datetime(df['Start Time'])

    # extract month, day of week, and hour from the Start Time column
    df['Month'] = df['Start Time'].dt.month_name()
    df['Day of Week'] = df['Start Time'].dt.day_name()
    df['Hour'] = df['Start Time'].dt.hour

    # calculate the most common month
    common_month = df['Month'].mode()[0]
    print("The most common month is:", common_month)

    # calculate the most common day of week
    common_day = df['Day of Week'].mode()[0]
    print("The most common day of week is:", common_day)

    # calculate the most common hour of day
    common_hour = df['Hour'].mode()[0]
    print("The most common hour of day is:", common_hour)

    display_data(df)

def display_data(df):
    """
    Displays 5 rows of data and prompts the user if they want to see more.

    Args:
        df: Pandas DataFrame containing the trip data.
    """

    view_data = input('\nWould you like to view 5 rows of individual trip data? Enter yes or no\n').lower()

    # Initialize start location to 0
    start_loc = 0

    while view_data == 'yes':
        # Set end location to start location + 5
        end_loc = start_loc + 5

        # Print rows from start location to end location
        print(df.iloc[start_loc:end_loc])

        # Update start location for next iteration
        start_loc += 5

        # Prompt user if they want to see more rows
        view_data = input("Do you want to see the next 5 rows of data? Enter yes or no\n").lower()

if __name__ == '__main__':
    main()


#2 Popular stations and trip

#  most common start station
#  most common end station
#  most common trip from start to end (i.e., most frequent combination of start station and end station)

import pandas as pd

# load the data for the city specified
def load_data(city):
    df = pd.read_csv(city + '.csv')
    return df

# calculate the most popular start station
def popular_start_station(df):
    return df['Start Station'].mode()[0]

# calculate the most popular end station
def popular_end_station(df):
    return df['End Station'].mode()[0]

# calculate the most popular trip from start to end
def popular_trip(df):
    trip_counts = df.groupby(['Start Station', 'End Station']).size().reset_index(name='counts')
    trip_counts = trip_counts.sort_values('counts', ascending=False).reset_index(drop=True)
    return trip_counts.loc[0, 'Start Station'], trip_counts.loc[0, 'End Station']

# main function to call other functions
def main():
    city = input("Enter the city name (chicago, new_york_city, washington): ").lower()
    df = load_data(city)
    print("Most Popular Start Station: ", popular_start_station(df))
    print("Most Popular End Station: ", popular_end_station(df))
    start_station, end_station = popular_trip(df)
    print("Most Popular Trip from {} to {}: ".format(start_station, end_station))

    # prompt user to view individual trip data
    view_data = input('\nWould you like to view 5 rows of individual trip data? Enter yes or no\n').lower()

    # Initialize start location to 0
    start_loc = 0

    while view_data == 'yes':
        # Set end location to start location + 5
        end_loc = start_loc + 5

        # Print rows from start location to end location
        print(df.iloc[start_loc:end_loc])

        # Update start location for next iteration
        start_loc += 5

        # Prompt user if they want to see more rows
        view_data = input("Do you want to see the next 5 rows of data? Enter yes or no\n").lower()

if __name__ == '__main__':
    main()
    
    
#3 Trip duration

#    total travel time
#   average travel time

import pandas as pd

# specify the filenames for each city's CSV file
CITY_DATA = {'chicago': 'chicago.csv',
             'new york city': 'new_york_city.csv',
             'washington': 'washington.csv'}

def trip_duration_stats(city_file):
    """
    Calculates and prints statistics related to trip duration.
    
    Args:
        (str) city_file - name of the city's CSV file to load
    """
    # load data file into a dataframe
    df = pd.read_csv(city_file)
    
    # convert the 'Start Time' and 'End Time' columns to datetime
    df['Start Time'] = pd.to_datetime(df['Start Time'])
    df['End Time'] = pd.to_datetime(df['End Time'])
    
    # calculate the total travel time
    total_travel_time = df['Trip Duration'].sum()
    print('Total travel time: {} seconds'.format(total_travel_time))
    
    # calculate the mean travel time
    mean_travel_time = df['Trip Duration'].mean()
    print('Mean travel time: {} seconds'.format(mean_travel_time))


def display_data(df):
    """
    Displays 5 rows of data and prompts the user if they want to see more.

    Args:
        df: Pandas DataFrame containing the trip data.
    """

    view_data = input('\nWould you like to view 5 rows of individual trip data? Enter yes or no\n').lower()

    # Initialize start location to 0
    start_loc = 0

    while view_data == 'yes':
        # Set end location to start location + 5
        end_loc = start_loc + 5

        # Print rows from start location to end location
        print(df.iloc[start_loc:end_loc])

        # Update start location for next iteration
        start_loc += 5

        # Prompt user if they want to see more rows
        view_data = input("Do you want to see the next 5 rows of data? Enter yes or no\n").lower()


# test the function for each city
for city, filename in CITY_DATA.items():
    print('\n', '-'*40)
    print(city.title())
    print('-'*40)
    trip_duration_stats(filename)
    display_data(pd.read_csv(filename))


# 4 User info

#    counts of each user type
#    counts of each gender (only available for NYC and Chicago)
#    earliest, most recent, most common year of birth (only available for NYC and Chicago)


import pandas as pd
import time

# dictionary to map cities to their CSV files
CITY_DATA = {'chicago': 'chicago.csv',
             'new york city': 'new_york_city.csv',
             'washington': 'washington.csv'}

MONTH_DATA = {'january': 1,
              'february': 2,
              'march': 3,
              'april': 4,
              'may': 5,
              'june': 6}

DAY_DATA = {'monday': 0,
            'tuesday': 1,
            'wednesday': 2,
            'thursday': 3,
            'friday': 4,
            'saturday': 5,
            'sunday': 6}

def get_user_info(df):
    """
    Displays counts of each user type, counts of each gender (only available for NYC and Chicago),
    earliest, most recent, and most common year of birth (only available for NYC and Chicago).

    Args:
        (DataFrame) df - Pandas DataFrame containing city data

    Returns:
        None
    """
    print('\nCalculating User Info...\n')
    start_time = time.time()

    # get counts of each user type
    user_types = df['User Type'].value_counts()
    print('Counts of Each User Type:\n', user_types)

    # get counts of each gender (only available for NYC and Chicago)
    if 'Gender' in df.columns:
        gender_counts = df['Gender'].value_counts()
        print('\nCounts of Each Gender:\n', gender_counts)

    # get earliest, most recent, and most common year of birth (only available for NYC and Chicago)
    if 'Birth Year' in df.columns:
        birth_year_stats = df['Birth Year'].describe()
        print('\nEarliest, Most Recent, and Most Common Year of Birth:\n', birth_year_stats[['min', 'max', 'mean']])

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def display_data(df):
    """
    Asks user if they want to see 5 rows of individual trip data, and continues showing
    additional 5 rows each time the user inputs 'yes'.

    Args:
        (DataFrame) df - Pandas DataFrame containing city data

    Returns:
        None
    """
    view_data = input('\nWould you like to view 5 rows of individual trip data? Enter yes or no\n')
    start_loc = 0
    while view_data.lower() == 'yes':
        print(df.iloc[start_loc:start_loc+5])
        start_loc += 5
        view_data = input("Do you wish to continue?: ").lower()


def main():
    while True:
        # get user inputs for city, month, and day
        city = input('Enter city name (Chicago, New York City, or Washington): ').lower()
        while city not in CITY_DATA:
            city = input('Invalid city name. Please enter Chicago, New York City, or Washington: ').lower()

        month = input('Enter month (January, February, March, April, May, June) or type "all" to apply no month filter: ').lower()
        while month not in MONTH_DATA and month != 'all':
            month = input('Invalid month name. Please enter a valid month (January, February, March, April, May, June) or type "all" to apply no month filter: ').lower()

        day = input('Enter day of week (Monday, Tuesday, Wednesday, Thursday, Friday, Saturday
