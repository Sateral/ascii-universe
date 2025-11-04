from dataclasses import dataclass
from typing import Tuple, Optional
from enum import Enum


class BodyType(Enum):
    STAR = "Star"
    PLANET = "Planet"
    ASTEROID = "Asteroid"
    DEBRIS = "Debris"
    BLACK_HOLE = "Black Hole"


@dataclass
class Body:
    """A celestial body with optional physical metadata."""

    name: str
    pos: Tuple[float, float]
    velocity: Tuple[float, float]
    mass: float
    radius: float
    symbol: str = "*"
    type: BodyType = BodyType.PLANET
    luminosity: Optional[float] = None
    temperature: Optional[float] = None
    albedo: Optional[float] = None
    composition: Optional[str] = None
    description: Optional[str] = None

    def move(self, dt: float) -> None:
        """Move the body by its velocity over the supplied time step."""
        x, y = self.pos
        vx, vy = self.velocity
        self.pos = (x + vx * dt, y + vy * dt)

    @classmethod
    def star(
        cls,
        name: str,
        pos: Tuple[float, float],
        mass: float,
        radius: float,
        *,
        velocity: Tuple[float, float] = (0.0, 0.0),
        symbol: str = "☉",
        luminosity: float = 1.0,
        temperature: float = 5778.0,
        composition: str = "Hydrogen/Helium",
        description: Optional[str] = None,
    ) -> "Body":
        return cls(
            name=name,
            pos=pos,
            velocity=velocity,
            mass=mass,
            radius=radius,
            symbol=symbol,
            type=BodyType.STAR,
            luminosity=luminosity,
            temperature=temperature,
            composition=composition,
            description=description or "Main sequence star",
        )

    @classmethod
    def planet(
        cls,
        name: str,
        pos: Tuple[float, float],
        mass: float,
        radius: float,
        *,
        velocity: Tuple[float, float] = (0.0, 0.0),
        symbol: str = "●",
        albedo: float = 0.3,
        composition: str = "Silicate",
        description: Optional[str] = None,
    ) -> "Body":
        return cls(
            name=name,
            pos=pos,
            velocity=velocity,
            mass=mass,
            radius=radius,
            symbol=symbol,
            type=BodyType.PLANET,
            albedo=albedo,
            composition=composition,
            description=description or "Terrestrial planet",
        )

    @classmethod
    def asteroid(
        cls,
        name: str,
        pos: Tuple[float, float],
        mass: float,
        radius: float,
        *,
        velocity: Tuple[float, float] = (0.0, 0.0),
        symbol: str = "·",
        composition: str = "Carbonaceous",
        description: Optional[str] = None,
    ) -> "Body":
        return cls(
            name=name,
            pos=pos,
            velocity=velocity,
            mass=mass,
            radius=radius,
            symbol=symbol,
            type=BodyType.ASTEROID,
            composition=composition,
            description=description or "Irregular asteroid",
        )

    @classmethod
    def black_hole(
        cls,
        name: str,
        pos: Tuple[float, float],
        mass: float,
        radius: float,
        *,
        velocity: Tuple[float, float] = (0.0, 0.0),
        symbol: str = "●",
        description: Optional[str] = None,
    ) -> "Body":
        return cls(
            name=name,
            pos=pos,
            velocity=velocity,
            mass=mass,
            radius=radius,
            symbol=symbol,
            type=BodyType.BLACK_HOLE,
            description=description or "Supermassive black hole",
        )