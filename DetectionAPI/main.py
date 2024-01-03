import os
from itertools import chain

import requests
from flask import Flask, request, jsonify
import pandas as pd

from model import create_LRCN_model
from controller.video_processing import split_video_into_clips

app = Flask(__name__)

sequence_length = 30
image_height, image_width = 128, 128
classes_list = ['normal', 'fights']
model = create_LRCN_model(sequence_length, image_height, image_width, classes_list)
model.load_weights('DetectionAPI/resources/best_weights.h5')

global_predictions_list = []


@app.route('/upload', methods=['POST'])
def upload_video():
    file_path = request.form['video']
    if os.path.exists(file_path):
        print(f"Received video from {file_path}")
        all_clips_predictions_list = split_video_into_clips(file_path, model)
        global_predictions_list.append(all_clips_predictions_list)
        return jsonify({"message": "Video loaded successfully"}), 200
    else:
        return jsonify({"error": "File not found"}), 404


@app.route('/get_notifications', methods=['GET'])
def get_notification():
    try:
        list_to_df = list(chain.from_iterable(global_predictions_list))
        df = pd.DataFrame(list_to_df, columns=['clip_path', 'prediction', 'camera_name', 'clip_idx'])
        return jsonify(df.to_dict(orient='records')), 200
    except Exception as e:
        print(f'Failed get Notification {e}')
        return jsonify(e), 200



@app.route('/', methods=['GET'])
def connect():
    return 'Connected', 200


if __name__ == '__main__':
    app.run(port=8000, debug=True)
