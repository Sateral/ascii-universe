from dataclasses import dataclass
from enum import Enum
import math

from engine.body.base import BodyType, CelestialBody
from engine.camera import Camera


class PlanetType(Enum):
    GAS_GIANT = "Gas Giant"
    ICE_GIANT = "Ice Giant"
    TERRESTRIAL = "Terrestrial"
    LAVA_GIANT = "Lava Giant"

@dataclass
class Planet(CelestialBody):
    type: BodyType = BodyType.PLANET
    planet_type: PlanetType = PlanetType.TERRESTRIAL

#     GRADIENT = [" ", "·", ":", "*", "o", "O", "@"]

#     def draw(self, canvas, system_x: int, system_y: int, terminal_width: int, terminal_height: int, camera: Camera) -> None:
#         drawer = PLANET_DRAWERS[self.planet_type]
#         drawer(self, canvas, system_x, system_y, terminal_width, terminal_height, camera, self.radius, self.luminosity)

# def _draw_gas_giant(planet, canvas, system_x: int, system_y: int, terminal_width: int, terminal_height: int, camera: Camera, radius: float, luminosity: float) -> None:
#     radius = max(radius, 0.5)
#     radius_px = max(1, int(round(radius * camera.zoom)))
#     lum = luminosity or 1.0
#     levels = len(planet.GRADIENT) - 1

#     for dy in range(-radius_px, radius_px + 1):
#         planet_pixel_y = system_y + dy
#         if not (0 <= planet_pixel_y < terminal_height):
#             continue
#         for dx in range(-radius_px, radius_px + 1):
#             planet_pixel_x = system_x + dx
#             if not (0 <= planet_pixel_x < terminal_width):
#                 continue
            
#             dist = math.sqrt(dx * dx + dy * dy)
#             if dist > radius_px:
#                 continue
            
#             normalized = dist / max(radius_px, 1)
#             strength = (1 - normalized) * lum
#             idx = int(min(levels, max(0, strength * levels)))
#             if idx > 0:
#                 canvas[planet_pixel_y][planet_pixel_x] = planet.GRADIENT[idx]

# def _draw_ice_giant(planet, canvas, system_x: int, system_y: int, terminal_width: int, terminal_height: int, camera: Camera) -> None:
#     return

# def _draw_terrestrial(planet, canvas, system_x: int, system_y: int, terminal_width: int, terminal_height: int, camera: Camera) -> None:
#     return

# def _draw_lava_giant(planet, canvas, system_x: int, system_y: int, terminal_width: int, terminal_height: int, camera: Camera) -> None:
#     return
    

# PLANET_DRAWERS = {
#     PlanetType.GAS_GIANT: _draw_gas_giant,
#     PlanetType.ICE_GIANT: _draw_ice_giant,
#     PlanetType.TERRESTRIAL: _draw_terrestrial,
#     PlanetType.LAVA_GIANT: _draw_lava_giant,
# }