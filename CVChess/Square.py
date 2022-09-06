import cv2
import numpy as np


class Square:

    def __init__(self, image, c1, c2, c3, c4, position, scale, state=''):

        # Corners
        self.c1 = c1
        self.c2 = c2
        self.c3 = c3
        self.c4 = c4

        # Position
        self.position = position

        # npArray of corners
        self.contour = np.array([c1, c2, c4, c3], dtype=np.int32)

        # Center of square
        self.error_flag = False
        m = cv2.moments(self.contour)
        try:
            cx, cy = int(m['m10'] / m['m00']), int(m['m01'] / m['m00'])
        except ZeroDivisionError:
            cx = 0
            cy = 0
            self.error_flag = True
            
        # ROI for image differencing
        self.roi = (cx, cy)
        self.radius = int(scale * 0.3)

        self.emptyColor = self.roiColor(image)
        self.state = state

    def draw(self, image, color, thickness=2):

        # Format npArray of corners for drawContours
        ctr = np.array(self.contour).reshape((-1, 1, 2)).astype(np.int32)
        cv2.drawContours(image, [ctr], 0, color, thickness)

    def drawROI(self, image, color, thickness=1):

        cv2.circle(image, self.roi, self.radius, color, thickness)

    def roiColor(self, image):
        # Initialise mask
        mask_image = np.zeros((image.shape[0], image.shape[1]), np.uint8)
        # Draw the ROI circle on the mask
        cv2.circle(mask_image, self.roi, self.radius, (255, 255, 255), -1)
        # Find the average color
        average_raw = cv2.mean(image, mask=mask_image)
        # Need int format so reassign variable
        average = (int(average_raw[0]), int(average_raw[1]), int(average_raw[2]))

        return average

    def roiGray(self, image):
        mask_image = np.zeros((image.shape[0], image.shape[1]), np.uint8)
        cv2.circle(mask_image, self.roi, self.radius, 255, -1)
        average_gray = cv2.mean(cv2.cvtColor(image, cv2.COLOR_BGR2GRAY), mask=mask_image)[0]
        return average_gray

    def roiDiff(self, fun_type, pre, cur):
        mask_image = np.zeros((pre.shape[0], pre.shape[1]), np.uint8)
        cv2.circle(mask_image, self.roi, self.radius, (255, 255, 255), -1)
        p = c = None
        if fun_type == 'color':
            p = pre
            c = cur
        elif fun_type == 'gray':
            p = cv2.cvtColor(pre, cv2.COLOR_BGR2GRAY)
            c = cv2.cvtColor(cur, cv2.COLOR_BGR2GRAY)
        else:
            print("Wrong type, color or gray")

        circle_p = np.zeros_like(p)
        circle_c = np.zeros_like(c)
        circle_p[mask_image == 255] = p[mask_image == 255]
        circle_c[mask_image == 255] = c[mask_image == 255]
        img_diff = cv2.absdiff(circle_c, circle_p)

        diff = (cv2.mean(img_diff, mask=mask_image)[0] + cv2.mean(img_diff, mask=mask_image)[1] +
                cv2.mean(img_diff, mask=mask_image)[2]) / 3

        return diff

    def classify(self, image):

        cv2.putText(image, self.position, self.roi, cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 1, cv2.LINE_AA)
