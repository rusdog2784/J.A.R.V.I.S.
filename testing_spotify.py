import spotipy
import spotipy.util as util
from spotipy.oauth2 import SpotifyClientCredentials
import os

spotify_username = 'scott.tkdmaster@mac.com'
spotify_scope = 'user-library-read user-top-read user-read-private streaming'

spotify_token = util.prompt_for_user_token(spotify_username, spotify_scope)

sp = spotipy.Spotify(auth=spotify_token)
results = sp.current_user_top_tracks()

for item in results['items']:
    print item['uri']

'''
artist_list = []
track_list = []
my_artists = sp.current_user_top_artists()
for item in my_artists['items']:
    artist_list.append(item['id'])
my_tracks = sp.current_user_top_tracks()
for item in my_tracks['items']:
    track_list.append(item['id'])
recommendations = sp.recommendations(seed_artists=[artist_list[0]])
for r in recommendations['tracks']:
    print r['name'], '-', r['artists'][0]['name']
'''