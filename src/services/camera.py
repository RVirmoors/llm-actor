import cv2
import base64
import threading


class Camera:
    def __init__(self, index: int = 0):
        self.index = index
        self.cap = None
        self.lock = threading.Lock()
        self._init_camera()

    def _init_camera(self):
        try:
            self.cap = cv2.VideoCapture(self.index)
            if not self.cap.isOpened():
                print("❌ Camera could not be opened")
                self.cap = None
        except Exception as e:
            print("❌ Camera init error:", e)
            self.cap = None

    def capture_base64(self) -> str | None:
        """Capture a frame and return it as base64 JPEG."""
        with self.lock:
            if self.cap is None:
                self._init_camera()
                if self.cap is None:
                    return None

            ret, frame = self.cap.read()

            if not ret:
                print("❌ Failed to read frame")
                return None

            # Encode to JPEG
            success, buffer = cv2.imencode(".jpg", frame)
            if not success:
                print("❌ Failed to encode frame")
                return None

            return base64.b64encode(buffer).decode("utf-8")

    def release(self):
        with self.lock:
            if self.cap is not None:
                self.cap.release()
                self.cap = None


# ✅ Global singleton (important for performance)
_camera_instance: Camera | None = None


def get_camera() -> Camera:
    global _camera_instance
    if _camera_instance is None:
        _camera_instance = Camera()
    return _camera_instance


def capture_image() -> str | None:
    """Convenience function for your pipeline."""
    camera = get_camera()
    return camera.capture_base64()