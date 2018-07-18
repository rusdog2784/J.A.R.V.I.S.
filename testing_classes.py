import json
import webbrowser

class Test(object):
    spotify_username = "scott"

    def __init__(self):
        print(self.spotify_username)
        # Initiating website variable from the "websites.json" file which contains a dictionary of websites
        with open("websites.json", 'r') as f:
            self.websites = json.load(f)

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

test = Test()
test.goToWebsite('facebook')