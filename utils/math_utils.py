from typing import Tuple
from math import sin, cos

def rotate_around(
    point: Tuple[float, float], center: Tuple[float, float], angle: float
) -> Tuple[float, float]:
    """Rotate a point around a center point by a given angle"""
    px, py = point
    cx, cy = center

    # Theta in radians
    cos_t = cos(angle)
    sin_t = sin(angle)

    x_shifted = px - cx
    y_shifted = py - cy

    x_rotated = x_shifted * cos_t - y_shifted * sin_t + cx
    y_rotated = x_shifted * sin_t + y_shifted * cos_t + cy
    
    return x_rotated, y_rotated
    
    