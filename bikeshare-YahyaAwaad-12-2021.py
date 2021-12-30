import pandas as pd
import numpy as np
import time

CITY_DATA = { 'chicago': 'chicago.csv',
              'new york city': 'new_york_city.csv',
              'washington': 'washington.csv' }
all_months = ['January', 'February','March', 'April', 'May', 'June']
all_days = {'sat':'Saturday', 'sun': 'Sunday', 'mon': 'Monday', 'tue': 'Tuesday', 'wed': 'Wednesday', 'thu': 'Thursday', 'fri': 'Friday'}


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
    user_city = ''
    while user_city not in CITY_DATA:
        user_city = input("***Please select one of the available cities: \"Chicago\", \"New York City\", or \"Washington\": ").lower()
        if user_city in CITY_DATA:
            req_city = CITY_DATA[user_city]
            print('You chose the city of {} loading the {} file'.format(user_city.title(), req_city))
        else:
            print("Please enter a valid city name!.")
        

    # get user input for month (all, january, february, ... , june)
    user_month = input("***Please enter a month number to filter your query (from [1 - 6] for months from [Jan - June]), \n(If you don't want to use a month filter just press Enter without adding a value):").lower()
    if user_month:
        if user_month in list(map(str, range(1,len(all_months)+1))):
            req_month = all_months[int(user_month)-1]
            print("You selected to have your inshights filtered by {}".format(req_month))
        else:
            req_month = None
            print('Not a valid month number (between [1-6]), NO (MONTH) FILTER will be applied!')
            print("You selected {} to filter by Months".format(req_month))
    else:
        req_month = None   
        print("You selected {} to filter days".format(req_month))
        print('You selected NO MONTH FILTER to be applied')

    # get user input for day of week (all, monday, tuesday, ... sunday)
    user_day = input("***Please enter a 3-letter day name to filter your query on (e.g.: sat, sun, ...), \n(If you don't want to use a day filter just press Enter without adding a value):").lower()
    if user_day:
        if user_day in all_days:
            req_day = all_days[user_day]
            print("You selected to have your inshights filtered by {}".format(req_day))

        else:
            req_day = None
            print('Not a valid day short name (sat, sun, ...), NO (DAY) FILTER will be applied!')
            print("You selected {} to filter days".format(req_day))
    else:
        req_day = None
        print("You selected {} to filter days".format(req_day))
        print('You selected NO DAY FILTER to be applied')


    print('-'*40)
    
    return req_city, req_month, req_day



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
    df = pd.read_csv(city)
    #Convert the 'Start Time' column to a datetime form to be able to further split its details
    df['Start Time'] = pd.to_datetime(df['Start Time'])
    #Extracting the required attributes (as new cloumns) to be able to give the required detailed insights
    #Extracting the Hours
    df['Hour'] = df['Start Time'].dt.hour
    #Extracting the Days
    df['Day_name'] = df['Start Time'].dt.day_name()
    #Extracting the Months
    df['Month'] = df['Start Time'].dt.month_name()

    if month:
        df = df.loc[df['Month'] == month]

    if day:
        df = df.loc[df['Day_name'] == day]

    return df



def time_stats(df, month, day):
    """Displays statistics on the most frequent times of travel."""

    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()

    # display the most common month if NOT filtered by
    if not month:
        common_month = df['Month'].mode()[0]
        print("The Most Common Month is: {}".format(common_month))
    else:
        print("You have filtered your query to the month of {}".format(month))

    # display the most common day of week if NOT filtered by
    if not day:
        common_day = df['Day_name'].mode()[0]
	print("The Most Common Month is: {}".format(common_day))
    else:
        print("You have filtered your query to the day of {}".format(day))


    # display the most common start hour
    start_hour = df['Hour'].mode()[0]
    print('The Most Common Start Hour is {}'.format(start_hour))


    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)



def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    # display most commonly used start station
    s_dist = df['Start Station'].mode()[0]
    print('The Most Commonly Used Start Station is {}'.format(s_dist))

    # display most commonly used end station
    e_dist = df['End Station'].mode()[0]
    print('The Most Commonly Used End Station is {}'.format(e_dist))
	

    # display Most Common Trip i.e. most frequent combination of start station and end station trip
    mct = df.groupby(['Start Station','End Station']).size().idxmax()
    print('Most Common Trip is FROM- {} -TO- {}'.format(list(mct)[0],list(mct)[1]))


    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)



def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    # display total travel time
    ttt = df['Trip Duration'].sum()/60
    print("Total Trips Time over the selected period(s) is {} minute(s)".format(round(ttt, 2)))

    # display mean travel time
    mtt = df['Trip Duration'].mean()/60
    print("Avarage Trips Time over the selected period(s) is {} minute(s)".format(round(mtt, 2)))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)



def user_stats(df, city):
    """Displays statistics on bikeshare users."""

    print('\nCalculating User Stats...\n')
    start_time = time.time()

    # Display counts of user types
    ut = df['User Type'].value_counts()
    unique_types = ut.count()
    for i in range(unique_types):
        print('There are {} users of type {}'.format(ut[i], ut.index[i]))

    if city != 'washington.csv':
        # Display counts of gender
        g_count = df['Gender'].value_counts()
        print('The {} users are {}'.format(g_count.index[0], g_count[0]))
        print('The {} users are {}'.format(g_count.index[1], g_count[1]))

        # Display earliest, most recent, and most common year of birth
        elder_user = df['Birth Year'].min()
        younger_users = df['Birth Year'].max()
        most_users = df['Birth Year'].mode()
        print('The OLDEST users were born on {}'.format(int(elder_user)))
        print('The YOUNGEST users were born on {}'.format(int(younger_users)))
        print('Most commone Age group of users were born on {}'.format(int(most_users)))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)

def disp_df(df):
    i = 0
    while True:
        print(df.iloc[i:i+5, : ])
        more_5 = input('Would you like to view the next 5 rows?([y], no)').lower()
        if more_5 == 'no':
            break
        else:
            i += 5
            continue

def main():
    while True:
        city, month, day = get_filters()
        df = load_data(city, month, day)
        print('Your Query Parameters are:\nCity: {}\nFilter By Month = {}\nFilter By Day = {}'.format(city.split('.')[0].title(), month, day))
        print(df)

        time_stats(df, month, day)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df, city)
	disp_df(df)

        restart = input('\nWould you like to restart? Enter yes or no.\n')
        if restart.lower() != 'yes':
            break


if __name__ == "__main__":
	main()
