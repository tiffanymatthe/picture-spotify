import cv2
import numpy as np

# add color-genre dictionary as a constant here
COLOUR_GENRE = {
    "red" : "pop",
    "blue" : "rock"
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