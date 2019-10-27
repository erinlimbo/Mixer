from flask import Flask, render_template

# import firebase_admin
# from firebase_admin import credentials
# from firebase_admin import firestore
from user_module import *
from flask import request

import sys
import spotipy
import spotipy.util as util
from keys import *
# from user_module import *


app = Flask(__name__)

# Use the application default credentials
# cred = credentials.ApplicationDefault()
# firebase_admin.initialize_app(cred, {
#   'projectId': "musicmixer",
# })

# db = firestore.client()

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

        # chosen_song = input('\nWhich song? \n>>> ')
        chosen_song = 0;

        return results['tracks']['items'][int(chosen_song)]

    def choose_song(self):
        song_id = request.form['songIdTextBox']

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
        return ('"{0}", {1}'.format(self.name, self.artist_name))

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

@app.route('/home', methods=['GET', 'POST'])
def root():
    good_songs = []

    if request.method == 'POST':

        # LOGIN SCREEN FUNCTIONS
        # user_id = input('Username:\n>>> ')
        user_id = "osnhoj"
        user = User(user_id)

        # INITIAL SEARCH FUNCTION
        initial = user.choose_song()
        initial_artist = Artist(initial, user)

        good_songs.append(initial)

        # GENERATING 10 'MOST SIMILAR' SONGS (aka training data!)
        recommended = user.generate_recommendations(initial, initial_artist)
        rec_songs = []
        for i in range(10):
            curr_song = next(recommended)
            rec_songs.append(curr_song)
            # add = request.form['yesorno']
            # if (add == "yes"):
            # good_songs.append(curr_song)
            # print(curr_song)
            # swipe = input('[y]/[n]\n>>> ')
            #
            # if swipe == 'y':
            #     good_songs.append(curr_song)
            #
            # print(good_songs, '\n')


        name = initial.name
        id = initial.id
        artist = initial.artist_name
        image = initial.image
        good_songs = good_songs
        rec_songs = rec_songs


        # FIREBASE STUFF; only dummy variables right now
        # doc_ref = db.collection(u'users').document(u'alovelace')
        # doc_ref.set({
        #     u'first': u'Ada',
        #     u'last': u'Lovelace',
        #     u'born': 1815
        # })
        #
        # doc_ref = db.collection(u'users').document(u'aturing')
        # doc_ref.set({
        #     u'first': u'Alan',
        #     u'middle': u'Mathison',
        #     u'last': u'Turing',
        #     u'born': 1912
        # })
        #
        # users_ref = db.collection(u'users')
        # docs = users_ref.stream()
        #
        # for doc in docs:
        #     print(u'{} => {}'.format(doc.id, doc.to_dict()))

        return render_template('home.html', name=name, id=id, artist=artist, image=image, good_songs = good_songs, rec_songs = rec_songs)

    if request.method == 'GET':
        name = "test"
        id = 12345
        artist = "test"
        good_songs = ["test"]
        return render_template('home.html', name=name, id=id, artist=artist, good_songs = good_songs)


@app.route('/profile')
def profile():

    return render_template('profile.html')

@app.route('/login')
def login():

    return render_template('login.html')


if __name__ == '__main__':
    # This is used when running locally only. When deploying to Google App
    # Engine, a webserver process such as Gunicorn will serve the app. This
    # can be configured by adding an `entrypoint` to app.yaml.
    # Flask's development server will automatically serve static files in
    # the "static" directory. See:
    # http://flask.pocoo.org/docs/1.0/quickstart/#static-files. Once deployed,
    # App Engine itself will serve those files as configured in app.yaml.
    app.run(host='127.0.0.1', port=8080, debug=True)
