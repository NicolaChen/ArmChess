import time
import sys
import numpy as np
sys.path.append('..')

from Arm.ArmMove import *

arm = ArmMove()

print("Done")
# time.sleep(5)
# arm.armCSInit()

# pos_mat = np.zeros((8, 8, 2))

#for i in range(8):
#    for j in range(8):
#        if j < 4:
#            pos_mat[i][j] = [152 + 20 + 38 * (0.5 + j), 140 - 35 * (0.5 + i)]
#        else:
#            pos_mat[i][j] = [152 + 20 + 41 * (0.5 + j), 140 - 37.5 * (0.5 + i)]

pos_mat = np.load('chess_board_matrix.npy')

i = 0
j = 0     
while True:
    if j == 4:
        break
    arm.armMove([pos_mat[i][j][0], pos_mat[i][j][1], 10])

#    if input("Adjust [%d, %d]\r\n" % (i, j)) == 'y':
    while True:
        dnd_in = input("Array of direction and distance, for example [0, 30]\r\n")
        if dnd_in == '' or dnd_in == 'n':
            break
        dnd = eval(dnd_in)
        pos_mat[i][j][dnd[0]] += dnd[1]
        arm.armMove([315, 0, 50])
        arm.armMove([pos_mat[i][j][0], pos_mat[i][j][1], 10])

    arm.armMove([pos_mat[7 - i][7 - j][0], pos_mat[7 - i][7 - j][1], 10])

#    if input("Adjust [%d, %d]\r\n" % (7 - i, 7 - j)) == 'y':
    while True:
        dnd_in = input("Array of direction and distance, for example [0, 30]\r\n")
        if dnd_in == '' or dnd_in == 'n':
            break
        dnd = eval(dnd_in)
        pos_mat[7 - i][7 - j][dnd[0]] += dnd[1]
        arm.armMove([315, 0, 50])
        arm.armMove([pos_mat[7 - i][7 - j][0], pos_mat[7 - i][7 - j][1], 10])

    if i == 7:
        i = 0
        j += 1
        continue

    i += 1
    np.save("chess_board_matrix.npy", pos_mat)

print("Matrix saved!")

#    arm.armMove([295, 0, 10])
#    time.sleep(2)
#    arm.armMove([152, -140, 10])
#    time.sleep(2)
#    arm.armMove([300, -150, 10])
#    time.sleep(2)
#    arm.armMove([468, -160, 10])
#    time.sleep(2)
#    arm.armMove([468, 0, 10])
#    time.sleep(2)
#    arm.armMove([468, 150, 10])
#    time.sleep(2)
#    arm.armMove([305, 140, 10])
#    time.sleep(2)
#    arm.armMove([152, 140, 10])
#    time.sleep(2)
#    arm.armMove([450, 0, 10])
#    time.sleep(2)
#    arm.armMove([450, -130, 10])
#    time.sleep(2)
#    arm.armMove([450, 130, 10])
#    time.sleep(2)
#    arm.armMove([450, 0, 10])
#    time.sleep(2)
