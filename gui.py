import sys
import cv2
import numpy as np
from PyQt6.QtWidgets import (
    QApplication, QWidget, QVBoxLayout, QPushButton, QLabel, QFrame
)
from PyQt6.QtCore import QThread, pyqtSignal, Qt, QTimer
from PyQt6.QtGui import QImage, QPixmap, QPainter, QColor
from tensorflow.keras.models import load_model


class VideoThread(QThread):
    change_pixmap_signal = pyqtSignal(np.ndarray, str)

    def run(self):
        model = load_model('model/emotion_model.h5')
        emotions = ['Angry', 'Disgust', 'Fear', 'Happy', 'Sad', 'Surprise', 'Neutral']

        face_cascade = cv2.CascadeClassifier(
            cv2.data.haarcascades + 'haarcascade_frontalface_default.xml'
        )

        cap = cv2.VideoCapture(0)

        while True:
            ret, frame = cap.read()
            if not ret:
                continue

            gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            faces = face_cascade.detectMultiScale(gray, 1.3, 5)

            emotion_text = "No Face"

            for (x, y, w, h) in faces:
                face = gray[y:y+h, x:x+w]
                face = cv2.resize(face, (48, 48))
                face = face / 255.0
                face = np.reshape(face, (1, 48, 48, 1))

                prediction = model.predict(face, verbose=0)
                emotion_text = emotions[np.argmax(prediction)]

                cv2.putText(frame, emotion_text, (x, y - 10),
                            cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
                cv2.rectangle(frame, (x, y), (x + w, y + h), (255, 0, 0), 2)

            self.change_pixmap_signal.emit(frame, emotion_text)


class LiveBackground(QWidget):
    def __init__(self):
        super().__init__()
        self.angle = 0
        self.timer = QTimer()
        self.timer.timeout.connect(self.update_animation)
        self.timer.start(50)

    def update_animation(self):
        self.angle += 2
        self.update()

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)

        # Gradient background
        gradient_color = QColor(20, 20, 40)
        painter.fillRect(self.rect(), gradient_color)

        # Animated circles (ML style watermark)
        painter.setPen(Qt.PenStyle.NoPen)

        for i in range(10):
            painter.setBrush(QColor(0, 255, 150, 40))
            radius = 50 + i * 20
            x = int(self.width() / 2 + radius * np.cos(np.radians(self.angle + i * 20)))
            y = int(self.height() / 2 + radius * np.sin(np.radians(self.angle + i * 20)))
            painter.drawEllipse(x, y, 20, 20)


class App(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("AI Emotion Detector Pro")
        self.setGeometry(100, 100, 900, 700)

        self.bg = LiveBackground()

        self.video_label = QLabel(self)
        self.video_label.setFixedSize(700, 500)
        self.video_label.setStyleSheet("border-radius:15px; background:black;")

        self.emotion_label = QLabel("Emotion: --")
        self.emotion_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.emotion_label.setStyleSheet("font-size: 24px; color: cyan;")

        self.start_btn = QPushButton("Start Detection")
        self.start_btn.setStyleSheet("""
            QPushButton {
                background-color: #739e90;
                padding: 10px;
                border-radius: 10px;
                font-size: 18px;
            }
            QPushButton:hover {
                background-color: #00cc88;
            }
        """)

        layout = QVBoxLayout()
        layout.addWidget(self.video_label, alignment=Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(self.emotion_label)
        layout.addWidget(self.start_btn)

        container = QFrame(self)
        container.setLayout(layout)
        container.setStyleSheet("background: transparent;")

        main_layout = QVBoxLayout(self)
        main_layout.addWidget(container)

        self.thread = VideoThread()
        self.thread.change_pixmap_signal.connect(self.update_image)

        self.start_btn.clicked.connect(self.start_camera)

    def start_camera(self):
        self.thread.start()

    def update_image(self, cv_img, emotion):
        qt_img = self.convert_cv_qt(cv_img)
        self.video_label.setPixmap(qt_img)
        self.emotion_label.setText(f"Emotion: {emotion}")

    def convert_cv_qt(self, cv_img):
        rgb_image = cv2.cvtColor(cv_img, cv2.COLOR_BGR2RGB)
        h, w, ch = rgb_image.shape
        bytes_per_line = ch * w
        qt_image = QImage(rgb_image.data, w, h, bytes_per_line, QImage.Format.Format_RGB888)
        return QPixmap.fromImage(qt_image).scaled(
            self.video_label.width(), self.video_label.height(), Qt.AspectRatioMode.KeepAspectRatio
        )


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = App()
    window.show()
    sys.exit(app.exec())
