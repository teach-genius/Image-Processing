from PySide6.QtCore import QThread, Signal, QDateTime
from PySide6.QtGui import QImage


class ReadVideo(QThread):
    frame_signal = Signal(QImage)
    def __init__(self, video_path=None):
        super().__init__()
        self.video_path = video_path
        self.running = True
        self.cap = None
    def run(self):
        # Ouvrir la webcam ou la vidéo
        self.cap = cv2.VideoCapture(self.video_path)
        while self.running:
            ret, frame = self.cap.read()
            if ret:
                frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                h, w, ch = frame_rgb.shape
                bytes_per_line = ch * w
                img = QImage(frame_rgb.data, w, h, bytes_per_line, QImage.Format_RGB888)
                self.frame_signal.emit(img)
            else:
                break

    def stop(self):
        self.running = False
        if self.cap:
            self.cap.release()
 
            

    