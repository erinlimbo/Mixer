# testing the Spotipy library: searching for playlists to extrapolate songs from
# V0.1, edited last by John So

from user_module import *
good_songs = []

# LOGIN SCREEN FUNCTIONS
user_id = input('Username:\n>>> ')
user = User(user_id)

# INITIAL SEARCH FUNCTION
initial = user.choose_song()
initial_artist = Artist(initial, user)

good_songs.append(initial)

print()
print(initial)
print()
print(initial_artist)
print()
# GENERATING 10 'MOST SIMILAR' SONGS (aka training data!)
recommended = user.generate_recommendations(initial, initial_artist)
for i in range(10):
    curr_song = next(recommended)

    print(curr_song)
    swipe = input('[y]/[n]\n>>> ')

    if swipe == 'y':
        good_songs.append(curr_song.name)

    print(good_songs, '\n')
#print('These playlists contain {0} by {1}:'.format(initial.name, initial.artist['name']))
#initial.find_playlists(user)
