import os
import sys
from datetime import datetime

import cv2
import numpy as np
import spotipy
from flask import Flask, flash, redirect, render_template, request, url_for
from spotipy import oauth2
from werkzeug.utils import secure_filename

import web_app.process_image as primg

from . import app

SPOTIPY_CLIENT_ID = '***REMOVED***'
SPOTIPY_CLIENT_SECRET = '***REMOVED***'
SPOTIPY_REDIRECT_URI = 'http://127.0.0.1:5000/connect'
SCOPE = 'playlist-modify-private'
CACHE = '.spotipyoauthcache'

sp_oauth = oauth2.SpotifyOAuth( SPOTIPY_CLIENT_ID, SPOTIPY_CLIENT_SECRET,SPOTIPY_REDIRECT_URI,scope=SCOPE,cache_path=CACHE )

@app.route("/about/")
def about():
    return render_template("about.html")


@app.route("/contact/")
def contact():
    return render_template("contact.html")


@app.route("/hello/")
@app.route("/hello/<name>")
def hello_there(name=None):
    return render_template(
        "hello_there.html",
        name=name,
        date=datetime.now()
    )


@app.route("/api/data")
def get_data():
    return app.send_static_file("data.json")


ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}


def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/playlist')
def playlist():
        results = sp.current_user_saved_tracks()
        for idx, item in enumerate(results['items']):
            track = item['track']
            print(idx, track['artists'][0]['name'], " – ", track['name'])
        return render_template("playlist.html")

@app.route('/connect', methods=['GET', 'POST'])
def connect():
    access_token = ""
    token_info = sp_oauth.get_cached_token()

    if token_info:
        print("Found cached token!")
        access_token = token_info['access_token']
    else:
        url = request.url
        code = sp_oauth.parse_response_code(url)
        if code and code != "http://127.0.0.1:5000/connect":
            print("Found Spotify auth code in Request URL! Trying to get valid access token...")
            token_info = sp_oauth.get_access_token(code)
            access_token = token_info['access_token']

    if access_token:
        print("Access token available! Trying to get user information...")
        sp = spotipy.Spotify(access_token)
        # results = sp.current_user()
        return sp.current_user_playlists()
    else:
        return htmlForLoginButton()
    

def htmlForLoginButton():
    auth_url = getSPOauthURI()
    htmlLoginButton = "<a href='" + auth_url + "'>Login to Spotify</a>"
    return htmlLoginButton

def getSPOauthURI():
    auth_url = sp_oauth.get_authorize_url()
    return auth_url

    scope = "playlist-modify-private"
    if request.method == 'POST':
        sp = spotipy.Spotify(auth_manager=SpotifyOAuth(scope=scope))

    return render_template("connect.html")

@app.route('/', methods=['GET', 'POST'])
def home():
    if request.method == 'POST':
        # check if the post request has the file part
        if 'file' not in request.files:
            flash('No file part')
            return redirect(request.url)
        file = request.files['file']
        filetype = type(file) # fileStorage type. Need to convert to color array
        # if user does not select file, browser also
        # submit an empty part without filename
        if file.filename == '':
            flash('No selected file')
            return redirect(request.url)
        if file and allowed_file(file.filename):
            filestr = file.read()
            npimg = np.fromstring(filestr, np.uint8)
            img = cv2.imdecode(npimg, cv2.IMREAD_UNCHANGED)
            primg.get_playlist(img)
            # this need to change to sending file to python module and spitting out playlist
            # filename = secure_filename(file.filename)
            # file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            # return redirect(url_for('uploaded_file',
            # filename=filename))
    return render_template("home.html")
