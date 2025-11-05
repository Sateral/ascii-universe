from dataclasses import dataclass, field
from typing import List

from .body.celestial_body import CelestialBody
from utils.math_utils import rotate_around

@dataclass
class SolarSystem:
    """Represents a star system with orbiting bodies."""

    name: str
    center: CelestialBody
    bodies: List[CelestialBody] = field(default_factory=list)

    def update(self, dt: float) -> None:
        """Rotate all orbiting bodies around the center."""
        for body in self.bodies:
            body.pos = rotate_around(body.pos, self.center.pos, dt * 0.2)