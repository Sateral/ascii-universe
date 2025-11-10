from dataclasses import dataclass
from math import sqrt

from engine.body.base import CelestialBody
from engine.body.base import BodyType
from engine.camera import Camera

@dataclass
class Star(CelestialBody):
    type: BodyType = BodyType.STAR

    # def draw(self, canvas, system_x: int, system_y: int, terminal_width: int, terminal_height: int, camera: Camera) -> None:
    #     radius_world = max(self.radius, 0.5) # World space radius, avoids 0-size stars
    #     radius_px = max(1, int(round(radius_world * camera.zoom))) # Converted into pixels and adjusted by camera's zoom level, ensures at least 1 pixel wide
    #     lum = self.luminosity or 1.0 # Luminosity of star, used for brightness
    #     gradient = [" ", "·", ":", "*", "o", "O", "@"]
    #     levels = len(gradient) - 1

    #     for dy in range(-radius_px, radius_px + 1):
    #         star_pixel_y = system_y + dy
    #         if not (0 <= star_pixel_y < terminal_height):
    #             continue
    #         for dx in range(-radius_px, radius_px + 1):
    #             star_pixel_x = system_x + dx
    #             if not (0 <= star_pixel_x < terminal_width):
    #                 continue

    #             # Euclidean distance from center of star
    #             dist = sqrt(dx * dx + dy * dy)

    #             # If pixel is outside of star's radius
    #             if dist > radius_px:
    #                 continue

    #             # Normalize distance to [0 (center), 1 (edge)]
    #             normalized = dist / max(radius_px, 1)
    #             strength = (1 - normalized) * lum
    #             idx = int(min(levels, max(0, strength * levels)))
    #             if idx > 0:
    #                 canvas[star_pixel_y][star_pixel_x] = gradient[idx]