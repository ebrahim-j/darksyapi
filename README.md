# Darksy API
Script to gather hourly data from darksky api and appended to a csv, provided a few command line arguments:
- Latitude and Longitude
- Time
- Filename

After acquiring an [API Key](https://darksky.net/dev/docs) and changing it's value on [this line](https://github.com/ebrahim-j/darksyapi/blob/73ce58cf40eff5f1bd4542da7da722c1ff3256be/main.py#L22), run the script on your terminal like this:

`python main.py latitude,longitude period_as_unix_timestamp mycsvfilename`
