## User defined classes and import statements!

import sys
import spotipy
import spotipy.util as util
from keys import *

class User:

    def __init__(self, user):
        self.user = user
        self.sp = self.login(user)
        self.input_song = ''
        self.id = self.sp.current_user()['id']
        self.genres = self.sp.recommendation_genre_seeds()['genres']
        print(self)

    def login(self, user):
        token = util.prompt_for_user_token(user, scope, clientID, clientSecret, redirectURL)
        if token: return spotipy.Spotify(auth=token)
        else:
            print("Can't get token for", user)
            sys.exit()

    def search(self, song, lim = 1):
        results = self.sp.search(q = str(song), limit = lim)

        if not results['tracks']['items']:
            print('No songs found!')
            sys.exit()

        elif lim == 1:
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

    def generate_recommendations(self, song, artist):
        recommendations = self.sp.recommendations([song.id], artist.genres, [self.input_song.id])['tracks']

        for i in range(len(recommendations)):
            yield Song(recommendations[i])

    def __repr__(self):
        return '\nUSER: {0}'.format(self.user) + '\nID: {0}'.format(self.id)


class Song:

    def __init__(self, input_song):
        ''' input_song is an output from sp.search()'''
        self.name = input_song['name']
        self.id = input_song['id']
        self.image = input_song['album']['images'][0]['url']
        self.preview = input_song['preview_url']
        self.artist = input_song['artists'][0]
        self.artist_name = self.artist['name']

    def __repr__(self):
        return (
            'NAME: ' + self.name +
            '\nARTIST: ' + self.artist_name +
            '\nID: ' + self.id
            )

    def find_playlists(self, user, lim = 10):
        results = user.sp.search(self.name, limit = lim, type='playlist')

        for t in results['playlists']['items']:
            print(Playlist(t))


class Playlist:

    def __init__(self, input_playlist = None):
        ''' input_playlist is an output from sp.search()'''
        if input_playlist:
            self.name = input_playlist['name']
            self.id = input_playlist['id']

    def add_song(self, song):
        pass

    def __repr__(self):
        return '{0}'.format(self.name)

class Artist:

    def __init__(self, song, user):
        self.name = song.artist['name']
        self.id = song.artist['id']
        self.uri = song.artist['uri']
        self.genres = [genre for genre in self.generate_genres(user) if genre in user.genres]

    def generate_genres(self, user):
        artist_metadata = user.sp.artist(self.uri)
        return artist_metadata['genres']

    def __repr__(self):
        return 'ARTIST: {0} \nID: {1} \nURI: {2}'.format(self.name, self.id, self.uri) + '\nGENRES:' + str(self.genres)
