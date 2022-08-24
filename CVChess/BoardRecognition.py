import math

import cv2
import numpy as np

from CVChess.Board import Board
from CVChess.Line import Line
from CVChess.Square import Square

debug = False


class BoardRecognition:

    def __init__(self, camera):
        self.cam = camera
        self.square_scale = 50
        self.image = None
        self.contour_perimeter = 0

    def initializeBoard(self):
        corners = []
        while len(corners) < 121:
            while True:
                self.image = self.cam.getFrame()
                print(cv2.Laplacian(self.image, cv2.CV_64F).var())
                if abs(cv2.Laplacian(self.image, cv2.CV_64F).var() - self.cam.laplacian_threshold) < 20:
                    break
            thresh_image = self.cleanImage(self.image)
            max_contour, self.square_scale, self.contour_perimeter = self.getContour(self.image, thresh_image)
            mask_image = self.initializeMask(max_contour)
            edges, color_edges = self.findEdges(mask_image)
            # rot_edges, rot_color_edges = self.rotateImg(edges)	# 旋转线框图像至正位
            rot_edges, rot_color_edges = edges, color_edges  # 暂不旋转
            horizontal, vertical = self.findLines(rot_edges, rot_color_edges)
            corners = self.findCorners(horizontal, vertical, rot_color_edges)
        squares = self.findSquares(corners, self.image)
        board = Board(squares)
        return board

    @staticmethod
    def cleanImage(image):
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        blur = cv2.GaussianBlur(gray, (17, 17), 0)
        ret1, th1 = cv2.threshold(blur, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
        ret2, th2 = cv2.threshold(blur, ret1 - 20, 255, cv2.THRESH_BINARY)
        auto_thresh = th2

        if debug:
            cv2.imshow("Auto Thresholding", auto_thresh)
            cv2.waitKey(0)
            cv2.destroyAllWindows()

        return auto_thresh

    @staticmethod
    def getContour(color_image, thresh_image):
        contours, hierarchy = cv2.findContours(thresh_image, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
        image_copy = color_image.copy()
        max_ratio = 0
        max_contour = None
        max_perimeter = 0
        max_area = 0
        for c in range(len(contours)):
            area = cv2.contourArea(contours[c])
            perimeter = cv2.arcLength(contours[c], True)
            if perimeter > 0:
                ratio = area / perimeter
            else:
                continue
            if ratio > max_ratio:
                max_contour = contours[c]
                max_ratio = ratio
                max_perimeter = perimeter
                max_area = area
        square_scale = int(np.sqrt(max_area) / 9)
        contour_perimeter = max_perimeter
        cv2.drawContours(image_copy, [max_contour], -1, (0, 0, 0), 1)

        if debug:
            # Show image with contours drawn
            cv2.imshow("Chess Boarder", image_copy)
            cv2.waitKey(0)
            cv2.destroyAllWindows()

        return max_contour, square_scale, contour_perimeter

    def initializeMask(self, max_contour):

        chessboard_edges = cv2.convexHull(max_contour)  # 改用更好的凸包
        mask = np.zeros((self.image.shape[0], self.image.shape[1]), 'uint8')
        cv2.fillConvexPoly(mask, chessboard_edges, 255, 1)
        extracted = np.zeros_like(self.image)
        extracted[mask == 255] = self.image[mask == 255]

        if debug:
            # Show image with mask drawn
            cv2.imshow("masked image", extracted)
            cv2.waitKey(0)
            cv2.destroyAllWindows()

        return extracted

    @staticmethod
    def findEdges(mask_image):
        edges = cv2.Canny(mask_image, 60, 100, None, 3)

        if debug:
            # Show image with edges drawn
            cv2.imshow("Canny", edges)
            cv2.waitKey(0)
            cv2.destroyAllWindows()

        color_edges = cv2.cvtColor(edges, cv2.COLOR_GRAY2BGR)
        return edges, color_edges

    def rotateImg(self, edges):
        lines = cv2.HoughLinesP(edges, 1, np.pi / 180, 100, np.array([]), self.square_scale * 2, self.square_scale * 3)
        a, b, c = lines.shape
        angles = []
        for i in range(a):
            [[x1, y1, x2, y2]] = lines[i]
            angle_lines_new = Line(x1, x2, y1, y2)
            angles.append(angle_lines_new.get_angle())

        avg_rot_angle = np.mean(angles)
        print('average rotation angle: ', avg_rot_angle)

        rotate_matrix = cv2.getRotationMatrix2D((edges.shape[1] // 2, edges.shape[0] // 2), avg_rot_angle, 1.0)
        rot_img = cv2.warpAffine(edges, rotate_matrix, (edges.shape[1], edges.shape[0]))
        rot_img = np.array(rot_img, np.uint8)
        rot_bgr = cv2.cvtColor(rot_img, cv2.COLOR_GRAY2BGR)
        return rot_img, rot_bgr

    def findLines(self, edges, color_edges):
        lines = cv2.HoughLinesP(edges, 1, np.pi / 180, 100, np.array([]), self.square_scale * 2, self.square_scale * 3)
        a, b, c = lines.shape
        for i in range(a):
            cv2.line(color_edges, (lines[i][0][0], lines[i][0][1]), (lines[i][0][2], lines[i][0][3]), (0, 255, 0), 2,
                     cv2.LINE_AA)

        if debug:
            # Show image with lines drawn
            cv2.imshow("Lines", color_edges)
            cv2.waitKey(0)
            cv2.destroyAllWindows()

        horizontal = []
        vertical = []
        for i in range(a):
            [[x1, y1, x2, y2]] = lines[i]
            new_line = Line(x1, x2, y1, y2)
            if new_line.orientation == 'horizontal':
                horizontal.append(new_line)
            else:
                vertical.append(new_line)

        return horizontal, vertical

    def findCorners(self, horizontal, vertical, color_edges):
        corners = []
        for v in vertical:
            for h in horizontal:
                s1, s2 = v.find_intersection(h)
                corners.append([s1, s2])

        dedupe_corners = []
        for c in corners:
            matching_flag = False
            for d in dedupe_corners:
                if math.sqrt((d[0] - c[0]) * (d[0] - c[0]) + (d[1] - c[1]) * (d[1] - c[1])) < self.square_scale * 0.3:
                    matching_flag = True
                    break
            if not matching_flag:
                dedupe_corners.append(c)

        for d in dedupe_corners:
            cv2.circle(color_edges, (d[0], d[1]), 10, (0, 0, 255))

        if debug:
            # Show image with corners circled
            cv2.imshow("Corners", color_edges)
            cv2.waitKey(0)
            cv2.destroyAllWindows()

        return dedupe_corners

    def findSquares(self, corners, color_edges):
        corners.sort(key=lambda x: x[0])
        rows = [[], [], [], [], [], [], [], [], [], [], []]
        r = 0
        size = 11
        for c in range(0, size ** 2):
            if c > 0 and c % size == 0:
                r = r + 1

            rows[r].append(corners[c])

        letters = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h']
        numbers = ['1', '2', '3', '4', '5', '6', '7', '8']
        squares = []

        for r in rows:
            r.sort(key=lambda y: y[1])

        for r in range(0, 8):
            for c in range(0, 8):
                c1 = rows[r + 1][c + 1]
                c2 = rows[r + 1][c + 1 + 1]
                c3 = rows[r + 1 + 1][c + 1]
                c4 = rows[r + 1 + 1][c + 1 + 1]

                position = letters[r] + numbers[7 - c]
                new_squares = Square(color_edges, c1, c2, c3, c4, position, self.square_scale)
                new_squares.draw(color_edges, (0, 0, 255), 3)
                new_squares.drawROI(color_edges, (255, 0, 0), 2)
                new_squares.classify(color_edges)
                squares.append(new_squares)

        if debug:
            # Show image with squares and ROI drawn and position labelled
            cv2.imshow("Squares", color_edges)
            cv2.waitKey(0)
            cv2.destroyAllWindows()

        return squares
