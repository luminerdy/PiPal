"""Local camera capture and lightweight frontal-face detection; no recording."""
from pathlib import Path


class Tracker:
    def __init__(self, camera=None, width=640, height=480):
        try:
            import cv2
        except ImportError as exc:
            raise RuntimeError(
                "OpenCV is missing. Install python3-opencv and opencv-data; see README.md."
            ) from exc
        self.cv2 = cv2
        cv2.setNumThreads(2)
        cascades = [Path('/usr/share/opencv4/haarcascades/haarcascade_frontalface_default.xml')]
        if hasattr(cv2, 'data'):
            cascades.append(Path(cv2.data.haarcascades) / 'haarcascade_frontalface_default.xml')
        cascade = next((p for p in cascades if p.is_file()), None)
        if cascade is None:
            raise RuntimeError('Face cascade not found. Install opencv-data; see README.md.')
        self.detector = cv2.CascadeClassifier(str(cascade))
        if self.detector.empty():
            raise RuntimeError(f'Could not load face cascade: {cascade}')
        if camera is None:
            candidates = sorted(Path('/dev/v4l/by-id').glob('*C920*video-index0'))
            if len(candidates) != 1:
                raise RuntimeError(
                    'Cannot select a unique C920. Inspect v4l2-ctl --list-devices and pass --camera PATH.'
                )
            camera = str(candidates[0])
        self.camera = camera
        self.capture = cv2.VideoCapture(camera, cv2.CAP_V4L2)
        try:
            if not self.capture.isOpened():
                raise RuntimeError(f'Cannot open camera {camera}. Check connection, permissions, and other apps.')
            self.capture.set(cv2.CAP_PROP_FOURCC, cv2.VideoWriter_fourcc(*'MJPG'))
            self.capture.set(cv2.CAP_PROP_FRAME_WIDTH, width)
            self.capture.set(cv2.CAP_PROP_FRAME_HEIGHT, height)
            self.capture.set(cv2.CAP_PROP_FPS, 30)
            self.capture.set(cv2.CAP_PROP_BUFFERSIZE, 1)
        except Exception:
            self.close()
            raise

    def read(self):
        ok, frame = self.capture.read()
        if not ok or frame is None:
            raise RuntimeError('Camera stopped delivering frames. Reconnect it and restart PiPal.')
        return frame

    def detect(self, frame):
        cv2 = self.cv2
        # Work at half-size by default; boxes are in this image's coordinates.
        height, width = frame.shape[:2]
        size = (320, max(1, round(320 * height / width)))
        small = cv2.resize(frame, size)
        gray = cv2.equalizeHist(cv2.cvtColor(small, cv2.COLOR_BGR2GRAY))
        faces = self.detector.detectMultiScale(gray, scaleFactor=1.15, minNeighbors=5, minSize=(30, 30))
        return faces, size

    def close(self):
        self.capture.release()
