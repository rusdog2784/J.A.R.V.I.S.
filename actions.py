from __future__ import print_function
import datetime
import json
# weather-api imports
from weather import Weather, Unit
# Google Calendar API imports
from apiclient.discovery import build
from httplib2 import Http
from oauth2client import file, client, tools
# Open websites imports
import webbrowser
# Open applications imports
import os
# Play Marvel movie imports
import random
# Spotify API imports
import spotipy
import spotipy.util as util
# News API imports
from newsapi import NewsApiClient
import sys
# Magic Mirror imports
import requests

class Actions(object):
    google_scope = 'https://www.googleapis.com/auth/calendar'
    news_api_key = '603fdd9223614b60826a80b8ad29afa8'
    spotify_username = 'scott.tkdmaster@mac.com'
    spotify_scope = 'user-library-read user-read-private streaming'
    websites = {}
    applications = []
    movieNames = []
    folders = {}
    
    # Initializing function that is called at the start of JARVIS.
    def __init__(self, location="hoboken"):
        print("Initializing Actions class...")
        # Creating system applications list and saving it as "applications.txt"
        os.system("ls /Applications > /Users/scott/Desktop/Programming/Python/Projects/J.A.R.V.I.S./applications.txt")
        # Setting location for weather services
        self.location = location
        # Google Calendar API setup
        store = file.Storage('credentials.json')
        creds = store.get()
        if not creds or creds.invalid:
            flow = client.flow_from_clientsecrets('client_secret.json', self.google_scope)
            creds = tools.run_flow(flow, store)
        self.service = build('calendar', 'v3', http=creds.authorize(Http()))
        # Initiating website variable from the "websites.json" file which contains a dictionary of websites
        with open("websites.json", 'r') as f:
            self.websites = json.load(f)
        # Initiating applications variable from the "applications.txt" file which contains all system applications
        with open("applications.txt", "r") as f:
            self.applications = f.readlines()
        self.applications = [x.strip() for x in self.applications]
        # Initiating marvel movie variable, marvelMovies, from the "marvel_movies.txt" file.
        with open('marvel_movies.txt', 'r') as f:
                self.movieNames = f.readlines()
        # Spotify Authentication
        self.spotify_token = util.prompt_for_user_token(self.spotify_username, self.spotify_scope)
        # Initiating folders variable from the "folders.json" file which contains a dictionary of folder locations
        with open("folders.json", 'r') as f:
            self.folders = json.load(f)

    # Function to gather weather data for the specified location
    # Returns object (city, condition, high, low)
    def getWeather(self, date):
        weather = Weather(unit=Unit.FAHRENHEIT)
        city = ""
        condition = ""
        high = ""
        low = ""

        location = weather.lookup_by_location(self.location)
        city = location.location.city

        forecasts = location.forecast
        if (date == None or date.lower() == "today"):
            condition = forecasts[0].text
            high = forecasts[0].high
            low = forecasts[0].low
            date = "today"
        elif (date.lower() == "tomorrow"):
            condition = forecasts[1].text
            high = forecasts[1].high
            low = forecasts[1].low

        data = {
            "city": city,
            "date": date,
            "condition": condition,
            "high": high,
            "low": low
        }
        return data

    # Function collects 10 articles from the following news sources:
    # bbc-news,the-verge,the-wall-street-journal,bloomberg,the-economist,wired
    # and returns the list of articles for JARVIS to speak. The object returned
    # is a list of dictionary objects called 'articles'. This object contains
    # the following meta-data: title of article, when the article was published,
    # where the article came from, the url of the article, etc. just to name a
    # few. 
    def getNews(self):
        # Creating News API object
        newsapi = NewsApiClient(api_key=self.news_api_key)
        top_headlines = newsapi.get_top_headlines(sources='bbc-news,the-verge,the-wall-street-journal,bloomberg,the-economist,wired')
        articles = top_headlines['articles']
        if len(articles) > 10:
            articles = articles[0:10]
        '''
        count = 1
        for article in articles:
            print(article['title'])
            print(article['url'])
            print(article['publishedAt'])
            print(article['source']['name'])
            print('-'*60)
            command = 'say "Number %s: %s writes %s"' % (str(count), article['source']['name'].encode('utf-8'), article['title'].encode('utf-8'))
            count += 1
            try:
                os.system(command)
            except KeyboardInterrupt:
                print("Interupted! How rude!")
            finally:
                sys.exit()
        '''
        return articles

    # Simple function to get the current date.
    def getDate(self):
        now = datetime.datetime.now()
        day = now.strftime("%A, %B %dth")
        return day

    # Simple function to get the current time.
    def getTime(self):
        now = datetime.datetime.now()
        if (now.minute == 0):
            time = now.strftime("%I %p")
        else:
            time = now.strftime("%I:%M %p")
        return time

    def getCalendar(self, action):
        return

    def openFolder(self, location):
        if len(self.folders) == 0:
            print("Error, something happened with loading folder locations. The object, folders, is empty.")
            return
        location.lower()
        if location in self.folders:
            command = '''open "%s"''' % (self.folders[location])
            os.system(command)
        else:
            print("Folder not logged or doesn't exist.")
        return "Opening " + location

    # Function to open the specified website in a web browser assuming it knows
    # what website the user is talking about.
    def goToWebsite(self, location):
        if len(self.websites) == 0:
            print("Error, something happened with loading website locations. The object, websites, is empty.")
            return
        location = location.lower()
        if location in self.websites:
            webbrowser.open_new_tab(self.websites[location])
        else:
            print("Folder not logged or doesn't exist.")
        return "Opening " + location

    # Function will play the specified Marvel movie from iTunes.
    def playMarvelMovie(self, title):
        if title == None or title == "":
            if len(self.movieNames) == 0:
                movieName = "Iron Man"
            else:
                movieName = self.movieNames[random.randint(0, len(self.movieNames - 1))]
        else:
            movieName = title
        osascript = '''
        on replace(input, x, y)
            set text item delimiters to x
            set ti to text items of input
            set text item delimiters to y
            ti as text
        end replace

        tell application "iTunes"
            --play track "" of playlist "Marvel Movies"
            set allTracks to get tracks of playlist "Marvel Movies"
            repeat with aTrack in allTracks
                set movieName to (get name of aTrack)
                set movieName to my replace(movieName, ":", "")
                if (movieName contains "%s") then
                    play aTrack
                end if
            end repeat
        end tell
        ''' % (movieName)
        command = "osascript -e '" + osascript + "'"
        os.system(command)
        return "Playing " + movieName + "."

    # Function opens an application specified assuming it is an application present
    # on the local machine and inside the Applications folder.
    def openApplication(self, application):
        if len(self.applications) == 0:
            print("Error, something happened with loading website locations. The object, applications, is empty.")
            return
        application = application + ".app"
        if application in self.applications:
            os.system("open -a '" + application + "'")
        else:
            return "Invalid Application Specified."
        return application + " opened."

    # Function quits out of the application specified assuming it is an application
    # present on the local machine and inside the Applications folder.
    def closeApplication(self, application):
        if len(self.applications) == 0:
            print("Error, something happened with loading website locations. The object, applications, is empty.")
            return
        application = application + ".app"
        if application in self.applications:
            command = """osascript -e 'quit app "%s"'""" % (application)
            os.system(command)
        else:
            return "Invalid Application Specified."
        return application + " opened." 

    # Function created a calendar event in my personal google calendar with a
    # specified title, start date, and end date. If end date is not specified,
    # then end becomes the start date plus 30 minutes by default. This function
    # returns a string, success, with the calendar html link.
    def createCalendarEvent(self, title, start, end):
        if self.service == None:
            print("Error, something happened with creating a calendar event. The object, service, has not been created.")
            return
        if end == None:
            end = start + datetime.timedelta(minutes = 30)
        eventData = {
            'summary': title,
            'description': "This event was created by Scott Russell's JARVIS AI.",
            'start': {
                'dateTime': start.isoformat(),
                'timeZone': 'America/New_York'
            },
            'end': {
                'dateTime': end.isoformat(),
                'timeZone': 'America/New_York'
            },
            'reminders': {
                'useDefault': True
            }
        }
        newEvent = self.service.events().insert(calendarId='primary', body=eventData).execute()
        success = 'Event created: %s' % (newEvent.get('htmlLink'))
        return success
    
    # Function takes in a search item as well as a type of search (artist, album,
    # track, or playlist) and proceeds to check that a spotify api token has been
    # made and is active. If the token is valid, a spotify object is created that
    # performs a search based on the search and type, returns the first item,
    # then, using applescript, plays the desired spotify uri.
    def playSpotify(self, search, searchType):
        if searchType.lower() == "track":
            search = search.replace("by", "")

        if self.spotify_token:
            sp = spotipy.Spotify(auth=self.spotify_token)    
            result = sp.search(q=search, type=searchType)
            if result:
                if result[searchType+'s']:
                    if result[searchType+'s']['items']:
                        item = result[searchType+'s']['items'][0]
                        print(item)
                        item_uri = item['uri']
                        print(item_uri)
                        osascript = '''
                        tell application "Spotify"
                            play track "%s"
                        end tell
                        ''' % (item_uri)
                        command = "osascript -e '" + osascript + "'"
                        os.system(command)
        else:
            print("Error, something happened with creating a spotify token. The object, token, has not been created.")
        returnString = "Playing %s" % (search)
        return returnString

    def playRandomSpotify(self):
        if self.spotify_token:
            sp = spotipy.Spotify(auth=self.spotify_token)
            results = sp.current_user_top_tracks()
            randomSong = random.choice(results['items'])
            randomURI = randomSong['uri']
            print(randomURI)
            osascript = '''
            tell application "Spotify"
                play track "%s"
            end tell
            ''' % (randomURI)
            command = "osascript -e '" + osascript + "'"
            os.system(command)