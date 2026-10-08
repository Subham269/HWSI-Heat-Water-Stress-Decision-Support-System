import numpy as np
from typing import List, Tuple

def compute_ahp_weights(matrix: List[List[float]]) -> Tuple[np.ndarray, float]:
    """
    Compute AHP weights from pairwise matrix using eigenvalue method.
    Returns (weights, CR).
    """
    mat = np.array(matrix)
    n = mat.shape[0]
    
    # Calculate eigenvalues and eigenvectors
    eigenvalues, eigenvectors = np.linalg.eig(mat)
    max_eigenvalue = np.max(np.real(eigenvalues))
    principal_eigenvector = np.real(eigenvectors[:, np.argmax(np.real(eigenvalues))])
    
    # Normalize weights
    weights = principal_eigenvector / np.sum(principal_eigenvector)
    
    # Calculate Consistency Ratio (CR)
    # Random Index values for n=1 to 10
    RI = [0, 0, 0.58, 0.9, 1.12, 1.24, 1.32, 1.41, 1.45, 1.49]
    if n <= 2:
        cr = 0.0
    else:
        ci = (max_eigenvalue - n) / (n - 1)
        cr = ci / RI[n-1]
        
    return weights, cr

def get_weights_from_config(config_module):
    """Pre-compute weights from config"""
    weights = {}
    cr_vals = {}
    
    for key, matrix in config_module.AHP_MATRICES.items():
        w, cr = compute_ahp_weights(matrix)
        weights[key] = w
        cr_vals[key] = cr
        
    return weights, cr_vals

