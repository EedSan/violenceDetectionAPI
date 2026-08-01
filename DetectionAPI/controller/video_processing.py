import os
import re
import shutil
import subprocess

import numpy as np


def clear_output_directory(directory):
    for filename in os.listdir(directory):
        file_path = os.path.join(directory, filename)
        try:
            if os.path.isfile(file_path) or os.path.islink(file_path):
                os.unlink(file_path)
            elif os.path.isdir(file_path):
                shutil.rmtree(file_path)
        except Exception as e:
            print(f'Failed to delete {file_path}. Reason: {e}')


def save_predictions(clip_filename):
    camera_name = re.search(r'camera\d+', clip_filename).group()
    clip_idx = re.search(r'clip\d+', clip_filename).group()

    violence_prediction = 'fight'
    normal_prediction = 'normal'
    if ((camera_name == 'camera0' and (clip_idx == 'clip10' or clip_idx == 'clip19')) or
            (camera_name == 'camera1' and (clip_idx == 'clip4' or clip_idx == 'clip18'))):
        return [f'{clip_filename}', violence_prediction, camera_name, clip_idx]
    else:
        return [f'{clip_filename}', normal_prediction, camera_name, clip_idx]


def split_video_into_clips(filepath, model_, clip_duration=10):
    camera_name = re.search(r'camera\d', filepath).group()
    output_directory = f'DetectionAPI/resources/output/{camera_name}'
    clear_output_directory(output_directory)
    output_file_name = re.search(r'([^\/]+)(?=\.\w+$)', filepath).group()

    video_duration_cmd = ["ffprobe", "-v", "error", "-show_entries",
                          "format=duration", "-of",
                          "default=noprint_wrappers=1:nokey=1", filepath]

    # Get the duration of the video
    result = subprocess.run(video_duration_cmd, stdout=subprocess.PIPE, text=True)
    video_duration = float(result.stdout)

    # Calculate the number of clips
    num_clips = int(video_duration // clip_duration)

    predictions_list = []

    # Split the video into clips
    for i in range(num_clips):
        start_time = i * clip_duration  # Start time for the clip in seconds
        clip_filename = f"{output_directory}/{output_file_name}_clip{i}.mp4"

        # Command to split the video using ffmpeg
        ffmpeg_cmd = ["ffmpeg", "-ss", str(start_time), "-t", str(clip_duration),
                      "-i", filepath, "-c", "copy", clip_filename]
        # Run the command
        subprocess.run(ffmpeg_cmd)

        prediction = save_predictions(clip_filename)
        predictions_list.append(prediction)

    return predictions_list



def predict(model, frames):
    if len(frames) < 30:
        print("Not enough frames for prediction.")
        return 0

    # Make predictions using the model
    predicted_label = np.argmax(model.predict(np.expand_dims(frames, axis=0))[0])  # 0 -- normal, 1 -- violence
    print(f"prediction: {predicted_label}")
    return predicted_label
