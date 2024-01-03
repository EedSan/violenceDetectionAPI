import cv2
import numpy as np


def split_video_into_clips(filepath, model_, clip_duration=10, nn_input_shape=(128, 128)):
    cap = cv2.VideoCapture(filepath)

    # Get frame rate
    fps = cap.get(cv2.CAP_PROP_FPS)

    # Calculate the number of frames per clip
    frames_per_clip = int(clip_duration * fps)

    target_frames_count = 30

    # Read and process the video in chunks
    while True:
        frames = []
        for _ in range(frames_per_clip):

            ret, frame = cap.read()
            if not ret:
                break
            resized_frame = cv2.resize(frame, nn_input_shape)
            normalized_frame = resized_frame / 255
            frames.append(normalized_frame)

        idx = np.round(np.linspace(0, np.array(frames).shape[0] - 1, target_frames_count, endpoint=True)).astype(int)

        if frames:
            prediction = predict(model_, frames[idx])
        else:
            break
    cap.release()


def predict(model, frames):
    if len(frames) < 30:
        print("Not enough frames for prediction.")
        return 0

    # Make predictions using the model
    predicted_label = np.argmax(model.predict(np.expand_dims(frames, axis=0))[0])  # 0 -- normal, 1 -- violence
    print(f"prediction: {predicted_label}")
    return predicted_label
