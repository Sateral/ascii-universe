from dataclasses import dataclass
from typing import Tuple, Optional
from enum import Enum
from abc import abstractmethod, ABC

from engine.camera import Camera

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
    pos: Tuple[float, float]
    velocity: Tuple[float, float]
    mass: float
    radius: float
    type: BodyType = BodyType.PLANET
    luminosity: Optional[float] = None
    temperature: Optional[float] = None
    albedo: Optional[float] = None
    composition: Optional[str] = None
    description: Optional[str] = None

    # @abstractmethod
    # def draw(self, canvas, system_x: int, system_y: int, terminal_width: int, terminal_height: int, camera: Camera) -> None:
    #     """
    #     Draw the body to the renderer.
        
    #     Args:
    #         canvas: The canvas to draw to.
    #         system_x: The x coordinate of the system.
    #         system_y: The y coordinate of the system.
    #         terminal_width: The width of the terminal.
    #         terminal_height: The height of the terminal.
    #         camera: The camera to use for rendering.
    #     """
    #     pass

    def move(self, dt: float) -> None:
        """Move the body by its velocity over the supplied time step."""
        x, y = self.pos
        vx, vy = self.velocity
        self.pos = (x + vx * dt, y + vy * dt)
    

    # @classmethod
    # def star(
    #     cls,
    #     name: str,
    #     pos: Tuple[float, float],
    #     mass: float,
    #     radius: float,
    #     *,
    #     velocity: Tuple[float, float] = (0.0, 0.0),
    #     luminosity: float = 1.0,
    #     temperature: float = 5778.0,
    #     composition: str = "Hydrogen/Helium",
    #     description: Optional[str] = None,
    # ) -> "CelestialBody":
    #     return cls(
    #         name=name,
    #         pos=pos,
    #         velocity=velocity,
    #         mass=mass,
    #         radius=radius,
    #         type=BodyType.STAR,
    #         luminosity=luminosity,
    #         temperature=temperature,
    #         composition=composition,
    #         description=description or "Main sequence star",
    #     )

    # @classmethod
    # def planet(
    #     cls,
    #     name: str,
    #     pos: Tuple[float, float],
    #     mass: float,
    #     radius: float,
    #     *,
    #     velocity: Tuple[float, float] = (0.0, 0.0),
    #     albedo: float = 0.3,
    #     composition: str = "Silicate",
    #     description: Optional[str] = None,
    # ) -> "CelestialBody":
    #     return cls(
    #         name=name,
    #         pos=pos,
    #         velocity=velocity,
    #         mass=mass,
    #         radius=radius,
    #         type=BodyType.PLANET,
    #         albedo=albedo,
    #         composition=composition,
    #         description=description or "Terrestrial planet",
    #     )

    # @classmethod
    # def asteroid(
    #     cls,
    #     name: str,
    #     pos: Tuple[float, float],
    #     mass: float,
    #     radius: float,
    #     *,
    #     velocity: Tuple[float, float] = (0.0, 0.0),
    #     composition: str = "Carbonaceous",
    #     description: Optional[str] = None,
    # ) -> "CelestialBody":
    #     return cls(
    #         name=name,
    #         pos=pos,
    #         velocity=velocity,
    #         mass=mass,
    #         radius=radius,
    #         type=BodyType.ASTEROID,
    #         composition=composition,
    #         description=description or "Irregular asteroid",
    #     )

    # @classmethod
    # def black_hole(
    #     cls,
    #     name: str,
    #     pos: Tuple[float, float],
    #     mass: float,
    #     radius: float,
    #     *,
    #     velocity: Tuple[float, float] = (0.0, 0.0),
    #     description: Optional[str] = None,
    # ) -> "CelestialBody":
    #     return cls(
    #         name=name,
    #         pos=pos,
    #         velocity=velocity,
    #         mass=mass,
    #         radius=radius,
    #         type=BodyType.BLACK_HOLE,
    #         description=description or "Supermassive black hole",
    #     )   