import logging as log
from time import perf_counter
import cv2
from openvino.runtime import Core, get_version
from landmarks_detector import LandmarksDetector
from face_detector import FaceDetector
from faces_database import FacesDatabase
from face_identifier import FaceIdentifier
from model_api.performance_metrics import PerformanceMetrics

log.basicConfig(level=log.INFO)  # Initialize logging

source = "videos/test_video.mp4"
device = "CPU"
faceDETECT = "model_2022_3/face-detection-retail-0004.xml"
faceLANDMARK = "model_2022_3/landmarks-regression-retail-0009.xml"
faceIDENTIFY = "model_2022_3/face-reidentification-retail-0095.xml"

class FrameProcessor:
    QUEUE_SIZE = 16
    def __init__(self):
        log.info('OpenVINO Runtime')
        log.info('\tbuild: {}'.format(get_version()))
        core = Core()
        self.face_detector = FaceDetector(core, faceDETECT, input_size=(0, 0), confidence_threshold=0.6)
        self.landmarks_detector = LandmarksDetector(core, faceLANDMARK)
        self.face_identifier = FaceIdentifier(core, faceIDENTIFY, match_threshold=0.7, match_algo='HUNGARIAN')
        self.face_detector.deploy(device)
        self.landmarks_detector.deploy(device, self.QUEUE_SIZE)
        self.face_identifier.deploy(device, self.QUEUE_SIZE)
        self.face_database = FacesDatabase('face_img', self.face_identifier, self.landmarks_detector)
        self.face_identifier.set_faces_database(self.face_database)
        log.info('Database is built, registered {} identities'.format(len(self.face_database)))

    def face_process(self, frame):
        rois = self.face_detector.infer((frame,))
        if len(rois) > self.QUEUE_SIZE:
            rois = rois[:self.QUEUE_SIZE]
        landmarks = self.landmarks_detector.infer((frame, rois))
        face_identities, unknowns = self.face_identifier.infer((frame, rois, landmarks))
        return [rois, landmarks, face_identities]

def draw_face_detection(frame, frame_processor, detections):
    is_authorized = False
    size = frame.shape[:2]
    for roi, landmarks, identity in zip(*detections):
        text = frame_processor.face_identifier.get_identity_label(identity.id)
        xmin = max(int(roi.position[0]), 0)
        ymin = max(int(roi.position[1]), 0)
        xmax = min(int(roi.position[0] + roi.size[0]), size[1])
        ymax = min(int(roi.position[1] + roi.size[1]), size[0])
        cv2.rectangle(frame, (xmin, ymin), (xmax, ymax), (0, 220, 0), 2)
        for point in landmarks:
            x = int(xmin + roi.size[0] * point[0])
            y = int(ymin + roi.size[1] * point[1])
            cv2.circle(frame, (x, y), 1, (0, 255, 255), 2)
        is_authorized = image_recognizer(frame, text, identity, (xmin, ymin), 0.75)
    return frame, is_authorized

def image_recognizer(frame, text, identity, face_point, threshold):
    xmin, ymin = face_point
    if identity.id != FaceIdentifier.UNKNOWN_ID:
        if (1 - identity.distance) > threshold:
            textsize = cv2.getTextSize(text, cv2.FONT_HERSHEY_SIMPLEX, 0.7, 1)[0]
            cv2.rectangle(frame, (xmin, ymin), (xmin + textsize[0], ymin - textsize[1]), (255, 255, 255), cv2.FILLED)
            cv2.putText(frame, text, (xmin, ymin), cv2.FONT_HERSHEY_COMPLEX, 0.7, (0, 0, 0), 1)
            return True
        else:
            textsize = cv2.getTextSize("Unknown", cv2.FONT_HERSHEY_SIMPLEX, 0.7, 1)[0]
            cv2.rectangle(frame, (xmin, ymin), (xmin + textsize[0], ymin - textsize[1]), (255, 255, 255), cv2.FILLED)
            cv2.putText(frame, "Unknown", (xmin, ymin), cv2.FONT_HERSHEY_COMPLEX, 0.7, (0, 0, 0), 1)
            return False


# # cap = cv2.VideoCapture(source)
# cap = cv2.VideoCapture(0)
# frame_processor = FrameProcessor()
# metrics = PerformanceMetrics()

# while True:
#     start_time = perf_counter()
#     ret, frame = cap.read()
#     if not ret:
#         break
#     detections = frame_processor.face_process(frame)
#     frame = draw_face_detection(frame, frame_processor, detections)
#     metrics.update(start_time, frame)
#     cv2.imshow("face recognition demo", frame)
#     key = cv2.waitKey(1)
#     if key in {ord('q'), ord('Q'), 27}:
#         break

# cap.release()
# cv2.destroyAllWindows()
