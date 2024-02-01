# FindMy Location Logger

## Introduction
By default, Find My doesn't include a location history feature for AirTags. And even if it did, it would probably have a limited amount of time to track an AirTag. <br>
This python script runs on a jailbroken iphone, and essentially reads the cache files from the Find My app constantly and logs it into a CSV file. Of course since CSV files aren't that useful for location mapping, included is a tool that will convert the CSV file to Google Maps/Google Earth compitable KML files.
 ## Installation
- Download this repo (via git or downloading the zip file from github and extracting)
- Jailbreak your iphone
- install Sileo 
- install NewTerm (terminal emulator) using Sileo
- install python3 using Sileo
- Install an ssh server using Sileo
- install (on your host PC) WinSCP or similar SCP client program
- copy over the find-my-thing directory into a directory easily accessible by NewTerm using the SCP client. Keep in mind that most default ssh creds on jailbroken iphones are the user `mobile` and the password `alpine`
## Usage
- open NewTerm and cd into find-my-thing directory 
- run `python3 main.py`
- let NewTerm run this process in thhe background, open the Find My app
- keep the Find My app open as long as you want to log the AirTag locations
- Whenever you want to extract the location history data, use SCP to extract the files in the find-my-thing/log/ directory.
- use the python script findmy2kml.py on your host machine to convert them into KML. the syntax is `python3 findmy2kml.py (csv file path)`
- import your KML files into google maps or google earth.
- (Optional) change the Auto Lock setting in your iphone to "Never" and keep your Find My app open 24/7
