__author__ = 'tklutey'

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
import spotipy
import spotipy.util as util
from lyric_cloud import word_cloud



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

  lyric_query = "SELECT lyrics FROM SONG ;"
  cursor = engine.execute(text(lyric_query))
  lyric_list = []
  for row in cursor:
    lyric_list.append((row['lyrics']))

  result = word_cloud(lyric_list)

  #
  # example of a database query
  #
  cursor = g.conn.execute("SELECT artist_name FROM artist")
  names = []
  for result in cursor:
    names.append(result['artist_name'])  # can also be accessed using result[0]
  cursor.close()

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
  context = dict(data = names)


  #
  # render_template looks in the templates/ folder for files.
  # for example, the below file reads template/index.html
  #
  return render_template("index.html", result=result, **context)

#
# This is an example of a different path.  You can see it at:
#
#     localhost:8111/another
#
# Notice that the function name is another() rather than index()
# The functions for each app.route need to have different names
#
# @app.route('/another')
# def another():
# return render_template("another.html")

# @app.route('/login')
# def login():
#     return render_template("login.html")


@app.route('/testpage', methods=['POST', 'GET'])
def testpage():
    print "got it!"
    username = request.form['username']
    client_id = "08ce831d3cc3450a80d4333d11bb9945"
    client_secret = "08434edc62004761a790d8014a3a5e79"
    redirect_uri = "http://localhost:8111/callback"
    token = util.prompt_for_user_token(username, scope=None, client_id=client_id, client_secret=client_secret, redirect_uri=redirect_uri)
    sp = spotipy.Spotify(token)
    playlists = sp.user_playlists(username)

    playlist_names = []
    for playlist in playlists['items']:
        # print(playlist['name'])
        playlist_names.append(playlist['name'])

    for x in playlist_names:
        print x

    return render_template("testpage.html", username=username, playlists=playlist_names)


@app.route('/cloud')
def cloud():

    ##NOT NECESSARY IN FINAL
    lyric_query = "SELECT lyrics FROM SONG WHERE song_name LIKE 'Famous' ;"
    cursor = engine.execute(text(lyric_query))
    lyric_list = []
    for row in cursor:
        lyric_list.append((row['lyrics']))


    result = word_cloud(lyric_list)
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
    #find names
    name = request.form.getlist('name')
    print(name)
    names = []
    i = 0
    while(i<len(name)):
        cursor = g.conn.execute("SELECT * FROM artist WHERE artist_name = '{}'".format(name[i]))
        for result in cursor:
            names.append(result['artist_name'])  # can also be accessed using result[0]
        cursor.close()
        i+=1
   # context = dict(data=names)

    year = request.form.getlist('year')
    print(year)
    years = []
    i = 0
    while (i < len(year)):
        cursor = g.conn.execute("SELECT * FROM song WHERE year = '{}'".format(year[i]))
        for result in cursor:
            years.append(result['year'])  # can also be accessed using result[0]
        cursor.close()
        i += 1

    context = dict(data=years)


    return render_template("another.html", **context)

#wtf
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

