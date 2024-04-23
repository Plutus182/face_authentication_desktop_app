import os
import cv2
import sys                                                                                                                           
import subprocess
from time import perf_counter
# from detector import FrameProcessor, PerformanceMetrics, draw_face_detection
from detector import *
from PyQt5.QtWidgets import QMainWindow, QVBoxLayout, QHBoxLayout, QWidget, QLabel, QPushButton, QApplication
from PyQt5.QtCore import QTimer, Qt
from PyQt5.QtGui import QImage, QPixmap, QIcon, QFont



class AuthenticationWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle('Face Authentication')
        self.setGeometry(600, 300, 800, 600)

        self.frame_processor = FrameProcessor()
        self.metrics = PerformanceMetrics()
        self.setWindowIcon(QIcon('resources/icons/face_icon.png'))
        self.initUI()
        self.initVideoCapture()
        

        # Lock timer: if no face is detected within 10 seconds, trigger lock
        self.lock_timer = QTimer(self)
        self.lock_timer.setInterval(10000)  # 10 seconds in milliseconds
        self.lock_timer.setSingleShot(True)  # The timer triggers only once per activation
        self.lock_timer.timeout.connect(self.lock_screen)
        self.authorized = False  # Assume unauthorized by default

    def initUI(self):
        self.centralWidget = QWidget(self)
        self.setCentralWidget(self.centralWidget)
        mainLayout = QVBoxLayout(self.centralWidget)

        self.videoLabel = QLabel('Webcam feed will appear here')
        # Styling the video label with an outline and rounded corners
        videoLabelStyle = """
            QLabel {
                font-family: Arial;
                font-size: 18px;
                color: #DDD;
            }
        """
        self.videoLabel.setAlignment(Qt.AlignCenter)
        self.videoLabel.setStyleSheet(videoLabelStyle)
        mainLayout.addWidget(self.videoLabel)

        buttonLayout = QHBoxLayout()
        
        # Styling buttons
        buttonStyle = """
            QPushButton {
                border: 2px solid #555;
                border-radius: 15px;
                background-color: #333;
                color: white;
                font-size: 16px;
                min-width: 150px;
                max-width: 150px;
                min-height: 40px;
                max-height: 40px;
                margin: 20px;
            }
            QPushButton:hover {
                background-color: #555;
            }
            QPushButton:pressed {
                background-color: #777;
            }
        """

        self.btn_activate = QPushButton('Activate')
        self.btn_activate.setStyleSheet(buttonStyle)
        self.btn_activate.setFixedSize(120, 40)
        self.btn_activate.clicked.connect(self.activateAuthentication)

        self.btn_deactivate = QPushButton('Deactivate')
        self.btn_deactivate.setStyleSheet(buttonStyle)
        self.btn_deactivate.setFixedSize(120, 40)
        self.btn_deactivate.clicked.connect(self.deactivateAuthentication)

        buttonLayout.addStretch()
        buttonLayout.addWidget(self.btn_activate)
        buttonLayout.addWidget(self.btn_deactivate)
        buttonLayout.addStretch()

        mainLayout.addLayout(buttonLayout)

    def lock_screen(self):
        """Lock the computer screen."""
        # The command depends on your operating system
        if os.name == 'nt':  # For Windows
            subprocess.run(["rundll32.exe", "user32.dll,LockWorkStation"])
            self.lock_timer.start()
        elif os.name == 'posix':  # For Linux/Unix
            subprocess.run(["gnome-screensaver-command", "--lock"])
        else:
            print("Locking screen mechanism not configured for your OS.")

    def initVideoCapture(self):
        self.capture = cv2.VideoCapture(0)  # Start video capture
        self.timer = QTimer(self)  # Timer for frame updates
        self.timer.timeout.connect(self.updateFrame)

    def activateAuthentication(self):
        self.timer.start(20)
        self.lock_timer.start()

    def deactivateAuthentication(self):
        self.timer.stop()

    def updateFrame(self):
        ret, frame = self.capture.read()
        if ret:
            start_time = perf_counter()
            detections = self.frame_processor.face_process(frame)
            frame, self.authorized = draw_face_detection(frame, self.frame_processor, detections)
            self.metrics.update(start_time, frame)
            self.displayImage(frame)
            if self.authorized == True:
                self.lock_timer.start()

    def displayImage(self, frame):
        rgb_image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        h, w, ch = rgb_image.shape
        bytes_per_line = ch * w
        convert_to_Qt_format = QImage(rgb_image.data, w, h, bytes_per_line, QImage.Format_RGB888)
        p = convert_to_Qt_format.scaled(self.videoLabel.width(), self.videoLabel.height(), Qt.KeepAspectRatio)
        self.videoLabel.setPixmap(QPixmap.fromImage(p))

    def closeEvent(self, event):
        self.capture.release()

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = AuthenticationWindow()
    window.show()
    sys.exit(app.exec_())
