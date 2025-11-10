from math import sqrt

from engine.body.base import BodyType
from engine.camera import Camera

from ..base_renderer import BodyRenderer, register_renderer

@register_renderer(BodyType.STAR)
class StarRenderer(BodyRenderer):
    GRADIENT = [" ", "·", ":", "*", "o", "O", "@"]

    def draw(self, body, canvas, sx, sy, width, height, camera: Camera) -> None:
        radius_world = max(body.radius, 0.5) # World space radius, avoids 0-size stars
        radius_px = max(1, int(round(radius_world * camera.zoom))) # Converted into pixels and adjusted by camera's zoom level, ensures at least 1 pixel wide
        lum = body.luminosity or 1.0 # Luminosity of star, used for brightness
        levels = len(self.GRADIENT) - 1

        for dy in range(-radius_px, radius_px + 1):
            star_pixel_y = sy + dy
            if not (0 <= star_pixel_y < height):
                continue
            for dx in range(-radius_px, radius_px + 1):
                star_pixel_x = sx + dx
                if not (0 <= star_pixel_x < width):
                    continue

                # Euclidean distance from center of star
                dist = sqrt(dx * dx + dy * dy)

                # If pixel is outside of star's radius
                if dist > radius_px:
                    continue

                # Normalize distance to [0 (center), 1 (edge)]
                normalized = dist / max(radius_px, 1)
                strength = (1 - normalized) * lum
                idx = int(min(levels, max(0, strength * levels)))
                if idx > 0:
                    canvas[star_pixel_y][star_pixel_x] = self.GRADIENT[idx]