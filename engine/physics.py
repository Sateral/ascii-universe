import math
from dataclasses import dataclass
from typing import Tuple

@dataclass
class Orbit:
    """
    Represents a Keplerian orbit.
    """
    semi_major_axis: float  # The long radius of the ellipse (a)
    eccentricity: float     # How stretched the ellipse is (e)
    inclination: float      # Tilt of the orbit (i) - simplified for 2D as just visual or ignored
    argument_of_periapsis: float # Orientation of the ellipse (omega)
    mean_anomaly_at_epoch: float # Starting position (M0)
    period: float           # Time to complete one orbit

    def get_position(self, t: float) -> Tuple[float, float]:
        """
        Calculate position (x, y) relative to the parent at time t.
        """
        # Mean Anomaly (M)
        M = self.mean_anomaly_at_epoch + (2 * math.pi * t / self.period)
        
        # Solve Kepler's Equation for Eccentric Anomaly (E)
        # M = E - e * sin(E)
        # Iterative approximation (Newton-Raphson)
        E = M
        for _ in range(5):
            E = M + self.eccentricity * math.sin(E)
        
        # True Anomaly (nu)
        # cos(nu) = (cos(E) - e) / (1 - e * cos(E))
        # This is a bit complex, let's use the coordinate form directly from E
        
        # Coordinates in the orbital plane (P, Q)
        # x = a * (cos(E) - e)
        # y = a * sqrt(1 - e^2) * sin(E)
        
        P = self.semi_major_axis * (math.cos(E) - self.eccentricity)
        Q = self.semi_major_axis * math.sqrt(1 - self.eccentricity**2) * math.sin(E)
        
        # Rotate by argument of periapsis (omega)
        # x' = x * cos(w) - y * sin(w)
        # y' = x * sin(w) + y * cos(w)
        
        cos_w = math.cos(self.argument_of_periapsis)
        sin_w = math.sin(self.argument_of_periapsis)
        
        x = P * cos_w - Q * sin_w
        y = P * sin_w + Q * cos_w
        
        return x, y
