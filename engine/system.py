from dataclasses import dataclass, field
from typing import List

from .body.base import CelestialBody

@dataclass
class SolarSystem:
    """Represents a star system with orbiting bodies."""

    name: str
    center: CelestialBody
    bodies: List[CelestialBody] = field(default_factory=list)

    def update(self, t: float) -> None:
        """Update the system state at time t."""
        # Update the center body (which recursively updates children)
        self.center.update(t)