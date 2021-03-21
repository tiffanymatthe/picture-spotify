import cv2
import numpy as np
import sys
from math import sqrt, pow
import sys, colorsys

import spotipy
import os
from spotipy.oauth2 import SpotifyClientCredentials
from spotipy.oauth2 import SpotifyOAuth
from PIL import Image

import deezer
client = deezer.Client()

auth_manager = SpotifyClientCredentials()
sp = spotipy.Spotify(auth_manager=auth_manager)

"""
npimg = np.fromstring(filestr, np.uint8)
img = cv2.imdecode(npimg, cv2.IMREAD_UNCHANGED)
"""

# add colour-genre dictionary as a constant here
COLOUR_GENRE = {
    "red" : "Rock",
    "green" : ["Country", "Folk"],
    "yellow" : ["Reggae", "Latin"],
    "blue" : ["Blues", "Jazz"],
    "black" : "Metal",
    "white" : ["Gospel", "Classical"],
    "pink": "Pop",
    "cyan" : ["Electronic", "Dance"],
    #"grey" : "Other",
    "orange" : ["Soul", "r-n-b", "funk", "Hip-Hop"],
    "brown" : "World Music",
    "purple" : "New Age",
}

#basic colour dictionary
basic_colors = {
    "red" : [255, 0, 0],
    "green" : [0, 255, 0],
    "yellow" : [255, 255, 0],
    "blue" : [0, 0, 255],
    "black" : [0, 0, 0],
    "white" : [255, 255, 255],
    "pink": [255, 182, 193],
    "cyan" : [0, 255, 255],
    #"grey" : [128,128,128],
    "orange" : [255, 128, 0],
    "brown" : [165 ,42, 42],
    "purple" : [128, 0, 128],   
}

# finding distance between any x and dictionary of colours
def distance_3d(rgb_1, rgb_2):
    return sqrt(pow(rgb_1[0] - rgb_2[0], 2)+
                pow(rgb_1[1] - rgb_2[1], 2)+
                pow(rgb_1[2] - rgb_2[2], 2))

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
    height = 10
    width = 4
    img = np.zeros((height,width,3), np.uint8)
    # colour_array = get_colour_array(img)
    playlist_size = 10
    # return colours_to_playlist(colour_array, playlist_size)
    return {
        'Tove Lo': 'Habits (Stay High)',
        'Julia Michaels': 'Issues',
        'Astrid S': 'It\'s Ok If You Forget Me'
    }

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
    

    print("reshaped image:", newimg)
    
    colour_count_dict = {
        "red": 0,
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
    """
    for x in newimg:
        distance_from_red = distance_3d(x, basic_colors["red"])
        distance_from_green = distance_3d(x, basic_colors["green"])
        distance_from_yellow = distance_3d(x, basic_colors["yellow"])
        distance_from_blue = distance_3d(x, basic_colors["blue"])
        distance_from_black = distance_3d(x, basic_colors["black"])
        distance_from_white = distance_3d(x, basic_colors["white"])
        distance_from_pink = distance_3d(x, basic_colors["pink"])
        distance_from_cyan = distance_3d(x, basic_colors["cyan"])
        distance_from_orange = distance_3d(x, basic_colors["orange"])
        distance_from_brown = distance_3d(x, basic_colors["brown"])
        distance_from_purple = distance_3d(x, basic_colors["purple"])

        distance_dict = {
            "red": distance_from_red,
            "yellow": distance_from_yellow,
            "blue": distance_from_blue,
            "black": distance_from_black,
            "white": distance_from_white,
            "pink": distance_from_pink,
            "cyan": distance_from_cyan,
            "orange": distance_from_orange,
            "brown": distance_from_brown,
            "purple": distance_from_purple,
        }

        min_colour_dist = min(distance_dict.values())
        min_colour_key_list = [key for key in distance_dict if distance_dict[key] == min_colour_dist]
        min_colour_key = min_colour_key_list[0]
        
    for x in newimg:
        r = x[0]
        g = x[1]
        b = x[2]
        match = "[{}, {}, {}]".format(int(r), int(g), int(b))

        for line in open("satfaces.txt"):
            if line.startswith(match):
                print("You were thinking of: " + line.split("] ")[1].strip())
                break
              
        
    colour_count_dict[min_colour_key] += 1

    total_colour = sum(colour_count_dict.values())
    perc_colour_dict = {
        "red": colour_count_dict["red"]/total_colour,
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
    """
    return 0


def colours_to_playlist(colour_array: dict[str, float], playlist_size: int):
    """Converts a dictionary of weighted colours to a spotify playlist.

    Parameters
    ----------
    colour_array : dict[str, float]
        a dictionary of colour keys where their values represent the percent composition seen in the image.
    playlist_size : int
        number of songs in playlist.

    Returns
    -------
    unknown type! Need to find out.
        a playlist representing the colour distribution.
        
    """

    genre = client.get_genre(113)

    artists = genre.get_artists()

    tracks = artists[1].get_top()

    print(tracks)
    return 0


img = cv2.imread('red_1px.png')
img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)

print(type(img))
print("test")
print(img.shape)
print(type(img.shape))

height, width, _ = img.shape

if ((width * height) > 1000):
    resized_img = cv2.resize(img, dsize=(54, 140), interpolation=cv2.INTER_CUBIC)
    npimage = np.asarray(resized_img)
    print(resized_img)
else:
    npimage = img

get_colour_array(npimage)
