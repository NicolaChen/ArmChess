import threading
import time

import cv2


class Camera:

    def __init__(self):
        self.cam = cv2.VideoCapture(0)
        self.frame = None
        self.lock = threading.Lock()
        self.laplacian_threshold = 0

    def cali(self):
        print("Calibration begins. Exit by press key 'Esc'.")
        if not self.cam.isOpened():
            print("Cam Open Fail. Try Again!")
        while self.cam.isOpened():
            self.lock.acquire()
            frame = self.frame
            self.lock.release()
            frame_copy = frame.copy()
            cv2.putText(frame_copy, "Laplacian: " + str(cv2.Laplacian(frame, cv2.CV_64F).var()), (100, 100),
                        cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 0, 0))
            cv2.putText(frame_copy, 'w: ' + str(frame.shape[1]) + ', h: ' + str(frame.shape[0]) + " threshold_var: "
                        + str(3E8 / (frame.shape[1] * frame.shape[0])), (100, 200), cv2.FONT_HERSHEY_SIMPLEX, 1,
                        (255, 0, 0))
            cv2.putText(frame_copy, str(cv2.mean(frame)[0] + cv2.mean(frame)[1] + cv2.mean(frame)[2]), (100, 300),
                        cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 0, 0))
            cv2.imshow("calibration", frame_copy)  # TODO: Figure out how to fix the position of imshow window
            if cv2.waitKey(100) == 27 or cv2.Laplacian(frame, cv2.CV_64F).var() > 400:
                self.laplacian_threshold = cv2.Laplacian(frame, cv2.CV_64F).var()
                print(self.laplacian_threshold)
                cv2.destroyWindow("calibration")
                break

    def run(self):

        while True:
            self.lock.acquire()
            ret, frame = self.cam.read()
            scale = 0.5  # TODO: Test appropriate scale for 800*600 screen
            size = (int(scale * frame.shape[1]), int(scale * frame.shape[0]))
            self.frame = cv2.resize(frame, size)
            self.lock.release()
            time.sleep(0.1)

    def getFrame(self):

        self.lock.acquire()
        frame = self.frame
        self.lock.release()
        return frame
