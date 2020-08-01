import numpy as np


def para_points(G, Tint):
    T = G[:, 0].reshape(-1, 1)
    Q = G[:, 1:-1]
    P = G[:, -1].reshape(-1, 1)

    PT = Q.shape[0]
    DOF = Q.shape[1]
    spilt_time = np.linspace(T[0], T[-1], int((T[-1]-T[0])/Tint) +
                             1).astype('float16').reshape(-1, 1)
    N = spilt_time.shape[0]

    T_onlyforV = np.array(T)

    T_onlyforV[0] = T_onlyforV[0] + P[0]*0.5
    T_onlyforV[-1] = T_onlyforV[-1] - P[-1]*0.5

    V = np.zeros((PT+1, DOF))

    for i in range(DOF):
        tmp = (np.diff(Q[:, i]).reshape(-1, 1) /
               np.diff(T_onlyforV, axis=0)).reshape(-1)
        V[1: -1, i] = tmp

    A = np.diff(V, axis=0)/P  # accer

    ZeroInM = np.zeros((2*(PT-2)+1+2, PT))

    for i in range(1, PT+1):
        ZeroInM[(i*2)-1-1, i-1] = 1

    A = np.dot(ZeroInM, A)

    points = np.zeros((N, DOF+1))
    TS = np.zeros(PT*2)

    T = T.reshape(-1)
    P = P.reshape(-1)
    TS[0] = T[0]
    TS[1] = T[0] + P[0]
    TS[-2] = T[-1] - P[-1]
    TS[-1] = T[-1]

    for i in range(2, PT):
        TS[i*2-1-1] = T[i-1]-P[i-1]/2
        TS[i*2-1] = T[i-1]+P[i-1]/2

    tStep = 2
    Ind = 2     # %2:Parabolic 2: Linear; Initial:2

    tStep = 2
    Ind = 2

    Q_a = np.append(Q[0, :], 2)
    points[0, :] = Q_a
    acc = A[0, :]
    velo = np.zeros_like(acc)

    for i in range(1, N):
        points[i, -1] = Ind
        points[i, 0: -1] = points[i-1, 0: -1] + velo*Tint + acc*(Tint**2)/2
        velo = velo + acc*Tint
        if(spilt_time[i] == TS[tStep-1]) and (i < N-1):
            acc = A[tStep-1, :]
            tStep = tStep + 1
            Ind = 2-Ind

    return spilt_time, points


if __name__ == "__main__":
    genParaPoints(G, Tint)
