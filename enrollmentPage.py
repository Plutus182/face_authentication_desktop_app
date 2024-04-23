import sys
import os
import cv2
from PyQt5.QtWidgets import (QApplication, QMainWindow, QWidget, QLabel, QVBoxLayout, QHBoxLayout, QLineEdit,
                             QPushButton, QFileDialog)
from PyQt5.QtCore import Qt, QTimer
from PyQt5.QtGui import QImage, QPixmap, QFont, QIcon

class EnrollmentWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Let's Get You Enrolled!")
        self.setGeometry(600, 300, 800, 600)
        self.setWindowIcon(QIcon('resources/icons/face_icon.png'))
        self.initUI()
        self.photo_count = 1

    def initUI(self):
        # Central widget
        centralWidget = QWidget(self)
        self.setCentralWidget(centralWidget)

        # Main layout
        mainLayout = QHBoxLayout(centralWidget)

        # Left column: Webcam
        webcamLayout = QVBoxLayout()
        self.webcamView = QLabel(self)
        self.webcamView.setAlignment(Qt.AlignCenter)  # Center the video feed within the label
        self.webcamView.setMinimumSize(360, 240)  # Adjusted for a minimum size to better fit layout
        self.capture = cv2.VideoCapture(0)
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.update_frame)
        self.timer.start(100)

        # Webcam buttons
        webcamButtonsLayout = QHBoxLayout()
        takePhotoBtn = QPushButton("Take Photo")
        takePhotoBtn.clicked.connect(self.take_photo)
        openFolderBtn = QPushButton("Open Folder")
        openFolderBtn.clicked.connect(self.open_folder)

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
        takePhotoBtn.setStyleSheet(buttonStyle)
        openFolderBtn.setStyleSheet(buttonStyle)

        # Adding buttons to their layout and aligning center
        webcamButtonsLayout.addWidget(takePhotoBtn)
        webcamButtonsLayout.addWidget(openFolderBtn)
        webcamButtonsLayout.setAlignment(Qt.AlignCenter)

        # Adding elements to webcam layout
        webcamLayout.addWidget(self.webcamView)
        webcamLayout.addLayout(webcamButtonsLayout)
        webcamLayout.setAlignment(Qt.AlignCenter)

        # Right column: Form inputs and buttons
        formLayout = QVBoxLayout()

        # Name input field
        self.nameInput = QLineEdit()
        self.nameInput.setPlaceholderText("Enter Your Full Name")
        self.nameInput.setFont(QFont("Arial", 16))  # Larger font size
        self.nameInput.setAlignment(Qt.AlignCenter)
        self.nameInput.setStyleSheet("""
            QLineEdit {
                background: white; 
                color: black; 
                padding: 10px; 
                min-width: 200px;
                max-width: 300px; 
                margin: 10px;
            }
        """)

        # Submit button directly below the name input
        submitBtn = QPushButton("Submit")
        submitBtn.setStyleSheet(buttonStyle)

        # Adding elements to form layout
        formLayout.addWidget(self.nameInput, 1, Qt.AlignCenter)
        formLayout.addWidget(submitBtn, 1, Qt.AlignCenter)  # Adjusted alignment

        # Combine layouts
        mainLayout.addLayout(webcamLayout, 60)
        mainLayout.addLayout(formLayout, 40)

    def update_frame(self):
        ret, self.frame = self.capture.read()
        if ret:
            rgb_image = cv2.cvtColor(self.frame, cv2.COLOR_BGR2RGB)
            h, w, ch = rgb_image.shape
            bytes_per_line = ch * w
            convert_to_Qt_format = QImage(rgb_image.data, w, h, bytes_per_line, QImage.Format_RGB888)
            p = convert_to_Qt_format.scaled(self.webcamView.width(), self.webcamView.height(), Qt.KeepAspectRatio)
            self.webcamView.setPixmap(QPixmap.fromImage(p))

    def take_photo(self):
        if hasattr(self, 'frame'):
            name = self.nameInput.text().strip().replace(" ", "_")
            if not name:
                name = "Unknown"
            directory = "face_img"
            if not os.path.exists(directory):
                os.makedirs(directory)
            path = os.path.join(directory, f"{name}-{self.photo_count}.jpg")
            cv2.imwrite(path, self.frame)
            self.photo_count += 1

    def open_folder(self):
        path = os.path.join(os.getcwd(), "face_img")
        os.startfile(path)

    def closeEvent(self, event):
        self.capture.release()

def main():
    app = QApplication(sys.argv)
    ex = EnrollmentWindow()
    ex.show()
    sys.exit(app.exec_())

if __name__ == '__main__':
    main()
