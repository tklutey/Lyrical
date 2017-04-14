import spotipy
import json
import spotipy.util as util

def test():
    client_id = "08ce831d3cc3450a80d4333d11bb9945"
    client_secret = "08434edc62004761a790d8014a3a5e79"
    redirect_uri = "http://localhost:8111/callback"
    username = "tklutey"
    token = util.prompt_for_user_token(username, scope=None, client_id=client_id, client_secret=client_secret, redirect_uri=redirect_uri)
    sp = spotipy.Spotify(token)
    playlists = sp.user_playlists(username)
    for playlist in playlists['items']:
        print(playlist['name'])

if __name__ == "__main__":
    test()
