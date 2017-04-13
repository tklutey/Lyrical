__author__ = 'tklutey, abair'

#!/usr/bin/env python2.7

"""
Columbia's COMS W4111.001 Introduction to Databases
Example Webserver

To run locally:

    python server.py

Go to http://localhost:8111 in your browser.

A debugger such as "pdb" may be helpful for debugging.
Read about it online.
"""

import os
from sqlalchemy import *
from sqlalchemy.pool import NullPool
from flask import Flask, request, render_template, g, redirect, Response
from wordcloud import WordCloud
import io
import base64



tmpl_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'templates')
app = Flask(__name__, template_folder=tmpl_dir)


#
# The following is a dummy URI that does not connect to a valid database. You will need to modify it to connect to your Part 2 database in order to use the data.
#
# XXX: The URI should be in the format of:
#
#     postgresql://USER:PASSWORD@104.196.135.151/proj1part2
#
# For example, if you had username gravano and password foobar, then the following line would be:
#
#     DATABASEURI = "postgresql://gravano:foobar@104.196.135.151/proj1part2"
#
DATABASEURI = "postgresql://tlk2129:0790@104.196.135.151/proj1part2"


#
# This line creates a database engine that knows how to connect to the URI above.
#
engine = create_engine(DATABASEURI)

#
# Example of running queries in your database
# Note that this will probably not work if you already have a table named 'test' in your database, containing meaningful data. This is only an example showing you how to run queries in your database using SQLAlchemy.

engine.execute("""CREATE TABLE IF NOT EXISTS test (
  id serial,
  name text
);""")
engine.execute("""INSERT INTO test(name) VALUES ('grace hopper'), ('alan turing'), ('ada lovelace');""")


@app.before_request
def before_request():
  """
  This function is run at the beginning of every web request
  (every time you enter an address in the web browser).
  We use it to setup a database connection that can be used throughout the request.

  The variable g is globally accessible.
  """
  try:
    g.conn = engine.connect()
  except:
    print ("uh oh, problem connecting to database")
    import traceback; traceback.print_exc()
    g.conn = None

@app.teardown_request
def teardown_request(exception):
  """
  At the end of the web request, this makes sure to close the database connection.
  If you don't, the database could run out of memory!
  """
  try:
    g.conn.close()
  except Exception as e:
    pass


#
# @app.route is a decorator around index() that means:
#   run index() whenever the user tries to access the "/" path using a GET request
#
# If you wanted the user to go to, for example, localhost:8111/foobar/ with POST or GET then you could use:
#
#       @app.route("/foobar/", methods=["POST", "GET"])
#
# PROTIP: (the trailing / in the path is important)
#
# see for routing: http://flask.pocoo.org/docs/0.10/quickstart/#routing
# see for decorators: http://simeonfranklin.com/blog/2012/jul/1/python-decorators-in-12-steps/
#
@app.route('/')
def index():
  """
  request is a special object that Flask provides to access web request information:

  request.method:   "GET" or "POST"
  request.form:     if the browser submitted a form, this contains the data in the form
  request.args:     dictionary of URL arguments, e.g., {a:1, b:2} for http://localhost?a=1&b=2

  See its API: http://flask.pocoo.org/docs/0.10/api/#incoming-request-data
  """

  # DEBUG: this is debugging code to see what request looks like
  print (request.args)


  #
  # example of a database query
  #
  cursor = g.conn.execute("SELECT artist_name FROM artist")
  names = []
  for result in cursor:
    names.append(result['artist_name'])  # can also be accessed using result[0]
  cursor.close()
  names = sorted(removeDuplicates(names))

  cursor = g.conn.execute("SELECT year FROM song")
  years = []
  for result in cursor:
      years.append(result['year'])  # can also be accessed using result[0]
  cursor.close()
  years = sorted(removeDuplicates(years))


  cursor = g.conn.execute("SELECT genre_name FROM genre")
  genres = []
  for result in cursor:
      genres.append(result['genre_name'])  # can also be accessed using result[0]
  cursor.close()
  genres = sorted(removeDuplicates(genres))

  cursor = g.conn.execute("SELECT album_name FROM album")
  albums = []
  for result in cursor:
      albums.append(result['album_name'])  # can also be accessed using result[0]
  cursor.close()
  albums = sorted(removeDuplicates(albums))

  cursor = g.conn.execute("SELECT song_name FROM song")
  songs = []
  for result in cursor:
      songs.append(result['song_name'])  # can also be accessed using result[0]
  cursor.close()
  songs = sorted(removeDuplicates(songs))

  #
  # Flask uses Jinja templates, which is an extension to HTML where you can
  # pass data to a template and dynamically generate HTML based on the data
  # (you can think of it as simple PHP)
  # documentation: https://realpython.com/blog/python/primer-on-jinja-templating/
  #
  # You can see an example template in templates/index.html
  #
  # context are the variables that are passed to the template.
  # for example, "data" key in the context variable defined below will be
  # accessible as a variable in index.html:
  #
  #     # will print: [u'grace hopper', u'alan turing', u'ada lovelace']
  #     <div>{{data}}</div>
  #
  #     # creates a <div> tag for each element in data
  #     # will print:
  #     #
  #     #   <div>grace hopper</div>
  #     #   <div>alan turing</div>
  #     #   <div>ada lovelace</div>
  #     #
  #     {% for n in data %}
  #     <div>{{n}}</div>
  #     {% endfor %}
  #

  # context = dict(names = names)
  # context2 = dict(years =years )

  #
  # render_template looks in the templates/ folder for files.
  # for example, the below file reads template/index.html
  #
  return render_template("index.html", years=years,names = names,genres = genres,albums = albums,songs = songs)

#
# This is an example of a different path.  You can see it at:
#
#     localhost:8111/another
#
# Notice that the function name is another() rather than index()
# The functions for each app.route need to have different names
#
#@app.route('/another')
#def another():
#  return render_template("another.html")

def removeDuplicates(values):
    mySet = set(values)
    result = list(mySet)
    return result

@app.route('/songLyrics.html', methods=['POST'])
def songLyrics():
    song = request.form['song']
    cursor = engine.execute("SELECT lyrics FROM song WHERE song_name = '{}'".format(song))

    lyric_list = 0
    for result in cursor:
        lyric_list = (result['lyrics'])
    # print(lyric_list)
    list = lyric_list.splitlines()

    # print(lyric_list[2])
    # print(lyric_list)
    return render_template('songLyrics.html',lyrics = list)


@app.route('/cloud')
def cloud():

    lyric_query = "SELECT lyrics FROM SONG WHERE song_name LIKE 'Famous' ;"
    cursor = engine.execute(text(lyric_query))
    lyric_list = []
    for row in cursor:
        lyric_list.append((row['lyrics']))
    word_mass = ''.join(lyric_list)

    cloud = WordCloud().generate(word_mass)

    # Display the generated image:
    # the matplotlib way:
    import matplotlib.pyplot as plt
    plt.imshow(cloud)
    plt.axis("off")

    # lower max_font_size
    cloud = WordCloud(max_font_size=40).generate(word_mass)
    plt.figure()
    plt.imshow(cloud)
    plt.axis("off")
    # plt.show()
    plt.savefig('templates/images/cloud.png')

    figfile = io.BytesIO()
    plt.savefig(figfile, format='png')
    figfile.seek(0)
    figdata_png = base64.b64encode(figfile.getvalue())
    result = figdata_png

    return render_template('cloud.html', result=result)


# Example of adding new data to the database
@app.route('/add', methods=['POST'])
def add():
  name = request.form['name']
  g.conn.execute('INSERT INTO test(name) VALUES (%s)', name)
  return redirect('/')


# @app.route('/login')
# def login():
#     abort(401)
#     this_is_never_executed()

@app.route('/another.html', methods=['GET','POST'])
def results():
    #find songs from name
    name = request.form.getlist('name')

    names = []
    i = 0
    while(i<len(name)):
        cursor = g.conn.execute("SELECT song_name FROM artist,song WHERE song.artist_id = artist.artist_id"
                                " AND artist_name = '{}'".format(name[i]))
        for result in cursor:
            names.append(result['song_name'])  # can also be accessed using result[0]

        cursor.close()
        i+=1
# find songs from year
    year = request.form.getlist('year')

    years = []
    i = 0
    while (i < len(year)):
        cursor = g.conn.execute("SELECT song_name FROM song WHERE year = '{}'".format(year[i]))
        for result in cursor:
            years.append(result['song_name'])  # can also be accessed using result[0]

        cursor.close()
        i += 1


    #find songs from album
    album = request.form.getlist('album')
    albums = []
    i = 0
    while (i < len(album)):
        cursor = g.conn.execute("SELECT song_name FROM song,album WHERE song.album_id = album.album_id"
                                " AND album_name = '{}'".format(album[i]))
        for result in cursor:
            albums.append(result['song_name'])  # can also be accessed using result[0]

        cursor.close()
        i += 1

    #find songs from genre
    genre = request.form.getlist('genre')
    genres = []
    i = 0
    while (i < len(genre)):
        cursor = g.conn.execute("SELECT song_name FROM song,genre WHERE song.artist_id = genre.artist_id"
                                " AND genre_name = '{}'".format(genre[i]))
        for result in cursor:
            genres.append(result['song_name'])  # can also be accessed using result[0]

        cursor.close()
        i += 1

    #find songs in songs
    song = request.form.getlist('song')
    songs = song

    #Create list of interesection for these lists
    filledLists = []
    #this is super sloppy and horrid, but whatever
    if(len(names)!=0):
        filledLists.append(names)
    if (len(years) != 0):
        filledLists.append(years)
    if (len(albums) != 0):
        filledLists.append(albums)
    if (len(genres) != 0):
        filledLists.append(genres)
    if (len(songs) != 0):
        filledLists.append(songs)

    intersection = list(set(filledLists[0]).intersection(*filledLists))


    return render_template("another.html", names = names, years = years, albums = albums, genres = genres, songs = songs )

@app.route('/')
def my_view():
    year = [1,2,3]
    context = dict(data=year)
    return render_template('index.html',**context)



if __name__ == "__main__":
  import click

  @click.command()
  @click.option('--debug', is_flag=True)
  @click.option('--threaded', is_flag=True)
  @click.argument('HOST', default='0.0.0.0')
  @click.argument('PORT', default=8111, type=int)
  def run(debug, threaded, host, port):
    """
    This function handles command line parameters.
    Run the server using:

        python server.py

    Show the help text using:

        python server.py --help

    """

    HOST, PORT = host, port
    print ("running on %s:%d" % (HOST, PORT))
    app.run(host=HOST, port=PORT, debug=debug, threaded=threaded)


  run()

