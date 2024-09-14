import time
import pandas as pd
import numpy as np

CITY_DATA = { 'chicago': 'chicago.csv',
              'new york city': 'new_york_city.csv',
              'washington': 'washington.csv' }

def get_filters():
    """
    Asks user to specify a city, month, and day to analyze.

    Returns:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    """
    print('Hello! Let\'s explore some US bikeshare data!')
    # get user input for city (chicago, new york city, washington). HINT: Use a while loop to handle invalid inputs
    cities = ['chicago', 'new york city', 'washington']
    city = input('choose the city in which you would like to ride a bike: chicago, new york city or washington? ').lower()
    while city not in cities:
        print('invalid input')
        city = input('please, make sure to write one of these cities: chicago, new york city or washington. ').lower()
    # get user input for month (all, january, february, ... , june)
    months = ['january', 'february', 'march', 'april', 'may', 'june', 'all']
    month = input('choose the month: january, february, march, april, may, june or all? ').lower()
    while month not in months:
        print('invalid input')
        month = input('please, if you chose a month make sure to write one of the available months, which are: january, february, march, april, may or june. and make sure to write it correctly.').lower()
  
    # get user input for day of week (all, monday, tuesday, ... sunday)
    days = ['saturday', 'sunday', 'monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'all']
    day = input('choose the day: saturday, sunday, monday, tuesday, wednesday, thursday, friday or all? ').lower()
    while day not in days:
        print('invalid input')
        day = input('please, if you chose a day make sure to write it correctly: saturday, sunday, monday, tuesday, wednesday, thursday or friday? ').lower()

    print('-'*40)
    return city, month, day


def load_data(city, month, day):
    """
    Loads data for the specified city and filters by month and day if applicable.

    Args:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    Returns:
        df - Pandas DataFrame containing city data filtered by month and day
    """
# load data file into a dataframe
    df = pd.read_csv(CITY_DATA[city])

    # convert the Start Time column to datetime
    df['Start Time'] = pd.to_datetime(df['Start Time'])
    df['End Time'] = pd.to_datetime(df['End Time'])
    # extract month and day of week and star hour from Start Time to create new columns
    df['month'] = df['Start Time'].dt.month
    df['day_of_week'] = df['Start Time'].dt.weekday_name
    df['hour'] = df['Start Time'].dt.hour
    # convert the END Time column to datetime( to use it later in trip duration
    df['trip duration'] = df['End Time'] - df['Start Time']
    # filter by month if applicable
    if month != 'all':
        # use the index of the months list to get the corresponding int
        months = ['january', 'february', 'march', 'april', 'may', 'june']
        month = months.index(month) + 1

        # filter by month to create the new dataframe
        df = df[df['month'] == month]

    # filter by day of week if applicable
    if day != 'all':
        # filter by day of week to create the new dataframe
        df = df[df['day_of_week'] == day.title()]
    
    return df 


def time_stats(df):
    """Displays statistics on the most frequent times of travel."""

    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()

    # display the most common month
    most_common_month = df['month'].mode()[0]
    print('most common month is: ', most_common_month)
    # display the most common day of week
    most_common_day = df['day_of_week'].mode()[0]
    print('most common day is: ', most_common_day)
    # display the most common start hour
    most_common_start_hour = df['hour'].mode()[0]
    print('most common start hour is: ', most_common_start_hour)

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    # display most commonly used start station
    most_common_start_station = df['Start Station'].mode()[0]
    print('most common start station: ', most_common_start_station)
    # display most commonly used end station
    most_common_end_station = df['End Station'].mode()[0]
    print('most common end station is: ', most_common_end_station)

    # display most frequent combination of start station and end station trip
    print('most common trip: ', (df['Start Station'] + ' to ' + df['End Station']).mode()[0])

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    # display total travel time
    print('total travel time of our trips: ', df['trip duration'].sum())

    # display mean travel time
    print('mean travel time of our trips: ', df['trip duration'].mean())

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def user_stats(df, city):
    """Displays statistics on bikeshare users."""

    print('\nCalculating User Stats...\n')
    start_time = time.time()

    # Display counts of user types
    print(df['User Type'].value_counts())
    
    # Display counts of gender
    if city != 'washington':
        print(df['Gender'].value_counts())
    
    # Display earliest, most recent, and most common year of birth
    if city != 'washington':
        print('most common year of birth is: ', df['Birth Year'].mode()[0])
        print('most recent year of birth is: ', df['Birth Year'].max())
        print('earliest year of birth is: ', df['Birth Year'].min())
    
    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


    
def display_row_data(df):
    
    question = input('would you like to display sample of complete data? (yes or no) ').lower()
    
    while question == 'yes':
        print(df.sample(5))
        question = input('would you like to display more of the complete data? ').lower()
        
        
def main():
    while True:
        city, month, day = get_filters()
        df = load_data(city, month, day)

        time_stats(df)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df, city)
        display_row_data(df)

        restart = input('\nWould you like to restart? Enter yes or no.\n')
        if restart.lower() != 'yes':
            break


if __name__ == "__main__":
	main()
