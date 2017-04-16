import re
import urllib
from wordcloud import WordCloud
from spotipytest import test
import sys

"""
Function that scrapes azlyrics.com and returns song lyrics as string.
"""
def lyrics(input_artist,input_song):
    artist = convert_query(input_artist)
    song = convert_query(input_song)
    try:
        request = "http://azlyrics.com/lyrics/"+str(artist)+"/"+str(song)+".html"
        print request
        raw_html = urllib.urlopen(request)
        html_copy = str(raw_html.read())
        split = html_copy.split('<!-- Usage of azlyrics.com content by any third-party '
                                'lyrics provider is prohibited by our licensing agreement. Sorry about that. -->', 1);
        words = split[1].split('<!-- MxM banner -->');
        split = words[0].split('</div>')
        lyrics = split[0]
        lyrics = re.sub('(<.*?>)',"",lyrics)
        return lyrics
    except IndexError:      #means that there are no lyrics for given song on azlyrics
        sys.stderr.write("No Lyrics Found \n")
        return " "

"""
Function to convert Spotify metadata syntax into html-compatible queries.
"""
def convert_query(input):
    input = input.replace(" ", "")
    input = input.replace(".", "")
    input = input.replace("-","")
    input = input.replace("'", "")
    input = input.replace(":", "")

    if '(' in input:
        half = input.split("(")
        input = half[0]

    ##NEED TO CATCH "THE" IN ARTISTS
    #need to catch rapper titles for groups with multiple singers
    #catch 'quot'
    #catch tags i.e. "chorus"

    input = input.lower()
    return input

"""
Generates word cloud from block of lyrics.
"""
def word_cloud(lyrics):
    cloud = WordCloud().generate(lyrics)

    # Display the generated image:
    # the matplotlib way:
    import matplotlib.pyplot as plt
    plt.imshow(cloud)
    plt.axis("off")

    # lower max_font_size
    cloud = WordCloud(max_font_size=40).generate(lyrics)
    plt.figure()
    plt.imshow(cloud)
    plt.axis("off")
    plt.show()

# def main():
#
#     ##if user provides CL args
#     if(len(sys.argv) == 3):
#         input_query = sys.argv[1]
#         input_artist = sys.argv[2]
#         tracklist = test(input_query, input_artist)
#     ##default
#     else:
#         input_artist = "Kanye West"
#         input_query = "The Life of Pablo"
#         tracklist = test(input_query, input_artist)
#
#     song_lyrics = []
#
#     for i in tracklist:
#         artist = convert_query(input_artist)
#         song = convert_query(i)
#         song_lyrics.append(lyrics(artist, song))
#
#     word_mass = ''.join(song_lyrics)
#     word_cloud(word_mass)


if __name__ == "__main__":
    main()
