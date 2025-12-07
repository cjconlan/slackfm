import os
import sys
import time
import json
import pylast

from collections import deque

# pip install pylast
# pylast/pylast: A Python interface to Last.fm and Libre.fm

api_keys_file = ".api_app_keys"

with open(api_keys_file, 'r') as file:
    api_keys = json.load(file)


try:
    USERNAME = sys.argv[1]
except IndexError:
    USERNAME = api_keys.get("user")

API_KEY = api_keys.get("key")
API_SECRET = api_keys.get("secret")


def get_current_track(api_key, api_secret, username):
    try:
        network = pylast.LastFMNetwork(api_key=api_key, api_secret=api_secret)
        user = network.get_user(username)
        current_track = user.get_now_playing()

        # current_track.info
        # {'album': 'Dark Space -I', 'image': [
        #        'https://lastfm.freetls.fastly.net/i/u/34s/1772c5ae7ff6287b2e1eb204069d5aaf.png',     # x-small
        #        'https://lastfm.freetls.fastly.net/i/u/64s/1772c5ae7ff6287b2e1eb204069d5aaf.png',     # small
        #        'https://lastfm.freetls.fastly.net/i/u/174s/1772c5ae7ff6287b2e1eb204069d5aaf.png',    # med
        #        'https://lastfm.freetls.fastly.net/i/u/300x300/1772c5ae7ff6287b2e1eb204069d5aaf.png'  # large
        #        ]}

        
        if current_track:
            artist = current_track.artist.name
            title = current_track.title
            release = current_track.info.get('album')
            release_str = f"  (Release: {release})" if release is not None else ""
            return f"Now Playing: {artist} - {title}{release_str}"
        else:
            return f"User is not currently scrobbling."
    except pylast.WSError as e:
        return f"Last.fm API Error: {e}"
    except Exception as e:
        return f"An unexpected error occurred: {e}"


def display(text):
    timestamp = time.ctime(time.time())
    print(f"{timestamp:<25}{result}")


announce = None
hist = deque(maxlen=2)
while True:
    try:
        result = get_current_track(API_KEY, API_SECRET, USERNAME)
        hist.append(result)
        if len(hist) == hist.maxlen and len(set(hist)) == 1:
            if announce:
                display(result)
                announce = False
        else:
            announce = True
        sys.stdout.flush()
        time.sleep(10)
    except KeyboardInterrupt:
        print()
        break
    

