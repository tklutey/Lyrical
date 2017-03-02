__author__ = 'tklutey'

from spotipy.oauth2 import SpotifyClientCredentials
import spotipy
import json


def return_playlist(uri):

    client_credentials_manager = SpotifyClientCredentials()
    sp = spotipy.Spotify(client_credentials_manager=client_credentials_manager)

    username = uri.split(':')[2]
    playlist_id = uri.split(':')[4]

    results = sp.user_playlist(username, playlist_id)

    top_songs = []
    sql_data = {}

    for i, t in enumerate(results['tracks']['items']):
            current = t['track']
            sql_data = current['album']['name']

    print json.dumps(results, indent=4)
    #print json.dumps(sql_data, indent=4)



    return results


def main():

    playlist_uri = 'spotify:user:tklutey:playlist:4jsH6oQYN8jA29OWdKaxAM'
    return_playlist(playlist_uri)

if __name__ == "__main__":
    main()


