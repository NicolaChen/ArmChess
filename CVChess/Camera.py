import threading
import time

import cv2


class Camera:

    def __init__(self):
        self.cam = cv2.VideoCapture(0)
        self.frame = None
        self.lock = threading.Lock()
        self.laplacian_threshold = 0
        self.flip_flag = 0
        self.cali_cap_event = 0
        self.stop_cam_flag = False

    def cali(self):
        print("Calibration begins. Exit by press key 'Esc'.")
        if not self.cam.isOpened():
            print("Cam Open Fail. Try Again!")
        while self.cam.isOpened():
            self.lock.acquire()
            frame = self.frame
            self.lock.release()
            frame_copy = frame.copy()
            if self.flip_flag:
                frame_copy = cv2.flip(frame, -1)
            cv2.putText(frame_copy, "Laplacian: " + str(cv2.Laplacian(frame, cv2.CV_64F).var())[:6], (0, 100),
                        cv2.FONT_HERSHEY_SIMPLEX, 4, (255, 0, 0), 6)
            cv2.namedWindow('calibration', 0)
            cv2.setWindowProperty('calibration', cv2.WND_PROP_FULLSCREEN, cv2.WINDOW_FULLSCREEN)
            cv2.setMouseCallback('calibration', self.captureEvent)
            cv2.imshow("calibration", frame_copy)
            if cv2.waitKey(100) == 27 or self.cali_cap_event or cv2.Laplacian(frame, cv2.CV_64F).var() > 500:
                self.laplacian_threshold = cv2.Laplacian(frame, cv2.CV_64F).var()
                print(self.laplacian_threshold)
                cv2.destroyWindow("calibration")
                break

    def captureEvent(self, event, x, y, flags, params):
        if event == cv2.EVENT_LBUTTONDBLCLK:
            self.cali_cap_event = 1

    def run(self):

        while True:
            self.lock.acquire()
            ret, frame = self.cam.read()
            scale = 0.5
            size = (int(scale * frame.shape[1]), int(scale * frame.shape[0]))
            self.frame = cv2.resize(frame, size)
            self.lock.release()
            if self.stop_cam_flag:
                print("Camera stops")
                break
            time.sleep(0.1)

    def getFrame(self):

        self.lock.acquire()
        frame = self.frame
        self.lock.release()
        if self.flip_flag:
            return cv2.flip(frame, -1)
        else:
            return frame

    def flip(self):
        
        self.flip_flag = 1
