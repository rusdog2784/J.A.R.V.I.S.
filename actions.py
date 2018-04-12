from weather import Weather, Unit

class Actions:
    location = ""

    def __init__(self, location):
        print("Initializing Actions class...")
        self.location = location

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

    def getNews(self, story):
        return

    def getTime(self):
        return

    def getCalendar(self, action):
        return

    def openFolder(self, location):
        return

    def goToWebsite(self, location):
        return

