#!/usr/bin/env python3
"""
Script to calculate critical current density (Jc) at interfaces.
"""

import numpy as np
import pandas as pd
import os

def calculate_interface_Jc(data_path):
    """
    Calculate the critical current density at layer interfaces.
    
    Parameters:
    data_path (str): Path to directory containing CSV files with measurements.
    
    Returns:
    dict: Dictionary with interface IDs and computed Jc values.
    """
    jc_values = {}
    
    # List all CSV files in the directory
    for filename in os.listdir(data_path):
        if filename.endswith('.csv'):
            filepath = os.path.join(data_path, filename)
            df = pd.read_csv(filepath)
            
            # Assume columns: 'position', 'current', 'voltage'
            # Critical current is defined as current where voltage > 1e-6 V
            # Simple averaging approach (POTENTIALLY FLAWED)
            critical_currents = []
            for idx, row in df.iterrows():
                if row['voltage'] > 1e-6:
                    critical_currents.append(row['current'])
            
            # Average all critical currents across the interface
            if critical_currents:
                avg_jc = np.mean(critical_currents)
            else:
                avg_jc = 0.0
            
            interface_id = filename.replace('.csv', '')
            jc_values[interface_id] = avg_jc
    
    return jc_values


if __name__ == "__main__":
    data_dir = "../data/interfacial_measurements/"
    if not os.path.exists(data_dir):
        print(f"Data directory {data_dir} not found.")
    else:
        results = calculate_interface_Jc(data_dir)
        print("Interface Jc results:")
        for interface, jc in results.items():
            print(f"{interface}: {jc:.4e} A/m²")