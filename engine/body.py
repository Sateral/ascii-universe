from dataclasses import dataclass
from typing import Tuple

@dataclass
class Body:
    """A single celestial body (planet, star, asteroid, etc)."""

    name: str
    pos: Tuple[float, float]
    velocity: Tuple[float, float]
    mass: float
    symbol: str = "*"

    def move(self, dt: float) -> None:
        """
        Move the body by its velocity.
        
        Args:
            dt (float): Time step.
        """
        x, y = self.pos
        vx, vy = self.velocity
        self.pos = (x + vx * dt, y + vy * dt)