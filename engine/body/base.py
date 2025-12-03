from dataclasses import dataclass, field
from typing import Tuple, Optional, List
from enum import Enum
from abc import abstractmethod, ABC

from engine.camera import Camera
from engine.physics import Orbit

class BodyType(Enum):
    STAR = "Star"
    PLANET = "Planet"
    ASTEROID = "Asteroid"
    DEBRIS = "Debris"
    BLACK_HOLE = "Black Hole"


@dataclass
class CelestialBody(ABC):
    """A celestial body with optional physical metadata."""

    name: str
    mass: float
    radius: float
    type: BodyType = BodyType.PLANET
    
    # Hierarchy
    parent: Optional["CelestialBody"] = None
    children: list["CelestialBody"] = field(default_factory=list)
    orbit: Optional["Orbit"] = None
    
    # State
    pos: Tuple[float, float] = (0.0, 0.0)
    velocity: Tuple[float, float] = (0.0, 0.0) # Kept for compatibility/hybrid mode
    
    # Metadata
    luminosity: Optional[float] = None
    temperature: Optional[float] = None
    albedo: Optional[float] = None
    composition: Optional[str] = None
    description: Optional[str] = None

    def add_child(self, child: "CelestialBody", orbit: Optional["Orbit"] = None) -> None:
        """Add a child body orbiting this body."""
        child.parent = self
        if orbit:
            child.orbit = orbit
        self.children.append(child)

    def update(self, t: float) -> None:
        """Update position based on orbit and time t."""
        if self.parent and self.orbit:
            # Calculate local position from orbit
            lx, ly = self.orbit.get_position(t)
            # Add parent's position
            px, py = self.parent.pos
            self.pos = (px + lx, py + ly)
        
        # Recursively update children
        for child in self.children:
            child.update(t)