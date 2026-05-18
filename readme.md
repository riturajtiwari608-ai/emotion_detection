# AI Emotion Detection

A lightweight emotion detection project that trains a convolutional neural network on the FER2013-style dataset and detects emotions from a webcam feed. The repository includes scripts for data preprocessing, training, realtime webcam detection (CLI), a Flask-based web streamer, and a PyQt6 desktop GUI.

Supported emotions:
- Angry, Disgust, Fear, Happy, Sad, Surprise, Neutral

## Table of Contents
- [Repository Structure](#repository-structure)
- [Features](#features)
- [Requirements](#requirements)
- [Quick Start](#quick-start)
  - [1. Prepare dataset](#1-prepare-dataset)
  - [2. Train model](#2-train-model)
  - [3. Run detection (CLI)](#3-run-detection-cli)
  - [4. Run Flask web app](#4-run-flask-web-app)
  - [5. Run desktop GUI](#5-run-desktop-gui)
  - [6. Frontend (React)](#6-frontend-react)
- [Notes & Troubleshooting](#notes--troubleshooting)
- [Contributing](#contributing)
- [License](#license)
- [Contact](#contact)

## Repository Structure
- `app.py` — Flask application that streams webcam frames and overlays predicted emotion.
- `detect.py` — Simple CLI webcam emotion detector using OpenCV window.
- `gui.py` — PyQt6 desktop application with live video and animated background.
- `train.py` — Training script that builds a small CNN and saves the trained model to `model/emotion_model.h5`.
- `preprocess.py` — Loads and preprocesses the dataset (`dataset/fer2013.csv`) into numpy arrays.
- `model/` — Directory for saving/loading the trained model (contains `emotion_model.h5` after training).
- `dataset/fer2013.csv` — Expected dataset file used by `preprocess.py` and `train.py`.
- `haarcascade_frontalface_default.xml` — Haar cascade for face detection (included).
- `frontend/` — React frontend scaffold (Create React App) for a web UI (if used).
- `.gitignore`, `.gitattributes`, etc.

## Features
- Preprocessing of FER2013-style pixel data.
- Trainable CNN classifier (7-class softmax output).
- Realtime webcam emotion detection with bounding box and label.
- Flask server to stream processed video frames to a browser.
- Polished PyQt6 GUI with animated background and live emotion label.
- Frontend scaffold for future web UI integration.

## Requirements
General:
- Python 3.8+
- git, camera/webcam access

Python packages (install in a virtualenv):
- numpy
- pandas
- opencv-python
- tensorflow (or tensorflow-cpu / tensorflow-gpu as appropriate)
- flask
- pyqt6 (for GUI)
- (optional) matplotlib (if you plan to visualize results)

Frontend (if using):
- Node.js v14+ and npm
- Dependencies listed in `frontend/package.json`

Install example:
pip install -r requirements.txt
(There is no `requirements.txt` in the repo by default; create one with the packages above to simplify installs.)

## Quick Start

1) Prepare dataset
- Place a FER2013-style CSV at `dataset/fer2013.csv`. `preprocess.py` expects the CSV to include a `pixels` column (space-separated grayscale pixels for 48x48) and an `emotion` column with integer labels.
- Example: the common FER2013 dataset.

2) Train the model
- Train using:
  python train.py
- The script loads data with `preprocess.load_data()`, trains for 10 epochs (default), and saves the model to `model/emotion_model.h5`.
- Adjust hyperparameters in `train.py` as needed (epochs, batch size, architecture).

3) Run detection (CLI)
- Ensure `model/emotion_model.h5` exists (either by training locally or downloading a pretrained model).
- Run:
  python detect.py
- A window titled "Emotion Detector" will open and show bounding boxes and predicted emotion for each detected face.
- Press `q` to quit.

4) Run Flask web app
- Start the Flask app:
  python app.py
- Open http://localhost:5000 in your browser.
- The app streams webcam frames to the browser and overlays emotion labels on faces.

5) Run desktop GUI
- Launch the PyQt6 application:
  python gui.py
- Click "Start Detection" to begin webcam capture inside the desktop window.

6) Frontend (React)
- The `frontend/` folder contains a Create React App scaffold. To run it:
  cd frontend
  npm install
  npm start
- The frontend README contains Create React App usage instructions. Integrate the Flask stream endpoint or modify as needed.

## Notes & Troubleshooting
- Face detector: The code uses OpenCV Haar Cascade (`haarcascade_frontalface_default.xml`) included in repo. If detection fails, confirm the cascade path and camera feed are working.
- Camera index: If you have multiple cameras, change `cv2.VideoCapture(0)` to another index (1, 2, ...).
- TensorFlow compatibility: Use a TensorFlow version that matches your OS and hardware (CPU vs GPU). On some platforms, TensorFlow may require additional system libraries.
- Model file path: Scripts expect the model at `model/emotion_model.h5`. If you change the path, update the scripts accordingly.
- Training time: Training the CNN on CPU can be slow. Use GPU-enabled TensorFlow if available for faster training.
- Frontend integration: The React frontend is a scaffold; additional code is required to consume the Flask video stream if a web UI is desired.
- Missing requirements.txt / licence: Consider adding a `requirements.txt` and `LICENSE` file to the repository.

## Contributing
Contributions are welcome — please:
1. Open an issue to discuss large changes.
2. Submit pull requests for bug fixes, improvements, or additional features (e.g., pretrained model, test scripts, Dockerfile).
3. Add a `requirements.txt` and CI configuration for automated tests if possible.

## License
No license file is included in the repository. If you want others to use and contribute under a clear license, add a LICENSE file (MIT, Apache-2.0, etc.).

