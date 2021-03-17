import cv2
import numpy as np

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

def get_playlist(img: np.ndarray):
    """Converts an image array with rgb values to a playlist

    Parameters
    ----------
    img : np.ndarray
        The image where colour composition will be extracted from.

    Returns
    -------
    unknown type! Need to find out. I think it is JSON. (so a string)
        a playlist representing the color distribution.
    """
    height = 10
    width = 4
    img = np.zeros((height,width,3), np.uint8) # white image
    colour_array = get_colour_array(img)
    playlist_size = 10
    return colours_to_playlist(colour_array, playlist_size)

def get_colour_array(img: np.ndarray):
    # Reshape img array into 1 x number of elements x 3
    reshaped_img = img.reshape()

    for
    # iterate (for-loop) over each color of array and classify color by looking at rgb values.
    d = dict(enumerate(img.flatten(), 1))

    for color in reshaped_img:
        # classify color
        color[0] ==sgs

    red_count = 0

    for color in list:
        if (color[0] > 200 && < 255) {
            if (color[1] >0 && < 50) {
                red_coumt = red_count + 1
            }
        }

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
    red_percentage = 0.1

    diction = {
        "red": red_percentage,
        "blue": 0.9
    }
    return diction

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
    """
    return 0

"""
# Online Python compiler (interpreter) to run Python online.
# Write Python 3 code in this online editor and run it.
import numpy as np

print("Hello world")

height = 2 # number of rows
width = 4
img = np.zeros((height,width,3), np.uint8)
img[0][0] = np.array([0, 0, 0]) #black
img[0][1] = np.array([0, 0, 255]) #blue
img[0][2] = np.array([165, 42, 42]) #brown
img[0][3] = np.array([0, 100, 100]) #cyan
img[1][0] = np.array([255, 0, 0]) #red
img[1][1] = np.array([0, 255, 0]) #green
img[1][2] = np.array([161, 255, 66]) #shade of green
img[1][3] = np.array([209, 28, 0]) #shade of red

print(img)

newimg = img.reshape(8,3)

print(newimg)

for x in newimg:
    red_colour = x[0]
    green_colour = x[1]
    blue_colour = x[2]
    
    red_count = 0
    green_count = 0
    blue_count = 0
    
    if (red_colour > 150):
        if (green_colour < 50):
            if(blue_colour < 50):
                print(red_count + 1)

"""