__author__ = 'tklutey'

import spotipy
import lyrics
import pprint
from sqlalchemy import *
from spotipy.oauth2 import SpotifyClientCredentials

def parse_playlist(username, playlist_uri, engine):

    client_credentials_manager = SpotifyClientCredentials()
    sp = spotipy.Spotify(client_credentials_manager=client_credentials_manager)

    # username = playlist_uri.split(':')[2]
    playlist_id = playlist_uri.split(':')[4]
    print playlist_id
    user_uri = "spotify:user:" + username
    results = sp.user_playlist(username, playlist_id)
    # pprint.pprint(results)
    playlist_name = results.get('name')

    #Playlist table DONE TESTED UNCOMMENT!!
    playlist_query = "'" + playlist_name + "', '" + playlist_id + "', '" + user_uri + "'"
    playlist_insert = "INSERT INTO Playlist( playlist_name, playlist_id, user_id ) VALUES( " + playlist_query + " );"
    engine.execute(text(playlist_insert))


    for i,t in enumerate(results['tracks']['items']):
            current = t['track']

            ## Artist table DONE TESTED
            artist_name = current.get('album').get('artists')[0].get('name')
            artist_uri = current.get('album').get('artists')[0].get('uri')
            artist_query = "'" + artist_name + "', '" + artist_uri + "'"
            artist_insert = "INSERT INTO Artist( artist_name, artist_id ) VALUES( " + artist_query + " );"
            artist_test = "SELECT * FROM Artist WHERE(artist_id='" + artist_uri + "');"
            if engine.execute(text(artist_test)).first() == None:
                engine.execute(text(artist_insert))



            ## Album table DONE TESTED
            album_name = current.get('album').get('name')
            album_uri = current.get('album').get('uri')
            album_query = "'" + album_name + "', '" + album_uri + "'"
            album_insert = "INSERT INTO Album( album_name, album_id ) VALUES( " + album_query + " );"
            album_test = "SELECT * FROM Album WHERE(album_id='" + album_uri + "');"
            if engine.execute(text(album_test)).first() == None:
                engine.execute(text(album_insert))

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
            engine.execute(text(song_insert))

            ##Contains table
            contains_query = "'" + playlist_id + "', '" + track_uri + "'"
            contains_insert = "INSERT INTO contains( playlist_id, song_id ) VALUES( " + contains_query + " );"
            contains_test = "SELECT * FROM contains WHERE(playlist_id='" + playlist_id + "' AND song_id='" + track_uri + "');"
            if engine.execute(text(contains_test)).first() == None:
                engine.execute(text(contains_insert))


            ## in_genre table DONE TESTED
            genres = sp.artist(artist_uri).get('genres')
            for x in genres:
                genre_query = x
                genre_insert = "INSERT INTO Genre( genre_name ) VALUES( '" + genre_query + "' );"
                genre_test = "SELECT * FROM Genre WHERE(genre_name='" + x + "');"
                if engine.execute(text(genre_test)).first() == None:
                    engine.execute(text(genre_insert))

                in_genre_query = "'" + artist_uri + "', '" + x + "'"
                in_genre_insert = "INSERT INTO in_genre( artist_id, genre_name ) VALUES( " + in_genre_query + " );"
                in_genre_test = "SELECT * FROM in_genre WHERE(artist_id='" + artist_uri + "' AND genre_name='" + x + "');"
                if engine.execute(text(in_genre_test)).first() == None:
                    engine.execute(text(in_genre_insert))


# def make_engine():
#         DBURI = "postgresql://tlk2129:0790@104.196.135.151/proj1part2"
#         engine = create_engine(DBURI)
#         return engine
#
# parse_playlist("tklutey", "spotify:user:tklutey:playlist:5qpLsOzNuCNH43zTMPPEWD", make_engine())

