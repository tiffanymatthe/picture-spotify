import cv2
import numpy as np
import sys
from math import sqrt, pow

import spotipy
import os
from spotipy.oauth2 import SpotifyClientCredentials
from spotipy.oauth2 import SpotifyOAuth
from PIL import Image


auth_manager = SpotifyClientCredentials()
sp = spotipy.Spotify(auth_manager=auth_manager)

# img  = Image.open("red.png").convert('RGB')
# img.show()
# npimage = np.asarray(img)

"""
npimg = np.fromstring(filestr, np.uint8)
img = cv2.imdecode(npimg, cv2.IMREAD_UNCHANGED)
"""

# add color-genre dictionary as a constant here
COLOUR_GENRE = {
    "black": "Metal",
    "blue": "Blues",
    "brown": "Country",
    "cyan": "Electronica and Dance",
    "orange": "Reggae",
    "pink": "Pop",
    "purple": "Gospel",
    "red": "Rock",
    "white": "Gospel",
    "yellow": "Latin",
}

#basic colour dictionary
basic_colors = {
    "black" : [0, 0, 0],
    "white" : [255, 255, 255],
    "red" : [255, 0, 0],
    "orange" : [255, 128, 0],
    "yellow" : [255, 255, 0],
    "chartreuse" : [128, 255, 0],
    "green" : [0, 255, 0],
    "spring green" : [0, 255, 128],
    "cyan" : [0, 255, 255],
    "azure" : [0, 128, 255],
    "blue" : [0, 0, 255],
}

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
    #img = np.zeros((height,width,3), np.uint8) # white image
    #colour_array = get_colour_array(img)
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
    print(img.ndim)
    height, width, dx = img.shape
    print(height)
    print(dx)
    #HOW TO RESHAPE ANY IMAGE?
    newimg = img.reshape(height * width, 3)
    

    print(newimg)

    red_count = 0
    green_count = 0
    blue_count = 0
    other = 0

    for x in newimg:
        print("color_name: " + str(distance_3d(x, basic_colors["yellow"])))
    """
    for x in newimg:
        red_colour = x[0]
        green_colour = x[1]
        blue_colour = x[2]

        if (red_colour > green_colour and red_colour > blue_colour):
            red_count += 1        
        elif (green_colour > red_colour and green_colour > blue_colour):
            green_count += 1
        elif (blue_colour > red_colour and blue_colour > green_colour):
            blue_count += 1
        else:
            other += 1

    total_colour = red_count + green_count + blue_count + other

    red_perc = red_count/total_colour
    green_perc = green_count/total_colour
    blue_perc = blue_count/total_colour
    other_perc = other/total_colour

    colour_dict = {
        "red_compo": red_perc,
        "green_compo": green_perc,
        "blue_compo": blue_perc,
        "other_compo": other_perc,
    }

    print(colour_dict)
    return colour_dict
    """

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
        a playlist representing the color distribution.
        

img = np.zeros((10,5,3), np.uint8)
get_colour_array(img)
print("Hello")
    """
    # search for top 3 songs of each artist on spotify
    # classify the tracks under their respective genres
    # this gives me a database of some kind of songs
    # then I assign each colour percentage to a proportion of songs
    # randomly select songs from database based on percentages
    # return a playlist song list
    return 0

#get_colour_array(npimage)