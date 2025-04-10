import math
import numpy as np
from math import sin, cos, pi
from collections import Counter

class LaminateAnalysis:
    """
    Classical Laminate Theory analysis for composite structures.
    This class handles calculation of stresses, strains, and ABD matrices.
    """
    
    def __init__(self, layup_angles, thicknesses, material_properties):
        """
        Initialize the laminate analysis with layup configuration and material properties.
        
        Parameters:
        -----------
        layup_angles : list or np.array
            Fiber orientation angles in degrees for each ply
        thicknesses : list or np.array
            Thickness of each ply in inches
        material_properties : dict
            Material properties including E11, E22, G12, V12
        """
        self.angles = np.array(layup_angles)
        self.theta = np.array(layup_angles) * pi/180  # Convert to radians
        
        # Make sure thicknesses is an array with the same length as angles
        if isinstance(thicknesses, (int, float)):
            self.t = np.full(len(self.angles), thicknesses)
        else:
            self.t = np.array(thicknesses)
            
        self.k = len(self.angles)  # Number of plies
        
        # Material properties
        self.E11 = material_properties['E11']
        self.E22 = material_properties['E22']
        self.G12 = material_properties['G12']
        self.V12 = material_properties['V12']
        self.V21 = self.V12 * self.E22 / self.E11
        
        # Initialize matrices
        self.Q = self._calculate_Q()
        self.z, self.z_m = self._calculate_z_coordinates()
        self.Q_bar = []
        self.T = []
        self.T_e = []
        
        # Calculate transformed matrices for each ply
        for i in range(self.k):
            T, T_e, Q_bar = self._calculate_transformation(self.theta[i], self.Q)
            self.T.append(T)
            self.T_e.append(T_e)
            self.Q_bar.append(Q_bar)
        
        # Calculate ABD matrices
        self.A, self.B, self.D = self._calculate_ABD_matrices()
    
    def _calculate_Q(self):
        """Calculate the reduced stiffness matrix Q."""
        return np.array([
            [self.E11/(1-self.V12*self.V21), self.V21*self.E11/(1-self.V12*self.V21), 0],
            [self.V12*self.E22/(1-self.V12*self.V21), self.E22/(1-self.V12*self.V21), 0],
            [0, 0, self.G12]
        ])
    
    def _calculate_z_coordinates(self):
        """Calculate z-coordinates for each ply."""
        t_total = np.sum(self.t)  # Total laminate thickness
        z = np.zeros((self.k, 1))
        z_m = np.zeros((self.k, 1))
        
        current_z = -t_total/2
        for i in range(self.k):
            z[i, 0] = current_z + self.t[i]
            z_m[i, 0] = current_z + self.t[i]/2
            current_z += self.t[i]
        
        return z, z_m
    
    def _calculate_transformation(self, theta_rad, Q):
        """Calculate transformation matrices and transformed reduced stiffness."""
        c = cos(theta_rad)
        s = sin(theta_rad)
        
        T = np.array([
            [c**2, s**2, 2*s*c],
            [s**2, c**2, -2*s*c],
            [-s*c, s*c, c**2 - s**2]
        ])
        
        T_e = np.array([
            [c**2, s**2, s*c],
            [s**2, c**2, -s*c],
            [-2*s*c, 2*s*c, c**2 - s**2]
        ])
        
        Q_bar = np.linalg.inv(T) @ Q @ T_e
        return T, T_e, Q_bar
    
    def _calculate_ABD_matrices(self):
        """Calculate the A, B, and D matrices."""
        A = np.zeros((3, 3))
        B = np.zeros((3, 3))
        D = np.zeros((3, 3))
        
        for i in range(3):
            for j in range(3):
                for ply in range(self.k):
                    A[i, j] += self.Q_bar[ply][i, j] * self.t[ply]
                    B[i, j] += 0.5 * self.Q_bar[ply][i, j] * (self.z[ply, 0]**2 - (self.z[ply, 0] - self.t[ply])**2)
                    D[i, j] += (1/3) * self.Q_bar[ply][i, j] * (self.z[ply, 0]**3 - (self.z[ply, 0] - self.t[ply])**3)
        
        return A, B, D
    
    def calculate_response(self, forces, moments):
        """
        Calculate midplane strains and curvatures from forces and moments.
        
        Parameters:
        -----------
        forces : np.array
            Force resultants [Nx, Ny, Nxy] in lb/in
        moments : np.array
            Moment resultants [Mx, My, Mxy] in lb-in/in
            
        Returns:
        --------
        midplane_strains : np.array
            Midplane strains [εx, εy, γxy]
        curvatures : np.array
            Curvatures [κx, κy, κxy]
        """
        # Combine forces and moments
        load_vector = np.vstack([forces.reshape(3, 1), moments.reshape(3, 1)])
        
        # Create the ABD matrix
        abd_matrix = np.block([[self.A, self.B], [self.B, self.D]])
        
        # Solve for strains and curvatures
        result = np.linalg.solve(abd_matrix, load_vector)
        
        midplane_strains = result[:3]
        curvatures = result[3:]
        
        return midplane_strains, curvatures
    
    def calculate_ply_strains_stresses(self, midplane_strains, curvatures, ply_number):
        """
        Calculate strains and stresses for a specific ply.
        
        Parameters:
        -----------
        midplane_strains : np.array
            Midplane strains [εx, εy, γxy]
        curvatures : np.array
            Curvatures [κx, κy, κxy]
        ply_number : int
            Ply number (1-based indexing)
            
        Returns:
        --------
        global_strain : np.array
            Global strains at ply [εx, εy, γxy]
        global_stress : np.array
            Global stresses at ply [σx, σy, τxy]
        local_strain : np.array
            Local strains at ply [ε1, ε2, γ12]
        local_stress : np.array
            Local stresses at ply [σ1, σ2, τ12]
        """
        # Adjust for 0-based indexing
        ply_idx = ply_number - 1
        
        # Calculate global strains and stresses
        global_strain = midplane_strains + self.z_m[ply_idx, 0] * curvatures
        global_stress = self.Q_bar[ply_idx] @ global_strain
        
        # Transform to local coordinates
        local_strain = self.T_e[ply_idx] @ global_strain
        local_stress = self.T[ply_idx] @ global_stress
        
        return global_strain, global_stress, local_strain, local_stress
    
    def get_engineering_constants(self):
        """
        Calculate effective engineering constants of the laminate.
        
        Returns:
        --------
        dict
            Dictionary containing Ex, Ey, Gxy, vxy, and vyx
        """
        t_total = np.sum(self.t)
        
        # Calculate engineering constants
        Ex = (self.A[0, 0] / t_total) * (1 - (self.A[0, 1]**2 / (self.A[0, 0] * self.A[1, 1])))
        Ey = (self.A[1, 1] / t_total) * (1 - (self.A[0, 1]**2 / (self.A[0, 0] * self.A[1, 1])))
        Gxy = self.A[2, 2] / t_total
        vxy = self.A[0, 1] / self.A[1, 1]
        vyx = self.A[0, 1] / self.A[0, 0]
        
        return {
            'Ex': Ex,
            'Ey': Ey,
            'Gxy': Gxy,
            'vxy': vxy,
            'vyx': vyx
        }
    
    def analyze_layup_distribution(self):
        """
        Analyze the distribution of angles in the layup.
        
        Returns:
        --------
        dict
            Dictionary containing angle counts and percentages
        """
        angle_counts = Counter(self.angles)
        total_plies = len(self.angles)
        
        # Calculate standard angle percentages
        percentages = {
            '0_deg': (angle_counts[0] / total_plies) * 100,
            '45_deg': ((angle_counts[45] + angle_counts[-45]) / total_plies) * 100,
            '90_deg': (angle_counts[90] / total_plies) * 100
        }
        
        return {
            'counts': angle_counts,
            'percentages': percentages,
            'total_plies': total_plies
        }
