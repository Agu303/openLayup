
def calcLamProps(input_angles, material_index):
    import math
    import numpy as np
    from math import sin, cos, pi
    import matplotlib.pyplot as plt
    from collections import Counter
    
    # Define Material Here
    M = 0
    t = 0.005
    # Define angle here:
    N = 1  # ply to test for local strain/stress
    max_strains = np.array([[0.0041],
                            [0.0041],
                            [0.007]])
    # Input max strain
    theta = np.transpose(np.array([input_angles]) * pi/180)
    k = len(theta)  # number of plies
    thickness = np.transpose(np.array([[t, t, t, t, t, t, t, t]]))
    # define known condition x, y, shear planes - enter in psi
    known_stresses = np.array([[6251.9936],
                               [0],
                               [2500.176],
                               [0],
                               [0],
                               [0]])
    
    
    # Units are in kpsi
    Material = [["T300/5208_graphite_epoxy"],
                ["B(4)/5505_boron_epoxy"],
                ["AS/3501_graphite_epoxy"],
                ["Scotchply_1002_glass_epoxy"],
                ["Kevlar49_aramid_epoxy"]]
    # Modulus along the fibers
    E11 = np.array([[26.25],
                    [29.59],
                    [20.01],
                    [5.6],
                    [11.02]])
    # Modulus accross the fibers
    E22 = np.array([[1.49],
                    [2.68],
                    [1.3],
                    [1.2],
                    [0.8]])
    # Shear Modulus
    G12 = np.array([[1.04],
                    [0.81],
                    [1.03],
                    [0.6],
                    [0.33]])
    
    # Poisson's ratio
    V12 = np.array([[0.28],
                    [0.23],
                    [0.3],
                    [0.26],
                    [0.34],
                    [0.33]])
    
    Max_stress = np.array([[217.5, 217.5, 5.8, 35.7, 9.86],
                           [182.7, 362.5, 8.85, 29.3, 9.72],
                           [209.9, 209.9, 7.5, 29.9, 13.5],
                           [154, 88.5, 4.5, 17.1, 10.4],
                           [203, 34.1, 1.74, 7.69, 4.93]])
    
    
    Max_strain = np.array([[0.00829, -0.00829, 0.00389, -0.02396, 0.00948],
                           [0.00617, -0.01225, 0.00330, -0.01093, 0.0120],
                           [0.01049, -0.01049, 0.00577, -0.0230, 0.01311],
                           [0.0275, -0.0158, 0.00375, -0.01425, 0.01733],
                           [0.01842, -0.00309, 0.00217, -0.00961, 0.01494]])
    
    
    E11, E22, G12, V12 = E11[M, 0] * 10**6, E22[M, 0] * \
        10**6, G12[M, 0]*10**6, V12[M, 0]
    V21 = V12 * E22 / E11
    Q = np.array([[E11/(1-V12*V21), V21*E11/(1-V12*V21), 0],
                 [V12*E22/(1-V12*V21), E22/(1-V12*V21), 0],
                 [0, 0, G12]
                  ])
    Q_list.append(Q)
    
    def calculate_T_Q(theta, Q):
        theta_scalar = theta.item()  # Convert to a scalar
        T = np.array([
            [cos(theta_scalar)**2, sin(theta_scalar)**2, 2*sin(theta_scalar)*cos(theta_scalar)],
            [sin(theta_scalar)**2, cos(theta_scalar)**2, -2*sin(theta_scalar)*cos(theta_scalar)],
            [-sin(theta_scalar)*cos(theta_scalar), sin(theta_scalar)*cos(theta_scalar), cos(theta_scalar)**2 - sin(theta_scalar)**2]
        ])
    
        T_e = np.array([
            [cos(theta_scalar)**2, sin(theta_scalar)**2, sin(theta_scalar)*cos(theta_scalar)],
            [sin(theta_scalar)**2, cos(theta_scalar)**2, -sin(theta_scalar)*cos(theta_scalar)],
            [-2*sin(theta_scalar)*cos(theta_scalar), 2*sin(theta_scalar)*cos(theta_scalar), cos(theta_scalar)**2 - sin(theta_scalar)**2]
        ])
        Q_bar = np.linalg.inv(T) @ Q @ T_e
        return T, T_e, Q_bar
    
    
    def T_convert(theta):
        theta_scalar = theta.item()  # Convert to a scalar
        T = np.array([
            [cos(theta_scalar)**2, sin(theta_scalar)**2, 2*sin(theta_scalar)*cos(theta_scalar)],
            [sin(theta_scalar)**2, cos(theta_scalar)**2, -2*sin(theta_scalar)*cos(theta_scalar)],
            [-sin(theta_scalar)*cos(theta_scalar), sin(theta_scalar)*cos(theta_scalar), cos(theta_scalar)**2 - sin(theta_scalar)**2]
        ])
    
        T_e = np.array([
            [cos(theta_scalar)**2, sin(theta_scalar)**2, sin(theta_scalar)*cos(theta_scalar)],
            [sin(theta_scalar)**2, cos(theta_scalar)**2, -sin(theta_scalar)*cos(theta_scalar)],
            [-2*sin(theta_scalar)*cos(theta_scalar), 2*sin(theta_scalar)*cos(theta_scalar), cos(theta_scalar)**2 - sin(theta_scalar)**2]
        ])
        return T, T_e
    
    
    def calc_zs(t, k):
        tlam = t * k  # total thickness
        # get z - upper ply surface
        z, z_m = np.zeros((k, 1)), np.zeros((k, 1))
        for i in range(k):
            z[i, 0] = -tlam*0.5 + t*(i+1)
            z_m[i, 0] = -0.5*(tlam - t) + (i*t)
        return z, z_m
    def calc_max_locals(laminate_curvatures,midplane_strains, Q_bar, k):
        for i in range(k):
            global_strain_ply = midplane_strains + z_m[N-1][0] * laminate_curvatures
            global_stress_ply = Q_bar[N-1] @ global_strain_ply
        
        return global_strain_ply, global_stress_ply
    
    # Define z & z_m matrices
    z, z_m = calc_zs(t, k)
    
    T_num = []
    T_enum = []
    Q_bar = []
    for i in range(k):
        update_Ts_Q = calculate_T_Q(theta[i, 0], Q)
        T_num.append(update_Ts_Q[0])
        T_enum.append(update_Ts_Q[1])
        Q_bar.append(update_Ts_Q[2])
    
    
    # Calculate A matrix
    A, B, D = np.zeros((3, 3)), np.zeros((3, 3)), np.zeros((3, 3))
    for i in range(3):
        for j in range(3):
            A_sum, B_sum, D_sum = 0, 0, 0
            for ply in range(k):
                A_sum = A_sum + Q_bar[ply][i, j]
                B_sum = B_sum + Q_bar[ply][i, j] * \
                    (z[ply, 0]**2 - (z[ply, 0] - t)**2)
                D_sum = D_sum + Q_bar[ply][i, j] * \
                    (z[ply, 0]**3 - (z[ply, 0] - t)**3)
            A[i, j] = A_sum * t
            B[i, j] = 0.5 * B_sum
            D[i, j] = D_sum / 3
    
    augmented_matrix = np.block([[A, B], [B, D]])
    
    
    # Solve midplane strains and curvatures
    total = np.linalg.inv(augmented_matrix) @ known_stresses
    midplane_strains = total[:3]
    laminate_curvatures = total[-3:]
    
    # determine stresses/strains in global coordinates at # ply
    T, T_e = T_convert(theta[N-1])
    
    global_strain_ply = midplane_strains + z_m[N-1][0] * laminate_curvatures
    global_stress_ply = Q_bar[N-1] @ global_strain_ply
    
    #### Conversion to local strain ###
    local_strain_ply = T_e @ global_strain_ply
    local_stress_ply = T @ global_stress_ply
    
    
    print("The global strains are:", np.array([f"{num:.5f}" for num in global_strain_ply.flatten()]), "\n")
    
    angle_counts = Counter(input_angles)
    percentages = [
        (angle_counts[0] / k) * 100,     # Percentage of 0 degrees
        (angle_counts[45] + angle_counts[-45])/k * 100,    # Percentage of 45 degrees
        (angle_counts[90] / k) * 100     # Percentage of 90 degrees
    ]
    
    print("The layup configuration (",k,"plies):\n",input_angles)
    # Display the formatted list
    print("Percentage layup breakdown (",angle_counts[0],angle_counts[45] + angle_counts[-45],angle_counts[90], "):\n",[f"{p:.2f}%" for p in percentages],"\n")
    ### Calculate Modulus of Elasticity constants ####
    E_xx = (A[0][0] / (k * t)) * (1 - A[0][1]**2 / (A[0][0] * A[1][1]))
    E_yy = (A[1][1] / (k * t)) * (1 - A[0][1]**2 / (A[0][0] * A[1][1]))
    G_xy = A[2][2] / (k * t)
    Ezz_list.append(E_xx)
    G_xy_list.append(G_xy)
    print('Ezz for this layup is:', E_xx)
    print('Gxy for this layup is:', G_xy)

half_input_angles = [0,0,0,0,0,0,0,45,-45,90]
total_angles = half_input_angles + half_input_angles[::-1]
result = calcLamProps(total_angles, material_index = 0)

'''
t = 0.005
W = 4.2
H = 5
a = 0.6 #in
My = -6000 #in-lb
Mz = 20000 #in-lb
Vy = 3000
Vz = 0 
P = 1000 #lb
h1 = total_angles*t
Er = 10*(10**6)

find: [Nxx, Nyy, Nxy, Mxx, Myy, Mxy]
'''
