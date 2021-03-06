import cv2
import numpy as np
import sys
from math import sqrt, pow
import sys
import colorsys
import random
from PIL import Image
import deezer
from pathlib import Path
import os

client = deezer.Client()

# Colours and their associated music genre. Based off "Associaing Colours with Musical Genres" by Jukka Holm , Antti Aaltonen & Harri Siirtola.
COLOUR_GENRE = {
    "red": "rock",
    "green": "country",
    "yellow": "latin",
    "blue": "blues",
    "black": "metal",
    "white": "classical",
    "pink": "pop",
    "cyan": "electronic",
    "orange": "hip-hop",
    "brown": "country",
    "purple": "new age",
}


def get_playlist(img: np.ndarray) -> dict[str, str]:
    """Converts an image array with BGR values to a playlist
    Parameters
    ----------
    img : np.ndarray
        The image where colour composition will be extracted from. In BGR. Of size height x width x 3
    Returns
    -------
    dict [str, str]
        a dictionary with keys as artists and values as their track. Maximum size is 15.
    """
    scaled_img = np.float32(np.true_divide(img, 255.0))
    img = cv2.cvtColor(scaled_img, cv2.COLOR_BGR2RGB)
    height, width, _ = img.shape

    if ((width * height) > 1000):
        biggest_dim = height
        if (width > height):
            biggest_dim = width
        biggest_pixels = 40
        scale = int(biggest_dim / biggest_pixels)
        resized_img = cv2.resize(img, dsize=(
            int(width/scale), int(height/scale)), interpolation=cv2.INTER_CUBIC)
        npimage = np.asarray(resized_img)
        print(npimage.shape)
    else:
        npimage = img

    rgb_img = npimage * 255
    rgb_img[rgb_img > 255] = 255
    rgb_img[rgb_img < 0] = 0

    perc_colour_dict = get_colour_array(rgb_img)

    return colours_to_playlist(perc_colour_dict, 15)


def get_colour_array(img: np.ndarray) -> dict[str, float]:
    """Converts an image array with rgb values to a dictionary of discrete colors.
    Parameters
    ----------
    img : np.ndarray
        The image where colour composition will be extracted from.
    Returns
    -------
    dict[str, float]
        a dictionary of colour keys where their values represent the percent composition seen in the image.
    """
    height, width, dx = img.shape
    newimg = img.reshape(height * width, 3)

    colour_count_dict = {
        "red": 0,
        "green": 0,
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

    any_colour_to_main_colour = {
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

    rgb_colours = {}
    
    __location__ = os.path.realpath(os.path.join(os.getcwd(), os.path.dirname(__file__)))
    path = os.path.join(__location__, "static", "satfaces.txt")
    for line in open(path):
        split_line = line.split("] ")
        rgb_value = split_line[0] + ']'
        colour = split_line[1].strip()
        rgb_colours[rgb_value] = colour

    for x in newimg:
        r = x[0]
        g = x[1]
        b = x[2]

        (h, s, v) = colorsys.rgb_to_hsv(r, g, b)
        (r, g, b) = colorsys.hsv_to_rgb(h, 1, v)

        if (r != 0 and g != 0 and b != 0):
            print("Faulty color!")

        match = "[{}, {}, {}]".format(int(r), int(g), int(b))

        if (match == '[255, 255, 255]'):
            colour_count_dict['white'] += 1
        else:
            colour = rgb_colours[match]
            redirected_colour = any_colour_to_main_colour[colour]
            colour_count_dict[redirected_colour] += 1

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


def colours_to_playlist(perc_colour_dict: dict[str, float], playlist_size: int) -> dict[str, str]:
    """Converts a dictionary of weighted colours to a spotify playlist.
    Parameters
    ----------
   perc_colour_dict : dict[str, float]
        a dictionary of colour keys where their values represent the percent composition seen in the image.
    playlist_size : int
        maximum number of songs in playlist.
    Returns
    -------
    dict [str, str]
        a dictionary with keys as artists and values as their track. Maximum size is playlist_size. Represents colour distribution.
    """
    genre_id_dict = {
        "rock": 152,
        "country": 84,
        "latin": 197,
        "blues": 153,
        "metal": 464,
        "classical": 98,
        "pop": 132,
        "electronic": 110,
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
        # define number of tracks to print
        random_radio = random.choice(radios)
        number_of_radio_tracks = 0
        try:
            radio_tracks = random_radio.get_tracks(
                limit=int(round(perc_colour_dict[x]*15)))
            number_of_radio_tracks = len(radio_tracks)
        except ValueError:
            print("Radio not accessible.")
        while_repeats = 0
        while (number_of_radio_tracks < round(perc_colour_dict[x]*15)):
            while_repeats += 1
            if while_repeats > 100:
                break
            random_radio = random.choice(radios)
            try:
                radio_tracks = random_radio.get_tracks(
                    limit=int(round(perc_colour_dict[x]*15)))
                number_of_radio_tracks = len(radio_tracks)
            except ValueError:
                print("Radio not accessible.")
        if round(perc_colour_dict[x]*15) != 0:
            for x in radio_tracks:
                artist = x.get_artist().name
                playlist_dict[x.title] = artist
    print(playlist_dict)

    return playlist_dict