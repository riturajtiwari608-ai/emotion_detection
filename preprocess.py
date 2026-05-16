import numpy as np
import pandas as pd

def load_data(csv_path):
    data = pd.read_csv(csv_path)

    pixels = data['pixels'].tolist()
    faces = []

    for pixel_sequence in pixels:
        face = [int(pixel) for pixel in pixel_sequence.split(' ')]
        face = np.array(face).reshape(48, 48)
        faces.append(face)

    faces = np.array(faces)
    faces = faces / 255.0

    faces = faces.reshape(-1, 48, 48, 1)

    emotions = pd.get_dummies(data['emotion']).values

    return faces, emotions