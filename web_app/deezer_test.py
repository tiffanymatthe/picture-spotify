import deezer
import os

client = deezer.Client()

genre = client.get_genre(113)

artists = genre.get_artists()

tracks = artists[1].get_top()

print(tracks)

print(os.urandom(24).hex())