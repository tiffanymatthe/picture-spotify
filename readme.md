# Picture Spotify

## How to Run

1. Clone repository.
2. Set up a virtual environment in directory by following the steps outlined in "Create a project environment for the Flask tutorial" from [VS Code](https://code.visualstudio.com/docs/python/tutorial-flask#_create-a-project-environment-for-the-flask-tutorial).
3. Activate virtual environment by running "Terminal: Create New Integrated Terminal" (``Ctrl+Shift+` ``) from Command Palette.
4. Run `pip install -r requirements.txt` to install requirements.
5. Add environment variable FLASK_APP=webapp. In Windows command terminal, run `setx FLASK_APP webapp`.
6. `cd web_app` to go into web_app folder and run `python -m flask run` in Integrated Terminal.
7. View website at http://127.0.0.1:5000/.

- For better development, create a code snippet by following the steps [here](https://code.visualstudio.com/docs/python/tutorial-flask#_create-multiple-templates-that-extend-a-base-template).

## To Do List
- [ ] Extract discrete colour composition from a photo.
- [ ] Show a playlist with ability to save after submitting photo.
- [ ] Create playlist with Spotipy.
- [ ] Add ability to login in to Spotify when user wants to save playlist.
- [ ] Extract random song in genre associated with colour.
- [ ] Make POST redirect to correct page and show playlist.
- [ ] Create interface with Bulma.
- [ ] Deploy as a Heroku app.