__author__ = 'tklutey'

from sqlalchemy import *
from wordcloud import WordCloud
import io
import base64



# def connection():
#     """Set up sqlalchemy connection"""
#     ##can likely delete when not just a tester
#     DBURI = "postgresql://tlk2129:0790@104.196.135.151/proj1part2"
#     engine = create_engine(DBURI)
#     connection = engine.connect()
#     trans = connection.begin()
#
#     # genre_insert = "INSERT INTO Genre( artist_id, genre_name ) VALUES( " + genre_query + " );"
#     # genre_test = "SELECT * FROM Genre WHERE(artist_id='" + artist_uri + "' AND genre_name='" + x + "');"
#     # if connection.execute(text(genre_test)).first() == None:
#     #     connection.execute(text(genre_insert))
#
#     lyric_query = "SELECT lyrics FROM SONG WHERE song_name LIKE 'Famous' ;"
#     cursor = connection.execute(text(lyric_query))
#     lyric_list = []
#     for row in cursor:
#         lyric_list.append((row['lyrics']))
#
#     # for x in lyric_list:
#     #     print x
#
#     return lyric_list
#
#     # trans.commit()

def word_cloud(lyric_list):

    word_mass = ''.join(lyric_list)

    cloud = WordCloud().generate(word_mass)

    # Display the generated image:
    # the matplotlib way:
    import matplotlib.pyplot as plt
    # plt.imshow(cloud)
    plt.axis("off")

    # lower max_font_size
    cloud = WordCloud(max_font_size=40).generate(word_mass)
    plt.figure()
    # plt.imshow(cloud)
    plt.axis("off")
    # plt.show()
    plt.savefig('templates/images/cloud.png')

    figfile = io.BytesIO()
    plt.savefig(figfile, format='png')
    figfile.seek(0)
    figdata_png = base64.b64encode(figfile.getvalue())
    result = figdata_png

    return result


    # cloud = WordCloud().generate(lyrics)
    #
    # # Display the generated image:
    # # the matplotlib way:
    # import matplotlib.pyplot as plt
    # plt.imshow(cloud)
    # plt.axis("off")
    #
    # # lower max_font_size
    # cloud = WordCloud(max_font_size=40).generate(lyrics)
    # plt.figure()
    # plt.imshow(cloud)
    # plt.axis("off")
    # # plt.show()
    # plt.savefig('cloud.png')

# def main():
#     lyric_list = connection()
#     # print lyric_list[0]
#     # print type(lyric_list[0])
#     word_mass = ''.join(lyric_list)
#     word_cloud(word_mass)
#
#
# if __name__ == "__main__":
#     main()