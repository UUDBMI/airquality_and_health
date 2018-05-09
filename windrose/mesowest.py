import json
from urllib.request import urlopen
import numpy as np


def query(stationID, 
                   start_time, 
                   end_time, 
                   variables=None):
                   
                   
    if variables == None:
        variables = ["altimeter",
                     "pressure",
                     "sea_level_pressure",
                     "wind_direction",
                     "wind_speed",
                     "air_temp",
                     "relative_humidity",
                     "dew_point_temperature",
                     "wind_gust"]
    token = 'demotoken'
    
    # Convert the start and end time to the string format requried by the API
    start = start_time.strftime("%Y%m%d%H%M")
    end = end_time.strftime("%Y%m%d%H%M")
    tz = 'utc'  # Timezone is hard coded for now. Could allow local time later.

    # Build the API request URL
    URL = 'http://api.mesowest.net/v2/stations/timeseries?&token=' + token \
        + '&stid=' + stationID \
        + '&start=' + start \
        + '&end=' + end \
        + '&vars=' + ",".join(variables)+";" \
        + '&obtimezone=' + tz \
        + '&output=json'

    # Open URL and read JSON content. Convert JSON string to some python
    # readable format.
    f = urlopen(URL)
    data = f.read()
    data = json.loads(data)
    return data, URL


def get_mesowest_ts(data):
    """
    Get MesoWest Time Series data:
    Makes a time series query from the MesoWest API for a single station.

    Input:
        stationID  : string of the station ID
        start_time : datetime object of the start time in UTC
        end_time   : datetime object of the end time in UTC
        variables  : a string of variables available through the MesoWest API
                     see https://synopticlabs.org/api/mesonet/variables/ for
                     a list of variables.
    Output:
        A dictionary of the data.
    """

    # Hey! You can get your own token! https://synopticlabs.org/api/guides/?getstarted
    # Create a new dictionary to store the data in.
    return_this = {}

    # Get basic station information
    return_this['URL'] = URL
    return_this['NAME'] = str(data['STATION'][0]['NAME'])
    return_this['STID'] = str(data['STATION'][0]['STID'])
    return_this['LAT'] = float(data['STATION'][0]['LATITUDE'])
    return_this['LON'] = float(data['STATION'][0]['LONGITUDE'])
    return_this['ELEVATION'] = float(data['STATION'][0]['ELEVATION'])
                               # Note: Elevation is in feet, NOT METERS!

    # Dynamically create keys in the dictionary for each requested variable
    for v in data['STATION'][0]['SENSOR_VARIABLES'].keys():
        if v == 'date_time':
            # Dates: Convert the strings to a python datetime object.
            dates = data["STATION"][0]["OBSERVATIONS"]["date_time"]
            DATES = [datetime.strptime(x, '%Y-%m-%dT%H:%M:%SZ') for x in dates]
            return_this['DATETIME'] = np.array(DATES)
        else:
            # v represents all the variables, but each variable may have
            # more than one set.
            # For now, just return the first set.
            key_name = str(v)
            set_num = 0

            grab_this_set = str(list(data['STATION'][0]['SENSOR_VARIABLES']\
                                [key_name].keys())[set_num]) # This could be problematic. No guarantee of order

            # Always grab the first set (either _1 or _1d)
            # ! Should make exceptions to this rule for certain stations and certain
            # ! variables (a project for another day :p).
            if grab_this_set[-1] != '1' and grab_this_set[-1] != 'd':
                grab_this_set = grab_this_set[0:-1]+'1'
            if grab_this_set[-1] == 'd':
                grab_this_set = grab_this_set[0:-2]+'1d'

            variable_data = np.array(data['STATION'][0]['OBSERVATIONS']\
                                    [grab_this_set], dtype=np.float)
            return_this[key_name] = variable_data

    return return_this
