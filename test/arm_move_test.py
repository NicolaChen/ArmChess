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
#            pos_mat[i][j] = [152 + 15 + 38 * (0.5 + j), 140 - 15 * (0.5 + i)]
#        else:
#            pos_mat[i][j] = [152 + 15 + 41 * (0.5 + j), 140 - 37.5 * (0.5 + i)]

pos_mat = np.load('cbm_0908.npy')

i = 0
j = 0     
while True:
    if j == 4:
        break
    arm.armMove([pos_mat[i][j][0], pos_mat[i][j][1], 150])
    arm.armMove([pos_mat[i][j][0], pos_mat[i][j][1], 30])
    arm.armMove([pos_mat[i][j][0], pos_mat[i][j][1], 15])
    while True:
        dnd_in = input("Array of direction and distance, for example [0, 30]\r\n")
        if dnd_in == '' or dnd_in == 'n':
            break
        dnd = eval(dnd_in)
        pos_mat[i][j][dnd[0]] += dnd[1]
        arm.armMove([200, 0, 150])
        arm.armMove([pos_mat[i][j][0], pos_mat[i][j][1], 150])
        arm.armMove([pos_mat[i][j][0], pos_mat[i][j][1], 30])
        arm.armMove([pos_mat[i][j][0], pos_mat[i][j][1], 15])
    arm.armMove([200, 0, 150])
    time.sleep(1)

    arm.armMove([pos_mat[7 - i][7 - j][0], pos_mat[7 - i][7 - j][1], 150])
    arm.armMove([pos_mat[7 - i][7 - j][0], pos_mat[7 - i][7 - j][1], 30])
    arm.armMove([pos_mat[7 - i][7 - j][0], pos_mat[7 - i][7 - j][1], 15])
    while True:
        dnd_in = input("Array of direction and distance, for example [0, 30]\r\n")
        if dnd_in == '' or dnd_in == 'n':
            break
        dnd = eval(dnd_in)
        pos_mat[7 - i][7 - j][dnd[0]] += dnd[1]
        arm.armMove([200, 0, 150])
        arm.armMove([pos_mat[7 - i][7 - j][0], pos_mat[7 - i][7 - j][1], 150])
        arm.armMove([pos_mat[7 - i][7 - j][0], pos_mat[7 - i][7 - j][1], 30])
        arm.armMove([pos_mat[7 - i][7 - j][0], pos_mat[7 - i][7 - j][1], 15])
    arm.armMove([200, 0, 150])
    time.sleep(1)
    if i == 7:
        i = 0
        j += 1
        continue

    i += 1

np.save("chess_board_matrix_V3.npy", pos_mat)

print("Matrix saved!")
