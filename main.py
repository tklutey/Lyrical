import string
import time
import re
import urllib

"""
Function that scrapes azlyrics.com and returns song lyrics as string.
"""
def lyrics(artist,song):
    artist = artist.lower()
    song = song.lower()
    artist = re.sub('[^A-Za-z0-9]+', "", artist)
    song = re.sub('[^A-Za-z0-9]+', "", song)
    request = "http://azlyrics.com/lyrics/"+str(artist)+"/"+str(song)+".html"
    print request
    raw_html = urllib.urlopen(request)
    html_copy = str(raw_html.read())
    split = html_copy.split('<!-- Usage of azlyrics.com content by any third-party lyrics provider is prohibited by our licensing agreement. Sorry about that. -->', 1);
    words = split[1].split('<!-- MxM banner -->');
    split = words[0].split('</div>')
    lyrics = split[0]
    lyrics = re.sub('(<.*?>)',"",lyrics)
    return lyrics

"""
Function to convert Spotify metadata syntax into html-compatible queries.
"""
def convert_query(input):
    input.replace(" ", "")
    input.replace(".", "")
    input.replace("-","")
    input.replace("'", "")
    input = input.lower()
    return input

def main():
    artist = convert_query("Run-D.M.C.")
    song = convert_query("It's Tricky")
    body = lyrics(artist, song)
    print body

if __name__ == "__main__":
    main()
