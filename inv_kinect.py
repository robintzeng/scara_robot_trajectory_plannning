import numpy as np


def inv_kinect(Xcoor, Ycoor, theta, l1, l2):
    n = Xcoor.shape[0]
    q = np.zeros((n, 3))

    q[:, 1] = np.arccos((Xcoor**2 + Ycoor**2 - l1 **
                         2 - l2**2)/(2*l1*l2))

    psi = np.arccos((Xcoor**2 + Ycoor**2 + l1**2 - l2 **
                     2)/(2*l1*(np.sqrt(Xcoor**2 + Ycoor**2))))

    q[:, 0] = np.where(q[:, 1] < 0,
                       np.arctan2(Ycoor, Xcoor)+psi,
                       np.arctan2(Ycoor, Xcoor)-psi)
    q[:, 2] = theta*(np.pi/180)-q[:, 0]-q[:, 1]

    return q
