

import pandas as pd
import simplekml
from datetime import datetime, timedelta
from sys import argv

def format_timestamp(ts, utc_offset):
    # Assuming the timestamp is in milliseconds since the Unix epoch
    utc_time = datetime.utcfromtimestamp(int(ts) / 1000) + timedelta(hours=utc_offset)
    return utc_time.strftime('%Y-%m-%d %H:%M:%S')

# Read the CSV file
csv_file = argv[1]  # Change this to the path of your CSV file
df = pd.read_csv(csv_file)

# Sort the DataFrame by timestamp
df.sort_values(by='location|timeStamp', inplace=True)

# Get the save filename and UTC offset hours from user input
kml_filename = input("Enter a save filename for the KML (e.g., my_location.kml): ").strip()
if not kml_filename.endswith('.kml'):
    kml_filename += '.kml'

utc_offset = input("Enter UTC offset hours (default 0): ")
if utc_offset == '':
    utc_offset = 0
else:
    try:
        utc_offset = int(utc_offset)
    except ValueError:
        print("Invalid input for UTC offset. Using default +0 hours.")
        utc_offset = 0

# Create a KML object
kml = simplekml.Kml()

# Iterate through the DataFrame and add points to the KML
for index, row in df.iterrows():
    # Extract necessary information
    lat, lon = row['location|latitude'], row['location|longitude']
    raw_timestamp = row['location|timeStamp']
    formatted_timestamp = format_timestamp(raw_timestamp, utc_offset)
    name = f"{row['deviceDisplayName']} ({formatted_timestamp})" if pd.notna(row['deviceDisplayName']) else f"Unknown Device ({formatted_timestamp})"
    description = f"ID: {row['identifier']}\nBattery Level: {row['batteryLevel']}\nTimestamp: {formatted_timestamp}"

    # Add a point to the KML
    kml.newpoint(name=name, coords=[(lon, lat)], description=description)

# Save the KML file
kml.save(kml_filename)

print(f"KML file created: {kml_filename}")
