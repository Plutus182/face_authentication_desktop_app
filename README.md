# Face Authentication App

This Face Authentication App is a desktop application developed using PyQt5 and powered by Intel's OpenVINO toolkit. It leverages advanced face recognition models to authenticate users in real-time via a webcam. If an authorized user is not detected within 10 seconds, the system automatically locks the screen, enhancing security measures for your device.

## Key Features

- **Real-Time Authentication**: Instantly recognizes faces through a webcam.
- **Auto-Lock Mechanism**: Automatically locks the screen if no authorized user is detected within a specified time frame.
- **Intel Hardware Optimization**: Specifically optimized for Intel hardware using the lightest and fastest models available.

## Prerequisites

Before installing and running the Face Authentication App, ensure you have the following:

- Python 3.6 or newer
- PyQt5
- OpenVINO Toolkit

## Models

The application incorporates the following models from the OpenVINO Model Zoo:

- **Face Detection**: `face-detection-retail-0004.xml`
- **Landmark Regression**: `landmarks-regression-retail-0009.xml`
- **Face Reidentification**: `face-reidentification-retail-0095.xml`

## Installation

To install the Face Authentication App, follow these steps:

### Clone the Repository

```bash
git clone https://github.com/Plutus182/face_authentication_desktop_app.git
cd face-authentication-app
```
