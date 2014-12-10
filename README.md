## What is this?
This program will search through available courses at University of Ontario Institute of Technology, and store information about them in an SQLite database.

The program uses three libraries:
+ urllib2 is used to load the web pages at http://uoit.ca/mycampus/avail_courses.html
+ BeautifulSoup4 is used to parse the webpage and help extract information.
+ sqlite3 is used to create an SQLite database with all the extracted information.
+ My pain and sweat in dealing with awful things like information separated by dashes containing dashes.

## What needs to be implemented?
There are some data which aren't get extracted by the program. A list of missing things is as follows:
+ Pre-requisites for certain courses - this could be useful for schedule-making things.
+ Compatible CRNs - which labs can be taken with which lectures, etc
+ Use of a 'Locations' table so information about particular locations can be added on.

## UOIT/DC Web & App Club
If you're in the UOIT/DC Web & App Club, you're encouraged to take a look through the code, and contribute features.
A database generated using this program is available in the club's Google Drive folder.
