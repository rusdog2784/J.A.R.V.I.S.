from weather import Weather, Unit

weather = Weather(unit=Unit.FAHRENHEIT)

location = weather.lookup_by_location("hoboken")
city = location.location.city
state =  location.location.region

forecasts = location.forecast
print(forecasts[0].text)
print(forecasts[0].date)
print(forecasts[0].high)
print(forecasts[0].low)
