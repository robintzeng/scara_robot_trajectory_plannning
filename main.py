import inv_kinect
import generate_param
import canvas
import numpy as np
import pygame as pg
# Time interval
Tint = 0.05

# parabolic time interval
tp = 0.2

# Goal matrix
#               T   x    y   theta
TQ = np.array([[0,  50,  0,   90],
               [1,  0,   50,  90],
               [2, -100, 0,   10],
               [3, -60,  30,  90]], dtype=float)
# parabolic blends time
P = tp*np.ones((TQ.shape[0], 1), dtype=float)
# Overall Goal Matrix
G = np.concatenate((TQ, P), axis=1)
# link length
l1 = 100
l2 = 100

spit_time, points = generate_param.para_points(G, Tint)
joint_angle = inv_kinect.inv_kinect(
    points[:, 0], points[:, 1], points[:, 2], l1, l2)*180/np.pi

pg.init()
canvas.auto_mode(joint_angle, l1, l2)
pg.quit()
