import cv2
import numpy as np
import sys
from math import sqrt, pow
import sys, colorsys
import random

import spotipy
import os
from spotipy.oauth2 import SpotifyClientCredentials
from spotipy.oauth2 import SpotifyOAuth
from PIL import Image

import deezer
client = deezer.Client()

auth_manager = SpotifyClientCredentials()
sp = spotipy.Spotify(auth_manager=auth_manager)

img = cv2.imdecode(npimg, cv2.IMREAD_UNCHANGED)
         

# add colour-genre dictionary as a constant here
COLOUR_GENRE = {
    "red" : "rock",
    "green" : "country",
    "yellow" : "latin",
    "blue" : "blues",
    "black" : "metal",
    "white" : "classical",
    "pink": "pop",
    "cyan" : "electronic",
    "orange" : "hip-hop",
    "brown" : "country",
    "purple" : "new age",
}

def get_playlist(img: np.ndarray):
    """Converts an image array with rgb values to a playlist

    Parameters
    ----------
    img : np.ndarray
        The image where colour composition will be extracted from.

    Returns
    -------
    dict [str, str]
        a dictionary with keys as artists and values as their track
    """
    # img = cv2.imread('south_africa.png')
    img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)

    height, width, _ = img.shape

    if ((width * height) > 1000):
        biggest_dim = height
        if (width > height):
            biggest_dim = width
        biggest_pixels = 40
        scale = int(biggest_dim / biggest_pixels)
        resized_img = cv2.resize(img, dsize=(int(width/scale), int(height/scale)), interpolation=cv2.INTER_CUBIC)
        cv2.imwrite("test_resizecv2.png", cv2.cvtColor(resized_img, cv2.COLOR_RGB2BGR))

        npimage = np.asarray(resized_img)
        #print(resized_img)
        print(npimage.shape)
    else:
        npimage = img

    perc_colour_dict = get_colour_array(npimage)

    return colours_to_playlist(perc_colour_dict, 10)

def get_colour_array(img: np.ndarray):
    """Converts an image array with rgb values to a dictionary of discrete colors.

    Parameters
    ----------
    img : np.ndarray
        The image where colour composition will be extracted from.

    Returns
    -------
    dict[str, float]
        a dictionary of colour keys where their values represent the percent composition seen in the image.
    
    #sample array to be removed later
    height = 2 # number of rows
    width = 4
    img = np.zeros((height,width,3), np.uint8)
    img[0][0] = np.array([255, 0, 0]) 
    img[0][1] = np.array([0, 0, 255])
    img[0][2] = np.array([165, 42, 42]) 
    img[0][3] = np.array([0, 100, 100])
    img[1][0] = np.array([255, 0, 0])
    img[1][1] = np.array([0, 255, 0])
    img[1][2] = np.array([161, 255, 66])
    img[1][3] = np.array([209, 28, 0])
    print(img)

    """
    print("Number of dimensions of image: ", img.ndim)
    height, width, dx = img.shape
    print("height: ", height)
    print("value of third dimension: ", dx)
    #HOW TO RESHAPE ANY IMAGE?
    newimg = img.reshape(height * width, 3)
    #print("reshaped image:", newimg)
    
    colour_count_dict = {
        "red": 0,
        "green" : 0,
        "yellow": 0,
        "blue": 0,
        "black": 0,
        "white": 0,
        "pink": 0,
        "cyan": 0,
        "orange": 0,
        "brown": 0,
        "purple": 0,
    }

    colour_redirect_to_colour_count_dict = {
        'black': 'black',
        'dark green': 'green',
        'green': 'green',
        'navy blue': 'blue',
        'dark blue': 'blue',
        'dark teal': 'cyan',
        'blue': 'blue',
        'teal': 'cyan',
        'light green': 'green',
        'light blue': 'blue',
        'cyan': 'cyan',
        'sky blue': 'blue',
        'brown': 'brown', 
        'dark purple': 'purple',
        'maroon': 'brown',
        'red': 'red',
        'dark red': 'red',
        'purple': 'purple',
        'magenta': 'pink',
        'pink': 'pink',
        'dark brown': 'brown',
        'orange': 'orange', 
        'olive': 'green',
        'gold': 'yellow',
        'mustard': 'yellow',
        'yellow': 'yellow',
        'lime green': 'green',
    }

    for x in newimg:
        r = x[0]
        g = x[1]
        b = x[2]

        (h, s, v) = colorsys.rgb_to_hsv(r, g, b)
        (r, g, b) = colorsys.hsv_to_rgb(h, 1, v)

        if (r != 0 and g != 0 and b != 0):
            print("Faulty color!!!!!!!!!!!!!!!!")

        match = "[{}, {}, {}]".format(int(r), int(g), int(b))

        if (match == '[255, 255, 255]'):
            colour_count_dict['white'] += 1
        else:
            for line in open("satfaces.txt"):
                if line.startswith(match):
                    colour = line.split("] ")[1].strip()
                    redirected_colour = colour_redirect_to_colour_count_dict[colour]
                    colour_count_dict[redirected_colour] += 1
                    break

    total_colour = sum(colour_count_dict.values())
    print("total_colours: ", total_colour)
    perc_colour_dict = {
        "red": colour_count_dict["red"]/total_colour,
        "green": colour_count_dict["green"]/total_colour,
        "yellow": colour_count_dict["yellow"]/total_colour,
        "blue": colour_count_dict["blue"]/total_colour,
        "black": colour_count_dict["black"]/total_colour,
        "white": colour_count_dict["white"]/total_colour,
        "pink": colour_count_dict["pink"]/total_colour,
        "cyan": colour_count_dict["cyan"]/total_colour,
        "orange": colour_count_dict["orange"]/total_colour,
        "brown": colour_count_dict["brown"]/total_colour,
        "purple": colour_count_dict["purple"]/total_colour,
    }
    print("colour_count_dict: ", colour_count_dict)
    print("perc_colour_dict: ", perc_colour_dict)

    return perc_colour_dict


def colours_to_playlist(perc_colour_dict: dict[str, float], playlist_size: int):
    """Converts a dictionary of weighted colours to a spotify playlist.

    Parameters
    ----------
   perc_colour_dict : dict[str, float]
        a dictionary of colour keys where their values represent the percent composition seen in the image.
    playlist_size : int
        number of songs in playlist.

    Returns
    -------
    unknown type! Need to find out.
        a playlist representing the colour distribution.
        
    """
    genre_id_dict = {
    "rock": 152,
    "country": 84,
    #"folk": 466,
    #"reggae": 144,
    "latin": 197,
    "blues": 153,
    #"jazz": 129,
    "metal": 464,
    #"gospel": 187,
    "classical": 98,
    "pop": 132,
    "electronic": 110,
    #"dance": 113,
    #"soul": 169,
    #"r-n-b": 165,
    "hip-hop": 116,
    "new age": 474,
    }

    playlist_dict = {}

    for x in perc_colour_dict:
        genre_name = COLOUR_GENRE[x]
        genre_id = genre_id_dict[genre_name]
        genre = client.get_genre(genre_id)
        radios = genre.get_radios()
        
        if (len(radios) == 0):
            print("no radio for the following genre:", genre_name)
            continue
        #define number of tracks to print
        random_radio = random.choice(radios)
        number_of_radio_tracks = 0
        try:
            radio_tracks = random_radio.get_tracks(limit=int(round(perc_colour_dict[x]*10)))
            number_of_radio_tracks = len(radio_tracks)
        except ValueError:
            print("Radio not accessible.")
        while_repeats = 0
        # print(x, ":", "genre id: ", genre_id, ".", "number of radio tracks: ",number_of_radio_tracks)
        while (number_of_radio_tracks < round(perc_colour_dict[x]*10)):
            while_repeats +=1
            if while_repeats > 100:
                break
            random_radio = random.choice(radios)
            try:
                radio_tracks = random_radio.get_tracks(limit=int(round(perc_colour_dict[x]*10)))
                number_of_radio_tracks = len(radio_tracks)
            except ValueError:
                print("Radio not accessible.")
        if round(perc_colour_dict[x]*10) != 0:
            for x in radio_tracks:
                artist = x.get_artist()
                playlist_dict[x] = artist
    print(playlist_dict)

        
    """


    print(x, ":", round(perc_colour_dict[x]*10), random_radio, radio_tracks)
    
    print(round(perc_colour_dict[x]*10))
    limit=int(round(perc_colour_dict[x]*10))
    random_radio = random.choice(radios)
    radio_tracks = random_radio.get_tracks()
    number_of_radio_tracks = len(radio_tracks)
    print(random_radio, number_of_radio_tracks)
    genre = client.get_genre(genre_id)
    radio = genre.get_radios()
    random_radio = random.choice(radio)
    radio_tracks = random_radio.get_tracks()
    number_of_radio_tracks = len(radio_tracks)
    print(random_radio, number_of_radio_tracks)
    
    genre = client.get_genre(genre_id)
    radio = genre.get_radios()
    random_radio = random.choice(radio)
    radio_tracks = random_radio.get_tracks()
    number_of_radio_tracks = len(radio_tracks)
    while (number_of_radio_tracks < 10):
        random_radio = random.choice(radio)
        radio_tracks = random_radio.get_tracks()
        number_of_radio_tracks = len(radio_tracks)
        random_radio_tracks = random.choice(radio_tracks)
        final_tracks = random_radio_tracks.get_tracks()
        print(final_tracks)
    """
    """
    genre_id = genre_id_dict[genre]
    artists = genre.get_artists()
    print(artists)
        
    genre = client.get_genre(197)
    radio = genre.get_radios()
    random_radio = random.choice(radio)
    radio_tracks = random_radio.get_tracks()
    print(radio_tracks)
    """


    return playlist_dict


img = cv2.imread('south_africa.png')
img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)

print(type(img))
print("test")
print(img.shape)
print(type(img.shape))

height, width, _ = img.shape

if ((width * height) > 1000):
    biggest_dim = height
    if (width > height):
        biggest_dim = width
    biggest_pixels = 40
    scale = int(biggest_dim / biggest_pixels)
    resized_img = cv2.resize(img, dsize=(int(width/scale), int(height/scale)), interpolation=cv2.INTER_CUBIC)
    cv2.imwrite("test_resizecv2.png", cv2.cvtColor(resized_img, cv2.COLOR_RGB2BGR))

    npimage = np.asarray(resized_img)
    #print(resized_img)
    print(npimage.shape)
else:
    npimage = img

perc_colour_dict = get_colour_array(npimage)

colours_to_playlist(perc_colour_dict, 10)

"""
npimg = np.fromstring(filestr, np.uint8)
img = cv2.imdecode(npimg, cv2.IMREAD_UNCHANGED)
"""