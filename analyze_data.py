import os
import pandas as pd
import folium


def get_calls(police_data):
  """
  reads in the police data .csv's, filter's for missing shift and latitude and longitude
  gets the top three call types for each shift for each year
  :param police_data: list of paths to police call data
  :return: type_df: dataframe of the filtered data
  """
  # Initialize dataframe
  count_df = pd.DataFrame(columns=['Tencode', 'Shift', 'Latitude', 'Longitude', 'Date', 'Year'])
  # loop through the police_data paths and read in the information
  for file_path in police_data:
    # read csv into dataframe
    calls_df = pd.read_csv(file_path, dtype={'Latitude': 'float64',  'Longitude': 'float64'}
                           , na_values='', keep_default_na=False).dropna(
                            subset=['Latitude', 'Longitude'])
    # Isolate variables Tencode, shift, Latitude, Longitude
    calls_df = calls_df.iloc[:, [3, 12, 15, 16, 18]]
    # Change_call_received to year update dataframe
    calls_df['Year'] = pd.to_datetime(calls_df['Call_Received']).dt.year
    calls_df['Call_Received'] = pd.to_datetime(calls_df['Call_Received']).dt.date
    calls_df = calls_df.rename(columns={'Call_Received': 'Date'})
    # Remove rows with missing Shift, Latitude, and Longitude
    calls_df.dropna(subset=['Shift', 'Latitude', 'Longitude'], inplace=True)
    # add calls_df to count_df
    count_df = pd.concat([count_df, calls_df], ignore_index=True)
    # group by year and date and get sizes, find max and min for each year
  counts = count_df.groupby(['Year', 'Date']).size()
  most_calls_date = counts.groupby('Year').idxmax()
  least_calls_date = counts.groupby('Year').idxmin()

  return count_df, most_calls_date, least_calls_date


def create_plots(call_info, most_calls_date, least_calls_date):
  '''
  This plots the call dataframes with call info, dates with most calls, and dates with least calls,
  and plots the dates with the least number of calls.
  :param call_info: dataframe with call info
  :param most_calls_date: dataframe with dates with the most calls
  :param least_calls_date: dataframe with dates with the most calls
  '''
  # Specify the city location (latitude and longitude)
  city_location = [36.165, -86.770]  # Nashville coordinates



  # Define colors
  colors = {'A': 'blue', 'B': 'orange', 'C': 'red'}
  # Iterate over most and least call days
  for calls_date in [most_calls_date, least_calls_date]:
    label = 'most_calls_date' if calls_date is most_calls_date else 'least_calls_date'
    # Iterate over year and shift to create map
    for year in call_info['Year'].unique():
      # Create a folium map centered at the city location
      city_map = folium.Map(location=city_location, zoom_start=11)
      date = calls_date.loc[year][1]
      date_data = call_info[call_info['Date'] == date]
      shift_count = []
      for shift in date_data.sort_values('Shift')['Shift'].unique():
        if len(shift_count) == 0 and shift == 'B':
          shift_count.append(0)
        shift_data = date_data[date_data['Shift'] == shift]
        shift_count.append(len(shift_data))
        for index, row in shift_data.iterrows():
            lat = row['Latitude']
            long = row['Longitude']
            folium.Marker(location=[lat, long],
                          icon=folium.Icon(color=colors[shift])).add_to(city_map)
      total_calls = len(date_data)
      # Create a legend
      if len(shift_count) != 3:
        for i in range(len(shift_count),3):
          shift_count.append(0)
      legend_html = '''
      <div style="position: fixed; 
      top: 10px; right: 10px; width: 225px; height: 175px; 
      border: 2px solid grey; z-index: 9999; font-size: 18px; background-color: white; padding: 5px;">
      <strong style="font-size:25px;">Legend</strong> <br>
      Date: {date} <br>
      Total Calls: {total_calls} <br>
      Day Shift Calls: {shift_count[0]}<i style="background:#3186cc; width: 10px; height: 10px; border-radius: 50%; display: inline-block; margin-top: 8px; float: right;"></i><br>
      Evening Shift Calls: {shift_count[1]} <i style="background: orange; width: 10px; height: 10px; border-radius: 50%; display: inline-block;margin-top: 8px;float:  right;"></i><br>
      Night Shift Calls: {shift_count[2]} <i style="background: red; width: 10px; height: 10px; border-radius: 50%; display: inline-block;margin-top: 8px; float: right;"></i><br>
      </div>
         '''.format(date=date, total_calls=total_calls, shift_count=shift_count)

      # Add the legend to the map
      city_map.get_root().html.add_child(folium.Element(legend_html))
      city_map.save(str(year) + '_' + label + '.html')



if __name__ == '__main__':
    """
    This script combines clean data for police calls and housing from .csv files. 
    The data is combined based on sectors and time period and then graphed.
    """


    # Create path variables to files
    #police_data = [os.getcwd() + '/data/calls_2019.csv']
    #police_data.append(os.getcwd() + '/data/calls_2020.csv')
    #police_data.append(os.getcwd() + '/data/calls_2021.csv')
    police_data = [os.getcwd() + '/data/calls_2022.csv']
    police_data.append(os.getcwd() + '/data/calls_2023.csv')
    police_data.append(os.getcwd() + '/data/calls_2024.csv')
    housing_path = os.getcwd() + '/data/housing.csv'

    # Initialize neighborhood sector dictionary
    ind_sectors = ['M', 'S', 'C', 'N', 'W', 'MT', 'E','H']
    nh_sectors = dict([('Antioch', 'M'), ('Berry Hill', 'S'), ('Donelson', 'H, S'),
                       ('East Nashville', 'C'), ('Germantown', 'C, N'), ('Hillwood', 'W'),
                       ('Inglewood', 'E'), ('Lockeland Springs', 'E'),
                       ('Sylvan Park', 'MT'), ('12 South', 'C, MH'), ('Belle Meade', 'MT'),
                       ('Downtown Nashville', 'C'), ('East Nashville', 'E, N'),
                       ('Hermitage', 'H'), ('Madison', 'M'), ('North Nashville', 'N'),
                       ('Oak Hill', 'H, W'), ('Old East Nashville', 'E'),
                       ('Old Hickory', 'M'), ('South Nashville', 'S'), ('West Nashville', 'W')])
    # Determine cutoff date
    # cutoff = (datetime.now() - timedelta(days=5 * 365)).year
    # average housing data by sectors and filter by date
    #housing_averages = get_housing(housing_path, nh_sectors, ind_sectors, cutoff)

    # get call info by sectors
    call_info, most_calls_date, least_calls_date = get_calls(police_data)
    # create plots showing the data.
    create_plots(call_info, most_calls_date, least_calls_date)