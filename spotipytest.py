import spotipy

def test(query, group):

    sp = spotipy.Spotify()

    top_songs = []

    search = query + " " + group
    print search
    results = sp.search(q=search, limit=20)

    for i, t in enumerate(results['tracks']['items']):
        current = t['name']
        top_songs.append(current)

    return top_songs

if __name__ == "__main__":
    test()