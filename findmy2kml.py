import pandas as pd
import simplekml
from datetime import datetime, timedelta
from sys import argv
from geopy.distance import geodesic

def format_timestamp(ts, utc_offset):
    # Assuming the timestamp is in milliseconds since the Unix epoch
    utc_time = datetime.utcfromtimestamp(int(ts) / 1000) + timedelta(hours=utc_offset)
    return utc_time.strftime('%Y-%m-%d %H:%M:%S')

def parse_timestamp(ts):
    # Convert timestamp from milliseconds since Unix epoch to datetime
    return datetime.utcfromtimestamp(int(ts) / 1000)

def are_too_close_and_recent(coord1, coord2, time1, time2, min_distance, min_time_diff):
    """Check if two coordinates are within the min_distance and time difference of each other."""
    distance = geodesic(coord1, coord2).kilometers
    time_diff = abs(time1 - time2)
    return distance < min_distance and time_diff < min_time_diff

def filter_placemarks(df, min_distance, min_time_diff, enable_filtering=True):
    """Filter placemarks that are too close and too recent to each other if enable_filtering is True."""
    filtered_data = []
    if not enable_filtering:
        return df
    for _, row in df.iterrows():
        coord = (row['location|latitude'], row['location|longitude'])
        time = parse_timestamp(row['location|timeStamp'])
        if all(not are_too_close_and_recent(coord, (r['location|latitude'], r['location|longitude']), time, parse_timestamp(r['location|timeStamp']), min_distance, min_time_diff) for r in filtered_data):
            filtered_data.append(row)
    return pd.DataFrame(filtered_data)

# Read the CSV file
csv_file = argv[1]  # Change this to the path of your CSV file
df = pd.read_csv(csv_file)

# Sort the DataFrame by timestamp
df.sort_values(by='location|timeStamp', inplace=True)

min_distance = 10  # Modify as needed
min_time_diff = timedelta(minutes=30)  # 30 minutes

# Prompt user to enable filtering
enable_filtering = input("Do you want to filter out potentially useless placemarks? (yes/no): ").strip().lower()
if enable_filtering == 'yes':
    enable_filtering = True
elif enable_filtering == 'no':
    enable_filtering = False
else:
    print("Invalid input. Defaulting to filtering enabled.")
    enable_filtering = True

# Filter the DataFrame
filtered_df = filter_placemarks(df, min_distance, min_time_diff, enable_filtering)

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

# Iterate through the filtered DataFrame and add points to the KML
for _, row in filtered_df.iterrows():
    # Extract necessary information
    lat, lon = row['location|latitude'], row['location|longitude']
    raw_timestamp = row['location|timeStamp']
    formatted_timestamp = format_timestamp(raw_timestamp, utc_offset)
    name = row['name']
    description = f"ID: {row['identifier']}\nBattery Level: {row['batteryLevel']}\nTimestamp: {formatted_timestamp}"

    # Add a point to the KML
    kml.newpoint(name=name, coords=[(lon, lat)], description=description)

# Save the KML file
kml.save(kml_filename)

print(f"KML file created: {kml_filename}")
