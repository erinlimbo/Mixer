# testing the Spotipy library: searching for a song and user auth
# V0.1, edited last by John So

from user_module import *

# LOGIN SCREEN FUNCTIONS
user_id = input('Username:\n>>> ')
user = User(user_id)

# INITIAL SEARCH FUNCTION
initial = user.choose_song()

print(initial)

# GENERATING 10 'MOST SIMILAR' SONGS (aka training data!)
print('These playlists contain {0} by {1}:'.format(initial.name, initial.artist))
