
import re, os
import pandas as pd


def read_file(file_path, sectors, cy):
  """
  reads in the .csv, filters and puts into a dataframe
  :param file_path: name of the input file
  :param sectors: list of sectors under consideration
  :param cy: current year specifier which determines if format has changed
  :return: filtered_df: dataframe of the filtered data
  """
  # Open the first .csv file, create dataframe, add data to dataframe
  last = 22 if cy else 19
  with open(file_path, 'r') as f:
    headers = f.readline().strip().split(',')[0:last]
    filtered_df = pd.DataFrame(columns=headers) # ignore last two datapoints,
    # rounded latitude and longitude that are often missing
    # loop through lines, find commas within quotation marks and delete them,
    # and eliminate lines where sector is incorrect or TenCode is missing
    # add to dataframe
    for line in f:
      pattern = r'(".*?")'
      quotes = re.findall(pattern, line)
      modified_line = re.sub(pattern, lambda match: match.group(0).replace(',', ''), line)
      temp = modified_line.strip().split(',')[0:last]
      if temp[3] is None or temp[13] not in sectors:
        continue
      filtered_df = pd.concat([filtered_df, pd.DataFrame([temp], columns=headers)]
                              , ignore_index=True)
    f.close()

    # remove extra columns from current year and rename column
    if cy:
      filtered_df = filtered_df.rename(columns={'Call Received': 'Call_Received'})
      filtered_df = filtered_df.drop(columns=[headers[14], headers[15], headers[16]])
    filtered_df['Call_Received'] = pd.to_datetime(filtered_df['Call_Received'], format='%m/%d/%Y %I:%M:%S %p')

    return filtered_df

if __name__ == '__main__':
    """
    This script pulls in data from the .csv files containing Nashville police calls for service.
    The data is filtered to contain TenCode and the sector of the call. Cleaned data is then output 
    to a csv file.
    """

    # Create path variables to files
    file_path_2018 = os.getcwd() + '/data/Metro_Nashville_Police_Department_Calls_for_Service_2018_8292891281301167783.csv'
    file_path_2019 = os.getcwd() + '/data/Metro_Nashville_Police_Department_Calls_for_Service_2019_1419525668394231252.csv'
    file_path_2020 = os.getcwd() + '/data/Metro_Nashville_Police_Department_Calls_for_Service_2020_-2961656542855534405.csv'
    file_path_2021 = os.getcwd() + '/data/Metro_Nashville_Police_Department_Calls_for_Service_2021_2317239082646722439.csv'
    file_path_2022 = os.getcwd() + '/data/Metro_Nashville_Police_Department_Calls_for_Service_2022_2401052795349394499.csv'
    file_path_2023 = os.getcwd() + '/data/Metro_Nashville_Police_Department_Calls_for_Service_2023_5456239620798107499.csv'
    file_path_2024 = os.getcwd() + '/data/Metro_Nashville_Police_Department_Calls_for_Service_view_5205088830608532215.csv'

    # Initialize needed sectors
    sectors = ['C', 'E', 'H', 'M', 'MT', 'N', 'S', 'W']

    calls_2018 = read_file(file_path_2018, sectors, False)
    calls_2018.to_csv(os.getcwd() + '/data/calls_2018.csv', index=False)
    calls_2019 = read_file(file_path_2019, sectors, False)
    calls_2019.to_csv(os.getcwd() + '/data/calls_2019.csv', index=False)
    calls_2020 = read_file(file_path_2020, sectors, False)
    calls_2020.to_csv(os.getcwd() + '/data/calls_2020.csv', index=False)
    calls_2021 = read_file(file_path_2021, sectors, False)
    calls_2021.to_csv(os.getcwd() + '/data/calls_2021.csv', index=False)
    calls_2022 = read_file(file_path_2022, sectors, False)
    calls_2022.to_csv(os.getcwd() + '/data/calls_2022.csv', index=False)
    calls_2023 = read_file(file_path_2023, sectors, False)
    calls_2023.to_csv(os.getcwd() + '/data/calls_2023.csv', index=False)
    calls_2024 = read_file(file_path_2024, sectors, True)
    calls_2024.to_csv(os.getcwd() + '/data/calls_2024.csv', index=False)
