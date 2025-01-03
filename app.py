from flask import Flask, render_template, request, redirect, url_for
import os
import cv2
import numpy as np
from werkzeug.utils import secure_filename

# Import utility functions
from utils.detect_orientation import detect_batsman_orientation
from utils.track_ball import track_ball_trajectory
from utils.recommend_shot import recommend_shot

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'static/uploads/'
app.config['ALLOWED_EXTENSIONS'] = {'mp4', 'avi', 'mov'}

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in app.config['ALLOWED_EXTENSIONS']

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/upload', methods=['POST'])
def upload_video():
    if 'video' not in request.files:
        return redirect(request.url)
    file = request.files['video']
    if file.filename == '':
        return redirect(request.url)
    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(filepath)

        # Process the video
        orientation = detect_batsman_orientation(filepath)
        ball_trajectory = track_ball_trajectory(filepath)
        shot = recommend_shot(orientation, ball_trajectory)

        return render_template('result.html', orientation=orientation, shot=shot)
    else:
        return redirect(request.url)

if __name__ == '__main__':
    if not os.path.exists(app.config['UPLOAD_FOLDER']):
        os.makedirs(app.config['UPLOAD_FOLDER'])
    app.run(debug=True)
