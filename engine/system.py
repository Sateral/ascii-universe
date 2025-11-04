from dataclasses import dataclass, field
from typing import List

from .body import Body
from utils.math_utils import rotate_around

@dataclass
class SolarSystem:
    """Represents a star system with orbiting bodies."""

    name: str
    center: Body
    bodies: List[Body] = field(default_factory=list)

    def update(self, dt: float) -> None:
        """Rotate all orbiting bodies around the center."""
        for body in self.bodies:
            body.pos = rotate_around(body.pos, self.center.pos, dt * 0.2)