import deezer
import os

client = deezer.Client()

genre_id_dict = {
    "rock": 152,
    "country": 84,
    "folk": 466,
    "reggae": 122,
    "latin": 197,
    "blues": 153,
    "jazz": 129,
    "metal": 464,
    "gospel": 187,
    "classical": 98,
    "pop": 132,
    "electronic": 110,
    "dance": 113,
    "soul": 169,
    "r-n-b": 165,
    "hip-hop": 116,
    "world music": 484,
    "new age": 474,
}

genre = client.get_genre(152)
chart = client.get_chart(relation=genre.get_relation(1))
print(chart)


"""
#to get list of all genres and genre_id
for i in range(0,500):
    try:
        genre = client.get_genre(i)
        print(i, genre)
    except ValueError as e:
        continue

chart = client.get_chart(112)
top_chart_tracks = chart.get_tracks()
artists = genre.get_artists()

tracks = top_chart_tracks.get_top()

print(tracks)
print(top_chart_tracks)

print(os.urandom(24).hex())


    genre = client.get_genre(113)

    artists = genre.get_artists()

    tracks = artists[1].get_top()

    print(tracks)

"""