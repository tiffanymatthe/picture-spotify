import json
import os
import secrets
import string
import sys
from datetime import datetime
from urllib.parse import urlencode

import cv2
import numpy as np
from flask import (Flask, flash, make_response, redirect, render_template,
                   request, session, url_for)
from spotipy import oauth2
from werkzeug.utils import secure_filename

import web_app.process_image as primg

from web_app import app

REDIRECT_URI = 'https://picture-spotify-app.herokuapp.com/add_playlist_result'
AUTH_URL = 'https://accounts.spotify.com/authorize'

app.config.update(SECRET_KEY=os.environ['SECRET_KEY'])

@app.route('/', methods=['GET', 'POST'])
def home():
    if request.referrer is not None and "add_playlist_result" in request.referrer:
        [session.pop(key) for key in list(session.keys())]
    artist_track = {}
    if request.method == 'POST':
        if request.form.get('save_playlist'):
            if session.get('file_added') is None:
                return render_template("home.html", success="No file added yet!", error=True, fileAdded=False, artist_track=artist_track)
            elif request.form.get('playlist_name') is None or str.strip(request.form.get('playlist_name')) == "":
                return render_template("home.html", success="Playlist name is empty.", artist_track=artist_track, error=True, fileAdded=True)
            else:
                session['playlist_name'] = str.strip(request.form.get('playlist_name'))
                return redirect(url_for('auth'))
        # check if the post request has the file part
        if 'file' not in request.files:
            flash('No file part')
            session.pop('file_added', None)
            return render_template("home.html", success="File not added.", artist_track=artist_track, error=True, fileAdded=False)
        file = request.files['file']
        filetype = type(file) # fileStorage type. Need to convert to color array
        # if user does not select file, browser also
        # submit an empty part without filename
        if file.filename == '':
            flash('No selected file')
            session.pop('file_added', None)
            return render_template("home.html", success="File not added.", artist_track=artist_track, error=True, fileAdded=False)
        if file and allowed_file(file.filename):
            filestr = file.read()
            npimg = np.fromstring(filestr, np.uint8)
            img = cv2.imdecode(npimg, cv2.IMREAD_UNCHANGED)
            artist_track = primg.get_playlist(img)
            session['file_added'] = 'true'
            # this need to change to sending file to python module and spitting out playlist
            # filename = secure_filename(file.filename)
            # file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            # return redirect(url_for('uploaded_file',
            # filename=filename))
            session['artist_track'] = artist_track
            return render_template("home.html", artist_track=artist_track, fileAdded=True)
    return render_template("home.html", artist_track=artist_track, fileAdded=False)

@app.route("/about/")
def about():
    return render_template("about.html")


@app.route("/contact/")
def contact():
    return render_template("contact.html")


@app.route("/auth")
def auth():
    # Request authorization from user
    payload = {
        'client_id': os.environ['SPOTIPY_CLIENT_ID'],
        'response_type': 'token',
        'redirect_uri': REDIRECT_URI,
        'scope': 'playlist-modify-private',
    }

    res = make_response(redirect(f'{AUTH_URL}/?{urlencode(payload)}'))

    return res

@app.route('/add_playlist_result')
def connect():
    error = request.args.get('error')
    state = request.args.get('state')

    if error:
        print("ERROR")

    artist_track = session['artist_track']
    playlist_name = session['playlist_name']
    return render_template("add_playlist_result.html", artist_track=artist_track, playlist_name=playlist_name)

ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS
