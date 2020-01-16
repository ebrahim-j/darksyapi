import csv
import json
import sys
import urllib.request


def main():
    # ensure the correct command is input
    if (len(sys.argv) != 4):
        print('Kindly input the command correctly like so:\npython main.py latitude,longitude period_as_unix_timestamp mycsvfile')
        return

    lat_long = validate_lat_long(sys.argv[1])
    period = validate_period(sys.argv[2])

    # Invalid format of one or more arguments
    if not lat_long or not period:
        print('Kindly ensure all command line arguments are valid')
        return
    
    # Replace this with your actual darksky API key
    api_key = "Enter-Api-Key_Here"

    # The request to darksy api using python's inbuilt urllib.request library
    try:
        response = urllib.request.urlopen(
            'https://api.darksky.net/forecast/{}/{},{}?exclude=currently,flags,minutely,daily,alerts'.format(api_key, lat_long, period))
    except Exception as e:
        print("Error occurred in making the request: {}".format(e))
        return

    # Decode the bytes response to utf-8
    response_str = response.read().decode('utf-8')

    # Convert the json to a python dictionary
    data = json.loads(response_str)

    try:
        hourly_points = data['hourly']['data']
    except KeyError:
        print("Could not find any data for this request")
        return

    write_to_csv(hourly_points)

def write_to_csv(hourly_points):
    '''
    This function writes each data point to the specified csv
    '''

    filename = make_filename(sys.argv[3])

    with open(filename, mode='w') as csv_file:
        # write to a CSV file using a writer object
        csv_writer = csv.writer(csv_file, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)

        # set the header row
        csv_writer.writerow(['time', 'temperature', 'apparentTemperature', 'dewPoint', 'humidity', 'windSpeed', 'windBearing', 'cloudCover', 'uvIndex'])
        for point in hourly_points:
            # write individual data points to the csv as a row
            csv_writer.writerow([point['time'], point['temperature'], point['apparentTemperature'], point['dewPoint'],\
                point['humidity'], point['windSpeed'], point['windBearing'], point['cloudCover'], point['uvIndex']])

def validate_lat_long(lat_long):
    ''' 
    Ensure the latitude and longitude are valid
    '''

    l_l = lat_long.split(",")
    try:
        latitude = float(l_l[0])
        longitude = float(l_l[1]) 
        if (-90 <= latitude <= 90) and (-180 <= longitude <= 180):
            return lat_long
        return None
    except ValueError:
        return None

def validate_period(period):
    '''
    Ensure the period is an integer (the correct format for all unix timestamps)
    '''
    try:
        int(period)
        return period
    except ValueError:
        return None

def make_filename(filename):
    '''
    Ensure the file format is correct
    '''
    filename = filename.split(".")[0]
    return filename + ".csv"

main()
