## User defined classes and import statements!

import spotipy
import spotipy.util as util
from keys import *

class User:

    def __init__(self, user):
        self.user = user
        self.sp = self.login(user)
        self.input_song = ''

    def login(self, user):
        token = util.prompt_for_user_token(user, scope, clientID, clientSecret, redirectURL)
        if token: return spotipy.Spotify(auth=token)
        else:
            print("Can't get token for", user)
            sys.exit()

    def search(self, song, lim = 1):
        results = self.sp.search(q = str(song), limit = lim)

        if lim == 1:
            return results['tracks']['items'][0]

        for i, t in enumerate(results['tracks']['items']):
            print('\n' + str(i) + '\n' + repr(Song(t)))

        chosen_song = input('\nWhich song? \n>>> ')
        return results['tracks']['items'][int(chosen_song)]

    def choose_song(self):
        song_id = input('\nEnter the name of a song!\n>>> ')

        if song_id == 'exit': # escape sequence (back button, etc)
            sys.exit()

        self.input_song = Song(self.search(song_id, 5)) # determine the song2

        return self.input_song

class Song:

    def __init__(self, input_song):
        ''' input_song is an output from sp.search()'''
        self.name = input_song['name']
        self.artist = input_song['artists'][0]['name']
        self.id = input_song['id']

    def __repr__(self):
        return (
            'NAME: ' + self.name +
            '\nARTIST: ' + self.artist +
            '\nID: ' + self.id
            )

class Playlist:
    def __init__(self, playlist = []):
        self.playlist = playlist

    def add_song(self, song):
        self.playlist.append(song)
