import math


class Line:

	def __init__(self, x1, x2, y1, y2):

		self.x1 = x1
		self.x2 = x2
		self.y1 = y1
		self.y2 = y2

		self.dx = self.x2 - self.x1
		self.dy = self.y2 - self.y1

		if abs(self.dx) > abs(self.dy):
			self.orientation = 'horizontal'
		else:
			self.orientation = 'vertical'

	def find_intersection(self, other):

		# Determinant for finding points of intersection
		x = ((self.x1 * self.y2 - self.y1 * self.x2) * (other.x1 - other.x2) - (self.x1 - self.x2) * (
				other.x1 * other.y2 - other.y1 * other.x2)) / (
					(self.x1 - self.x2) * (other.y1 - other.y2) - (self.y1 - self.y2) * (other.x1 - other.x2))
		y = ((self.x1 * self.y2 - self.y1 * self.x2) * (other.y1 - other.y2) - (self.y1 - self.y2) * (
				other.x1 * other.y2 - other.y1 * other.x2)) / (
					(self.x1 - self.x2) * (other.y1 - other.y2) - (self.y1 - self.y2) * (other.x1 - other.x2))
		x = int(x)
		y = int(y)

		return x, y

	def get_angle(self):
		"""
		获得网格线与方向轴正向的夹角[-45 deg, 45 deg]
		"""
		angle_r = math.atan2(self.dy, self.dx)
		angle = angle_r / math.pi * 180
		if self.orientation == 'horizontal':
			if self.dx * self.dy > 0 > angle:
				angle += 180
			elif self.dx * self.dy < 0 < angle:
				angle -= 180
		elif self.orientation == 'vertical':
			if self.dy > 0:
				angle -= 90
			else:
				angle += 90

		return angle

	def get_pts(self):
		pt1 = (self.x1, self.y1)
		pt2 = (self.x2, self.y2)
		return pt1, pt2
