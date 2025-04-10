import numpy as np
import json
import os

class Component:
    """
    Base class for aerospace structural components.
    """
    
    def __init__(self, name, component_type, geometry, layup_angles, ply_thickness=0.005, material_name=None):
        """
        Initialize a component.
        
        Parameters:
        -----------
        name : str
            Name of the component
        component_type : str
            Type of component (e.g., 'nosecone', 'airframe', 'fin')
        geometry : dict
            Geometry parameters specific to the component type
        layup_angles : list
            List of fiber orientation angles for each ply
        ply_thickness : float or list
            Thickness of each ply (inches)
        material_name : str
            Name of the material
        """
        self.name = name
        self.component_type = component_type
        self.geometry = geometry
        self.layup_angles = layup_angles
        
        # Handle single thickness or list of thicknesses
        if isinstance(ply_thickness, (int, float)):
            self.ply_thickness = [ply_thickness] * len(layup_angles)
        else:
            self.ply_thickness = ply_thickness
            
        self.material_name = material_name
        self.results = None  # Store analysis results
    
    @classmethod
    def from_dict(cls, data):
        """Create a component from a dictionary."""
        return cls(
            data['name'],
            data['component_type'],
            data['geometry'],
            data['layup_angles'],
            data.get('ply_thickness', 0.005),
            data.get('material_name')
        )
    
    def to_dict(self):
        """Convert component to dictionary for saving to JSON."""
        return {
            'name': self.name,
            'component_type': self.component_type,
            'geometry': self.geometry,
            'layup_angles': self.layup_angles,
            'ply_thickness': self.ply_thickness,
            'material_name': self.material_name
        }
    
    def get_loads(self, flight_conditions):
        """
        Calculate loads on the component based on flight conditions.
        This is a base method to be overridden by subclasses.
        
        Parameters:
        -----------
        flight_conditions : dict
            Dictionary of flight conditions (velocity, pressure, etc.)
            
        Returns:
        --------
        dict
            Dictionary of forces and moments
        """
        raise NotImplementedError("Subclasses must implement get_loads()")


class NoseCone(Component):
    """
    Nose cone component for aerospace structures.
    """
    
    def __init__(self, name, geometry, layup_angles, ply_thickness=0.005, material_name=None):
        """
        Initialize a nose cone component.
        
        Parameters:
        -----------
        name : str
            Name of the component
        geometry : dict
            Geometry parameters for nose cone:
            - shape: str (e.g., 'ogive', 'conical', 'elliptical')
            - length: float (inches)
            - base_diameter: float (inches)
            - additional shape-specific parameters
        layup_angles : list
            List of fiber orientation angles for each ply
        ply_thickness : float or list
            Thickness of each ply (inches)
        material_name : str
            Name of the material
        """
        super().__init__(name, 'nosecone', geometry, layup_angles, ply_thickness, material_name)
    
    def get_loads(self, flight_conditions):
        """
        Calculate loads on the nose cone based on flight conditions.
        
        Parameters:
        -----------
        flight_conditions : dict
            Dictionary of flight conditions:
            - velocity: float (ft/s)
            - density: float (slug/ft³)
            - angle_of_attack: float (degrees)
            
        Returns:
        --------
        dict
            Dictionary of forces and moments:
            - forces: np.array [Nx, Ny, Nxy] (lb/in)
            - moments: np.array [Mx, My, Mxy] (lb-in/in)
        """
        # Simple aerodynamic pressure calculation
        velocity = flight_conditions['velocity']
        density = flight_conditions['density']
        aoa = np.radians(flight_conditions['angle_of_attack'])
        
        # Dynamic pressure
        q = 0.5 * density * (velocity**2)
        
        # Convert to appropriate units (assuming ft/s to lb/in²)
        q = q / 144.0  # Convert from lb/ft² to lb/in²
        
        # Calculate rough pressure distribution (simplified)
        length = self.geometry['length']
        diameter = self.geometry['base_diameter']
        
        # Approximate normal force per unit area
        N_normal = q * np.sin(aoa)
        
        # Approximate axial force per unit area
        N_axial = q * np.cos(aoa)
        
        # Simplified conversion to membrane forces (lb/in)
        forces = np.array([
            N_axial,
            N_normal,
            0.0  # Assuming no in-plane shear for simplicity
        ])
        
        # Simplified moments (would require more detailed analysis in reality)
        moments = np.array([
            0.0,  # Mx
            N_normal * diameter / 4,  # My (simplified bending)
            0.0   # Mxy
        ])
        
        return {
            'forces': forces,
            'moments': moments
        }


class CylindricalAirframe(Component):
    """
    Cylindrical airframe component for aerospace structures.
    """
    
    def __init__(self, name, geometry, layup_angles, ply_thickness=0.005, material_name=None):
        """
        Initialize a cylindrical airframe component.
        
        Parameters:
        -----------
        name : str
            Name of the component
        geometry : dict
            Geometry parameters for cylindrical airframe:
            - length: float (inches)
            - diameter: float (inches)
            - additional parameters
        layup_angles : list
            List of fiber orientation angles for each ply
        ply_thickness : float or list
            Thickness of each ply (inches)
        material_name : str
            Name of the material
        """
        super().__init__(name, 'airframe', geometry, layup_angles, ply_thickness, material_name)
    
    def get_loads(self, flight_conditions):
        """
        Calculate loads on the cylindrical airframe based on flight conditions.
        
        Parameters:
        -----------
        flight_conditions : dict
            Dictionary of flight conditions:
            - velocity: float (ft/s)
            - density: float (slug/ft³)
            - axial_load: float (lb)
            - bending_moment: float (lb-in)
            
        Returns:
        --------
        dict
            Dictionary of forces and moments:
            - forces: np.array [Nx, Ny, Nxy] (lb/in)
            - moments: np.array [Mx, My, Mxy] (lb-in/in)
        """
        # Get geometry parameters
        diameter = self.geometry['diameter']
        radius = diameter / 2
        
        # Get loads
        axial_load = flight_conditions.get('axial_load', 0)
        bending_moment = flight_conditions.get('bending_moment', 0)
        internal_pressure = flight_conditions.get('internal_pressure', 0)
        
        # Circumferential force due to internal pressure
        N_theta = internal_pressure * radius
        
        # Axial force due to axial load
        circumference = np.pi * diameter
        N_axial = axial_load / circumference
        
        # Additional axial force due to bending
        N_bending = (bending_moment * radius) / (np.pi * radius**3)
        
        # Combine axial forces
        forces = np.array([
            N_axial + N_bending,  # Nx (axial)
            N_theta,              # Ny (circumferential)
            0.0                   # Nxy (in-plane shear)
        ])
        
        # Simplified moments (would require more detailed analysis in reality)
        moments = np.array([
            0.0,  # Mx
            0.0,  # My
            0.0   # Mxy
        ])
        
        return {
            'forces': forces,
            'moments': moments
        }


class Fin(Component):
    """
    Fin component for aerospace structures.
    """
    
    def __init__(self, name, geometry, layup_angles, ply_thickness=0.005, material_name=None):
        """
        Initialize a fin component.
        
        Parameters:
        -----------
        name : str
            Name of the component
        geometry : dict
            Geometry parameters for fin:
            - root_chord: float (inches)
            - tip_chord: float (inches)
            - span: float (inches)
            - sweep: float (degrees)
            - additional parameters
        layup_angles : list
            List of fiber orientation angles for each ply
        ply_thickness : float or list
            Thickness of each ply (inches)
        material_name : str
            Name of the material
        """
        super().__init__(name, 'fin', geometry, layup_angles, ply_thickness, material_name)
    
    def get_loads(self, flight_conditions):
        """
        Calculate loads on the fin based on flight conditions.
        
        Parameters:
        -----------
        flight_conditions : dict
            Dictionary of flight conditions:
            - velocity: float (ft/s)
            - density: float (slug/ft³)
            - angle_of_attack: float (degrees)
            
        Returns:
        --------
        dict
            Dictionary of forces and moments:
            - forces: np.array [Nx, Ny, Nxy] (lb/in)
            - moments: np.array [Mx, My, Mxy] (lb-in/in)
        """
        # Simple aerodynamic load calculation
        velocity = flight_conditions['velocity']
        density = flight_conditions['density']
        aoa = np.radians(flight_conditions['angle_of_attack'])
        
        # Dynamic pressure
        q = 0.5 * density * (velocity**2)
        
        # Convert to appropriate units (assuming ft/s to lb/in²)
        q = q / 144.0  # Convert from lb/ft² to lb/in²
        
        # Get geometry parameters
        root_chord = self.geometry['root_chord']
        span = self.geometry['span']
        
        # Simplified load calculations
        # Assuming fin as a flat plate at angle of attack
        normal_pressure = q * np.sin(aoa) * np.cos(aoa)
        
        # Convert to membrane forces (lb/in)
        # For a fin, primarily bending loads
        forces = np.array([
            0.0,   # Nx
            0.0,   # Ny
            normal_pressure / 2  # Approximate shear flow
        ])
        
        # Simplified moments (would require more detailed analysis in reality)
        moments = np.array([
            0.0,   # Mx
            normal_pressure * span / 2,  # My (bending)
            0.0    # Mxy
        ])
        
        return {
            'forces': forces,
            'moments': moments
        }


class ComponentDatabase:
    """
    Class to manage component presets database.
    """
    
    def __init__(self, database_path=None):
        """
        Initialize the component database.
        
        Parameters:
        -----------
        database_path : str
            Path to the JSON component database file
        """
        self.components = {}
        
        if database_path and os.path.exists(database_path):
            self.load_database(database_path)
        else:
            # Initialize with default components
            self._init_default_components()
    
    def _init_default_components(self):
        """Initialize with some default component presets."""
        # Define some default presets
        default_components = {
            "Standard Nosecone": {
                "component_type": "nosecone",
                "geometry": {
                    "shape": "ogive",
                    "length": 24.0,
                    "base_diameter": 6.0
                },
                "layup_angles": [0, 45, -45, 90, 90, -45, 45, 0],
                "ply_thickness": 0.005,
                "material_name": "T300/5208_graphite_epoxy"
            },
            "Standard Airframe": {
                "component_type": "airframe",
                "geometry": {
                    "length": 48.0,
                    "diameter": 6.0
                },
                "layup_angles": [0, 45, -45, 90, 90, -45, 45, 0],
                "ply_thickness": 0.005,
                "material_name": "T300/5208_graphite_epoxy"
            },
            "Standard Fin": {
                "component_type": "fin",
                "geometry": {
                    "root_chord": 12.0,
                    "tip_chord": 6.0,
                    "span": 6.0,
                    "sweep": 30.0
                },
                "layup_angles": [0, 45, -45, 90, 90, -45,
