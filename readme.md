# Picture Spotify

## How to Run
1. Clone repository.
2. Set up a virtual environment in directory by following the steps outlined in "Create a project environment for the Flask tutorial" from [VS Code](https://code.visualstudio.com/docs/python/tutorial-flask#_create-a-project-environment-for-the-flask-tutorial).
3. Activate virtual environment by running "Terminal: Create New Integrated Terminal" (Ctrl+Shift+`) from Command Palette.
4. Run `pip install -r requirements.txt` to install requirements.
5. Add environment variable FLASK_APP=webapp. In Windows command terminal, run `setx FLASK_APP webapp`.
6. `cd` into webapp folder and run `python -m flask run` in Integrated Terminal.
7. View website at http://127.0.0.1:5000/.

* For better development, create a code snippet by following the steps [here](https://code.visualstudio.com/docs/python/tutorial-flask#_create-multiple-templates-that-extend-a-base-template).