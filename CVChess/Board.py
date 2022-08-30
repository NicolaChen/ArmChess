import math

import cv2

debug = True


class Board:
    """
    Holds all the Square instances and updates changes to board after moves
    """

    def __init__(self, squares):

        self.squares = squares
        self.board_matrix = []
        self.promotion = 'q'
        self.promo = False
        self.move = "e2e4"
        self.dist_threshold = 50

    def draw(self, image):
        """
        Draws the board and classifies the squares (draws the square state on the image).
        """
        for square in self.squares:
            square.draw(image, (0, 0, 255))
            square.classify(image)

    def assignState(self):
        """
        Assigns initial setup states to squares and initializes the Board matrix.
        """
        black = ['r', 'n', 'b', 'q', 'k', 'b', 'n', 'r']
        white = ['R', 'N', 'B', 'Q', 'K', 'B', 'N', 'R']

        for i in range(8):
            self.squares[8 * i + 0].state = black[i]
            self.squares[8 * i + 1].state = 'p'
            self.squares[8 * i + 2].state = '.'
            self.squares[8 * i + 3].state = '.'
            self.squares[8 * i + 4].state = '.'
            self.squares[8 * i + 5].state = '.'
            self.squares[8 * i + 6].state = 'P'
            self.squares[8 * i + 7].state = white[i]

        for square in self.squares:
            self.board_matrix.append(square.state)

    def determineChanges(self, previous, current):
        """
        Determines the change in color values within square circles to infer piece movement
        """
        copy = current.copy()

        largest_square = 0
        second_largest_square = 0
        largest_dist = 0
        second_largest_dist = 0
        state_change = []

        if debug:
            # check for differences in gray between the photos
            cv2.imshow('diff', cv2.absdiff(cv2.cvtColor(current, cv2.COLOR_BGR2GRAY),
                                           cv2.cvtColor(previous, cv2.COLOR_BGR2GRAY)))

        for sq in self.squares:
            distance = sq.roiDiff('color', previous, current)

            if distance > self.dist_threshold:
                state_change.append(sq)
            if distance > largest_dist:
                # update squares with the largest change in color
                second_largest_square = largest_square
                second_largest_dist = largest_dist
                largest_dist = distance
                largest_square = sq
            elif distance > second_largest_dist:
                # update second change in color
                second_largest_dist = distance
                second_largest_square = sq

        # TODO: add new detect for PAWN special: en passant, current code can only infer from attacking side's move
        if len(state_change) >= 4:
            # if four square have color change in a single move, castling took place
            square_one = state_change[0]
            square_two = state_change[1]
            square_three = state_change[2]
            square_four = state_change[3]

            # check White short side castle
            if square_one.position == "e1" or square_two.position == "e1" or square_three.position == "e1" \
                    or square_four.position == "e1":
                if square_one.position == "f1" or square_two.position == "f1" or square_three.position == "f1" \
                        or square_four.position == "f1":
                    if square_one.position == "g1" or square_two.position == "g1" or square_three.position == "g1" \
                            or square_four.position == "g1":
                        if square_one.position == "h1" or square_two.position == "h1" or square_three.position == "h1" \
                                or square_four.position == "h1":
                            self.move = "e1g1"
                            print(self.move)
                            if debug:
                                square_one.draw(copy, (255, 0, 0), 2)
                                square_two.draw(copy, (255, 0, 0), 2)
                                square_three.draw(copy, (255, 0, 0), 2)
                                square_four.draw(copy, (255, 0, 0), 2)
                                cv2.imshow("previous", previous)
                                cv2.imshow("identified", copy)
                                cv2.waitKey()
                                cv2.destroyAllWindows()
                            return self.move

                # white long side castle
                if square_one.position == "d1" or square_two.position == "d1" or square_three.position == "d1" \
                        or square_four.position == "d1":
                    if square_one.position == "c1" or square_two.position == "c1" or square_three.position == "c1" \
                            or square_four.position == "c1":
                        if square_one.position == "a1" or square_two.position == "a1" or square_three.position == "a1" \
                                or square_four.position == "a1":

                            self.move = "e1c1"
                            print(self.move)
                            if debug:
                                square_one.draw(copy, (255, 0, 0), 2)
                                square_two.draw(copy, (255, 0, 0), 2)
                                square_three.draw(copy, (255, 0, 0), 2)
                                square_four.draw(copy, (255, 0, 0), 2)
                                cv2.imshow("previous", previous)
                                cv2.imshow("identified", copy)
                                cv2.waitKey(0)
                                cv2.destroyAllWindows()
                            return self.move

            # check Black short side castle
            if square_one.position == "e8" or square_two.position == "e8" or square_three.position == "e8" \
                    or square_four.position == "e8":
                if square_one.position == "f8" or square_two.position == "f8" or square_three.position == "f8" \
                        or square_four.position == "f8":
                    if square_one.position == "g8" or square_two.position == "g8" or square_three.position == "g8" \
                            or square_four.position == "g8":
                        if square_one.position == "h8" or square_two.position == "h8" or square_three.position == "h8" \
                                or square_four.position == "h8":
                            self.move = "e8g8"
                            print(self.move)
                            if debug:
                                square_one.draw(copy, (255, 0, 0), 2)
                                square_two.draw(copy, (255, 0, 0), 2)
                                square_three.draw(copy, (255, 0, 0), 2)
                                square_four.draw(copy, (255, 0, 0), 2)
                                cv2.imshow("previous", previous)
                                cv2.imshow("identified", copy)
                                cv2.waitKey(0)
                                cv2.destroyAllWindows()
                            return self.move

                # Black long side castle
                if square_one.position == "d8" or square_two.position == "d8" or square_three.position == "d8" \
                        or square_four.position == "d8":
                    if square_one.position == "c8" or square_two.position == "c8" or square_three.position == "c8" \
                            or square_four.position == "c8":
                        if square_one.position == "a8" or square_two.position == "a8" or square_three.position == "a8" \
                                or square_four.position == "a8":
                            self.move = "e8c8"
                            print(self.move)
                            if debug:
                                square_one.draw(copy, (255, 0, 0), 2)
                                square_two.draw(copy, (255, 0, 0), 2)
                                square_three.draw(copy, (255, 0, 0), 2)
                                square_four.draw(copy, (255, 0, 0), 2)
                                cv2.imshow("previous", previous)
                                cv2.imshow("identified", copy)
                                cv2.waitKey(0)
                                cv2.destroyAllWindows()
                            return self.move

        # regular move two squares change state
        square_one = largest_square
        square_two = second_largest_square

        if debug:
            square_one.draw(copy, (255, 0, 0), 2)
            square_two.draw(copy, (255, 0, 0), 2)
            cv2.imshow("previous", previous)
            # cv2.imshow("identified", copy)

        # get colors for each square from each photo
        one_curr = square_one.roiColor(current)
        two_curr = square_two.roiColor(current)
        # calculate distance from empty square color value
        sum_curr1 = 0
        sum_curr2 = 0
        for i in range(0, 3):
            sum_curr1 += (one_curr[i] - square_one.emptyColor[i]) ** 2
            sum_curr2 += (two_curr[i] - square_two.emptyColor[i]) ** 2
        dist_curr1 = math.sqrt(sum_curr1)
        dist_curr2 = math.sqrt(sum_curr2)

        if dist_curr1 < dist_curr2:
            # square 1 is closer to empty color value thus empty
            square_two.state = square_one.state
            square_one.state = '.'
            # check for promotion of a pawn
            if square_two.state.lower() == 'p':
                if square_one.position[1:2] == '2' and square_two.position[1:2] == '1':
                    self.promo = True
                if square_one.position[1:2] == '7' and square_two.position[1:2] == '8':
                    self.promo = True
                else:
                    self.promo = False
            self.move = square_one.position + square_two.position
            if debug:
                square_two.draw(copy, (0, 255, 0), 3)
                cv2.imshow('move', copy)
                cv2.waitKey(0)
                cv2.destroyAllWindows()
        else:
            # square 2 is currently empty
            square_one.state = square_two.state
            square_two.state = '.'
            # check pawn promotion
            if square_one.state.lower() == 'p':
                if square_one.position[1:2] == '1' and square_two.position[1:2] == '2':
                    self.promo = True
                if square_one.position[1:2] == '8' and square_two.position[1:2] == '7':
                    self.promo = True
                else:
                    self.promo = False
            self.move = square_two.position + square_one.position
            if debug:
                square_one.draw(copy, (0, 255, 0), 3)
                cv2.imshow('move', copy)
                cv2.waitKey(0)
                cv2.destroyAllWindows()

        return self.move
