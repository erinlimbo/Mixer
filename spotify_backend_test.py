# testing the Spotipy library: searching for playlists to extrapolate songs from
# V0.2, edited last by John So

from user_module import *

# LOGIN SCREEN FUNCTIONS
login_id = input('Username:\n>>> ')
user = User(login_id)
print()

# INITIAL SEARCH FUNCTION
initial = user.choose_song()
initial_artist = Artist(initial, user)

print(initial)

user.recommendations.append(initial)
user.sp.user_playlist_add_tracks(user = user, playlist_id = user.mixed_playlist.id, tracks = [initial.id])

# GENERATING 10 'MOST SIMILAR' SONGS (aka training data!)

recommended = user.generate_recommendations([initial], [initial_artist])

while True:
    i = 0

    while len(user.recommendations) < 20 or i % 10 != 0:
        curr_song = next(recommended)

        print(curr_song)
        if curr_song.preview: webbrowser.open(curr_song.preview, autoraise=True)
        swipe = input('[y]/[n]\n>>> ')

        if swipe == 'y':
            user.recommendations.append(curr_song)
            user.sp.user_playlist_add_tracks(user = user, playlist_id = user.mixed_playlist.id, tracks = [curr_song.id])
        elif swipe == 'exit':
            print("Enjoy your songs!\n")
            sys.exit()
        i += 1

    recommended = user.generate_recommendations(recommendations, [Artist(r, user) for r in recommendations], limit = 100)
print("Enjoy your new songs!")
