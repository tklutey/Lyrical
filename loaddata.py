__author__ = 'tklutey'

from spotipy.oauth2 import SpotifyClientCredentials
import spotipy
import json
import lyrics
import pprint


def parse_playlist(uri):

    client_credentials_manager = SpotifyClientCredentials()
    sp = spotipy.Spotify(client_credentials_manager=client_credentials_manager)

    username = uri.split(':')[2]
    playlist_id = uri.split(':')[4]

    results = sp.user_playlist(username, playlist_id)

    for i,t in enumerate(results['tracks']['items']):
            current = t['track']
            song_name = current['name']
            artist_name = current.get('album').get('artists')[0].get('name')
            artist_uri = current.get('album').get('artists')[0].get('uri')
            album_name = current.get('album').get('name')
            album_uri = current.get('album').get('uri')
            track_uri = current['uri']
            track_lyrics = lyrics.lyrics(artist_name, song_name)

            album = sp.album(album_uri)
            year = album.get('release_date')

            artist = sp.artist(artist_uri)
            genres = artist.get('genres')

            print song_name + ", " + artist_name + ", " + album_name + ", " + year + ", " \
                 + ", " + track_uri
            print genres
            print track_lyrics
            print "---------------------------------------------"


    #print json.dumps(results, indent=4)
    #return results


def main():

    playlist_uri = 'spotify:user:tklutey:playlist:4jsH6oQYN8jA29OWdKaxAM'
    parse_playlist(playlist_uri)

if __name__ == "__main__":
    main()


