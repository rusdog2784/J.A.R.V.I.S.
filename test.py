import datetime

now = datetime.datetime.now()

day = now.strftime("%A, %B %dth")
if (now.minute == 0):
    time = now.strftime("%I %p")
else:
    time = now.strftime("%I:%M %p")

print day
print time