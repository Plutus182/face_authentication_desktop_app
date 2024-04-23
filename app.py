import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QPushButton, QVBoxLayout, QWidget, QLabel, QLineEdit
from PyQt5.QtWidgets import QApplication, QMainWindow, QPushButton, QVBoxLayout, QHBoxLayout, QWidget, QLabel
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QPixmap, QIcon

from enrollmentPage import EnrollmentWindow
from authenticationPage import AuthenticationWindow

class App(QMainWindow):
    def __init__(self):
        # self.initUI()
        super().__init__()
        self.setWindowTitle('Face Authentication App')
        self.setGeometry(600, 300, 800, 600)
        self.setWindowIcon(QIcon('resources/icons/face_icon.png'))

        self.backgroundPixmap = QPixmap('resources/facial-recognition-background.jpg')
        self.backgroundLabel = QLabel(self)
        self.set_background()
        
        # Initialize the windows
        self.enrollmentWindow = EnrollmentWindow()
        
        
        
        self.initUI()

    def initUI(self):
        self.backgroundPixmap = QPixmap('resources/facial-recognition-background.jpg')
        self.backgroundLabel = QLabel(self)
        self.backgroundLabel.setPixmap(self.backgroundPixmap.scaled(self.size(), Qt.KeepAspectRatioByExpanding, Qt.SmoothTransformation))
        self.backgroundLabel.resize(self.size())

        self.centralWidget = QWidget(self)
        self.setCentralWidget(self.centralWidget)
        self.centralWidget.setStyleSheet("background-color: rgba(0, 0, 0, 0);")

        mainLayout = QVBoxLayout(self.centralWidget)

        # Description label
        self.descriptionLabel = QLabel("This is a Face Authentication App utilizing cutting-edge OpenVINO technology for rapid and accurate facial recognition.\n"
                                       "Use it to seamlessly authenticate users, leveraging advanced AI models for security and convenience.\n"
                                       "Effortlessly activate or deactivate authentication features to suit various operational requirements.", self.centralWidget)
        self.descriptionLabel.setStyleSheet("""
            background-color: rgba(255, 255, 255, 100);
            font-family: Arial;
            border-radius: 15px;
            color: white;
            padding: 10px;
            font-size: 14px;
        """)
        self.descriptionLabel.setAlignment(Qt.AlignCenter)
        mainLayout.addWidget(self.descriptionLabel, 0, Qt.AlignHCenter | Qt.AlignVCenter)

        # Button styling
        buttonStyle = """
            QPushButton {
                border: 2px solid #8f8f91;
                border-radius: 15px;
                background-color: rgba(255, 255, 255, 10);
                color: white;
                font-size: 20px;
                min-width: 120px;
                max-width: 120px;
                min-height: 30px;
                max-height: 30px;
                padding: 5px;
                margin: 20px;
            }
            QPushButton:pressed {
                background-color: rgba(255, 255, 255, 50);
            }
        """

        # Buttons layout
        buttonLayout = QHBoxLayout()
        self.btn_openEnrollmentWindow = QPushButton('Enroll')
        self.btn_openEnrollmentWindow.setStyleSheet(buttonStyle)
        buttonLayout.addWidget(self.btn_openEnrollmentWindow, 0, Qt.AlignBottom | Qt.AlignHCenter)

        self.btn_openAuthenticationWindow = QPushButton(' Run ')
        self.btn_openAuthenticationWindow.setStyleSheet(buttonStyle)
        buttonLayout.addWidget(self.btn_openAuthenticationWindow, 0, Qt.AlignBottom | Qt.AlignHCenter)

        # Add buttons to the main layout with stretch to push them to the bottom
        mainLayout.addStretch(1)
        mainLayout.addLayout(buttonLayout)

        # Connect buttons to their functions
        self.btn_openEnrollmentWindow.clicked.connect(self.openEnrollmentWindow)
        self.btn_openAuthenticationWindow.clicked.connect(self.openAuthenticationWindow)
    
    def set_background(self):
        # Scale the pixmap to fill the window, maintaining the aspect ratio
        scaledPixmap = self.backgroundPixmap.scaled(self.size(), Qt.KeepAspectRatioByExpanding, Qt.SmoothTransformation)
        self.backgroundLabel.setPixmap(scaledPixmap)
        self.backgroundLabel.resize(self.size())

    def resizeEvent(self, event):
        # Update the background image to fit the new window size
        self.set_background()
        super().resizeEvent(event)

    def openEnrollmentWindow(self):
        # Ensure Enrollment window is visible and focused
        self.enrollmentWindow.show()
        self.enrollmentWindow.raise_()
        self.enrollmentWindow.activateWindow()

    def openAuthenticationWindow(self):
        # Ensure authentication window is visible and focused
        self.authenticationWindow = AuthenticationWindow()
        self.authenticationWindow.show()
        self.authenticationWindow.raise_()
        self.authenticationWindow.activateWindow()

if __name__ == '__main__':
    app = QApplication(sys.argv)
    mainWindow = App()
    mainWindow.show()
    sys.exit(app.exec_())