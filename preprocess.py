import pandas as pd
import numpy as np

def load_data():
    df1 = pd.read_csv("dataset/fer2013_part1.csv")
    df2 = pd.read_csv("dataset/fer2013_part2.csv")
    df3 = pd.read_csv("dataset/fer2013_part3.csv")

    data = pd.concat([df1, df2, df3], ignore_index=True)

    pixels = data['pixels'].tolist()
    faces = []

    for pixel_sequence in pixels:
        face = [int(pixel) for pixel in pixel_sequence.split()]
        face = np.array(face).reshape(48, 48)
        faces.append(face)

    faces = np.array(faces, dtype="float32")
    faces /= 255.0

    faces = faces.reshape(-1, 48, 48, 1)

    emotions = pd.get_dummies(data['emotion']).values

    return faces, emotions