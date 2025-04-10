import json
import os
import numpy as np

class Material:
    """
    Class to handle composite material properties.
    """
    
    def __init__(self, name, properties):
        """
        Initialize a material with its properties.
        
        Parameters:
        -----------
        name : str
            Name of the material
        properties : dict
            Dictionary containing material properties
        """
        self.name = name
        self.properties = properties
    
    @classmethod
    def from_dict(cls, data):
        """Create a material from a dictionary."""
        return cls(data['name'], data['properties'])
    
    def to_dict(self):
        """Convert material to dictionary for saving to JSON."""
        return {
            'name': self.name,
            'properties': self.properties
        }

class MaterialDatabase:
    """
    Class to manage the database of composite materials.
    """
    
    def __init__(self, database_path=None):
        """
        Initialize the material database.
        
        Parameters:
        -----------
        database_path : str
            Path to the JSON material database file
        """
        self.materials = {}
        
        if database_path and os.path.exists(database_path):
            self.load_database(database_path)
        else:
            # Initialize with default materials
            self._init_default_materials()
    
    def _init_default_materials(self):
        """Initialize with some default composite materials."""
        default_materials = {
            "T300/5208_graphite_epoxy": {
                "properties": {
                    "E11": 26.25e6,  # psi
                    "E22": 1.49e6,   # psi
                    "G12": 1.04e6,   # psi
                    "V12": 0.28,
                    "max_stress": [217.5e3, 217.5e3, 5.8e3, 35.7e3, 9.86e3],  # psi
                    "max_strain": [0.00829, -0.00829, 0.00389, -0.02396, 0.00948]
                }
            },
            "B(4)/5505_boron_epoxy": {
                "properties": {
                    "E11": 29.59e6,  # psi
                    "E22": 2.68e6,   # psi
                    "G12": 0.81e6,   # psi
                    "V12": 0.23,
                    "max_stress": [182.7e3, 362.5e3, 8.85e3, 29.3e3, 9.72e3],  # psi
                    "max_strain": [0.00617, -0.01225, 0.00330, -0.01093, 0.0120]
                }
            },
            "AS/3501_graphite_epoxy": {
                "properties": {
                    "E11": 20.01e6,  # psi
                    "E22": 1.3e6,   # psi
                    "G12": 1.03e6,   # psi
                    "V12": 0.3,
                    "max_stress": [209.9, 209.9, 7.5, 29.9, 13.5],  # psi
                    "max_strain": [0.01049, -0.01049, 0.00577, -0.0230, 0.01311]
                }
            },
           "Scotchply_1002_glass_epoxy": {
                "properties": {
                    "E11": 5.6e6,  # psi
                    "E22": 1.2e6,   # psi
                    "G12": 0.6e6,   # psi
                    "V12": 0.26,
                    "max_stress":  [154, 88.5, 4.5, 17.1, 10.4],  # psi
                    "max_strain": [0.0275, -0.0158, 0.00375, -0.01425, 0.01733]
                }
            },
            "Kevlar49_aramid_epoxy": {
                "properties": {
                    "E11": 11.02e6,  # psi
                    "E22": 0.8e6,   # psi
                    "G12": 0.33e6,   # psi
                    "V12": 0.34,
                    "max_stress":  [203, 34.1, 1.74, 7.69, 4.93],  # psi
                    "max_strain": [0.01842, -0.00309, 0.00217, -0.00961, 0.01494]
                }
            }


        }
        
        for name, data in default_materials.items():
            self.materials[name] = Material(name, data["properties"])
    
    def load_database(self, database_path):
        """
        Load materials from a JSON database file.
        
        Parameters:
        -----------
        database_path : str
            Path to the JSON material database file
        """
        try:
            with open(database_path, 'r') as f:
                data = json.load(f)
                
            for name, material_data in data.items():
                self.materials[name] = Material.from_dict({"name": name, **material_data})
                
        except (json.JSONDecodeError, FileNotFoundError) as e:
            print(f"Error loading material database: {e}")
            # Initialize with defaults if loading fails
            self._init_default_materials()
    
    def save_database(self, database_path):
        """
        Save the material database to a JSON file.
        
        Parameters:
        -----------
        database_path : str
            Path to save the JSON material database file
        """
        data = {}
        for name, material in self.materials.items():
            data[name] = material.to_dict()
            
        try:
            # Ensure directory exists
            os.makedirs(os.path.dirname(database_path), exist_ok=True)
            
            with open(database_path, 'w') as f:
                json.dump(data, f, indent=4)
                
        except Exception as e:
            print(f"Error saving material database: {e}")
    
    def get_material(self, name):
        """
        Get a material by name.
        
        Parameters:
        -----------
        name : str
            Name of the material
            
        Returns:
        --------
        Material or None
            Material object or None if not found
        """
        return self.materials.get(name)
    
    def add_material(self, material):
        """
        Add a material to the database.
        
        Parameters:
        -----------
        material : Material
            Material object to add
        """
        self.materials[material.name] = material
    
    def delete_material(self, name):
        """
        Delete a material from the database.
        
        Parameters:
        -----------
        name : str
            Name of the material to delete
            
        Returns:
        --------
        bool
            True if deleted, False if not found
        """
        if name in self.materials:
            del self.materials[name]
            return True
        return False
    
    def get_material_names(self):
        """
        Get a list of all material names.
        
        Returns:
        --------
        list
            List of material names
        """
        return list(self.materials.keys())
