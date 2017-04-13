__author__ = 'tklutey'

from spotipy.oauth2 import SpotifyClientCredentials
import spotipy
import json
import lyrics
import pprint
from sqlalchemy import *


def parse_playlist(playlist_uri, user_uri):

    """Set up sqlalchemy connection"""
    DBURI = "postgresql://tlk2129:0790@104.196.135.151/proj1part2"
    engine = create_engine(DBURI)
    connection = engine.connect()
    trans = connection.begin()

    client_credentials_manager = SpotifyClientCredentials()
    sp = spotipy.Spotify(client_credentials_manager=client_credentials_manager)

    username = playlist_uri.split(':')[2]
    playlist_id = playlist_uri.split(':')[4]
    results = sp.user_playlist(username, playlist_id)
    playlist_name = results.get('name')

    #User table DONE TESTED
    user_query = "'" + user_uri + "', '" + username + "'"
    user_insert = "INSERT INTO Spotify_user( user_id, user_name ) VALUES( " + user_query + " );"
    connection.execute(text(user_insert))

    #Playlist table DONE TESTED
    playlist_query = "'" + playlist_name + "', '" + playlist_id + "', '" + user_uri + "'"
    playlist_insert = "INSERT INTO Playlist( playlist_name, playlist_id, user_id ) VALUES( " + playlist_query + " );"
    connection.execute(text(playlist_insert))


    for i,t in enumerate(results['tracks']['items']):
            current = t['track']

            ## Artist table DONE TESTED
            artist_name = current.get('album').get('artists')[0].get('name')
            artist_uri = current.get('album').get('artists')[0].get('uri')
            artist_query = "'" + artist_name + "', '" + artist_uri + "'"
            artist_insert = "INSERT INTO Artist( artist_name, artist_id ) VALUES( " + artist_query + " );"
            artist_test = "SELECT * FROM Artist WHERE(artist_id='" + artist_uri + "');"
            if connection.execute(text(artist_test)).first() == None:
                connection.execute(text(artist_insert))



            ## Album table DONE TESTED
            album_name = current.get('album').get('name')
            album_uri = current.get('album').get('uri')
            album_query = "'" + album_name + "', '" + album_uri + "'"
            album_insert = "INSERT INTO Album( album_name, album_id ) VALUES( " + album_query + " );"
            album_test = "SELECT * FROM Album WHERE(album_id='" + album_uri + "');"
            if connection.execute(text(album_test)).first() == None:
                connection.execute(text(album_insert))

            ## Song table HAVING ISSUES W LYRICS apostrophes
            song_name = current['name']
            track_uri = current['uri']
            # ascii_track = track_uri.encode('ascii', 'ignore')
            # ascii_name = song_name.encode('ascii', 'ignore')
            track_lyrics = lyrics.lyrics(artist_name, song_name)
            track_lyrics = track_lyrics.replace("'","''")
            unicode_lyrics = unicode(track_lyrics, "utf-8")
            release_date = sp.album(album_uri).get('release_date')
            year = release_date.split('-')[0]

            # ascii_year = year.encode('ascii', 'ignore')

            song_query = "'" + track_uri + "', '" + song_name + "', '" + year + "', '" + unicode_lyrics + "', '" + artist_uri + "', '" + album_uri + "'"
            # song_query = "'" + ascii_track + "', '" + ascii_name + "', '" + ascii_year + "', '" + track_lyrics + "', '" + artist_uri.encode('ascii', 'ignore') + "', '" + album_uri.encode('ascii', 'ignore') + "'"

            song_insert = "INSERT INTO Song( song_id, song_name, year, lyrics, artist_id, album_id ) VALUES( " + song_query + " );"
            connection.execute(text(song_insert))


            ## Genre table DONE TESTED
            genres = sp.artist(artist_uri).get('genres')
            for x in genres:
                genre_query = "'" + artist_uri + "', '" + x + "'"
                genre_insert = "INSERT INTO Genre( artist_id, genre_name ) VALUES( " + genre_query + " );"
                genre_test = "SELECT * FROM Genre WHERE(artist_id='" + artist_uri + "' AND genre_name='" + x + "');"
                if connection.execute(text(genre_test)).first() == None:
                    connection.execute(text(genre_insert))


            #Contains table
            contains_query = "'" + playlist_id + "', '" + track_uri + "'"
            contains_insert = "INSERT INTO Contains( playlist_id, song_id ) VALUES( " + contains_query + " );"
            connection.execute(text(contains_insert))

            # #in_genre table
            # in_genre_query = "'" + artist_uri + "', '" + genre_name + "'"
            # in_genre_insert = "INSERT INTO in_genre( artist_id, genre_name ) VALUES( " + in_genre_query + " );"
            # connection.execute(text(in_genre_insert))

            print song_name + ", " + artist_name + ", " + album_name + ", " + year + ", " \
                 + ", " + track_uri
            print genres
            print track_lyrics
            print "---------------------------------------------"

    trans.commit()


    #print json.dumps(results, indent=4)


def main():

    playlist_uri = 'spotify:user:tklutey:playlist:4jsH6oQYN8jA29OWdKaxAM'
    user_uri = 'spotify:user:tklutey'
    parse_playlist(playlist_uri, user_uri)


if __name__ == "__main__":
    main()


