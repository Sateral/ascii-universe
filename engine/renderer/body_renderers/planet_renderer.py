from dataclasses import dataclass
from enum import Enum
import math
import random
from typing import List

from engine.body.base import BodyType, CelestialBody
from engine.body.planet import Planet
from engine.camera import Camera
from engine.renderer.base_renderer import BodyRenderer, register_renderer


class PlanetType(Enum):
    GAS_GIANT = "Gas Giant"
    ICE_GIANT = "Ice Giant"
    TERRESTRIAL = "Terrestrial"
    LAVA_GIANT = "Lava Giant"

@register_renderer(BodyType.PLANET)
class PlanetRenderer(BodyRenderer[Planet]):
    GRADIENT = [" ", "·", ":", "*", "o", "O", "@"]

    def draw(self, body, canvas, sx, sy, width, height, camera: Camera) -> None:
        drawer = getattr(self, f"_draw_{body.planet_type.name.lower()}", None)
        if drawer is None:
            raise ValueError(f"No drawer for planet type {body.planet_type}")
        drawer(body, canvas, sx, sy, width, height, camera)

    # --- Drawers ---

    def _draw_gas_giant(self, body: Planet, canvas: List[List[str]], sx: int, sy: int, width: int, height: int, camera: Camera) -> None:
        radius = max(body.radius, 0.5)
        radius_px = max(1, int(round(radius * camera.zoom)))
        lum = body.luminosity or 1.0
        levels = len(self.GRADIENT) - 1

        # Stable randomization
        random.seed(hash(body.name))
        band_count = random.randint(6, 10)       # how many bands across the planet
        wave_amp = random.uniform(0.1, 0.25)     # horizontal wave distortion
        band_mix = random.uniform(0.2, 0.4)      # mixing strength for distortion

        for dy in range(-radius_px, radius_px + 1):
            y = sy + dy
            if not (0 <= y < height):
                continue
            for dx in range(-radius_px, radius_px + 1):
                x = sx + dx
                if not (0 <= x < width):
                    continue

                # Distance check
                dist = math.sqrt(dx * dx + dy * dy)
                if dist > radius_px:
                    continue

                # Normalize coords
                nx = dx / radius_px
                ny = dy / radius_px
                r = math.sqrt(nx * nx + ny * ny)
                if r > 1:
                    continue

                # Latitude-based wave (bands)
                latitude = ny * math.pi / 2
                band = math.sin(latitude * band_count)

                # Small horizontal distortion (simulate wind/turbulence)
                distortion = math.sin(nx * 8 + band_mix * ny * 6)
                band = (band + wave_amp * distortion) * 0.5 + 0.5  # normalize 0–1

                # Darken edges to look spherical
                brightness = band * lum * (1 - r * 0.7)
                idx = int(min(levels, max(0, brightness * levels)))
                canvas[y][x] = self.GRADIENT[idx]

    def _draw_ice_giant(self, body: Planet, canvas: List[List[str]], sx: int, sy: int, width: int, height: int, camera: Camera) -> None:
        return

    def _draw_terrestrial(self, body: Planet, canvas: List[List[str]], sx: int, sy: int, width: int, height: int, camera: Camera) -> None:
        return

    def _draw_lava_giant(self, body: Planet, canvas: List[List[str]], sx: int, sy: int, width: int, height: int, camera: Camera) -> None:
        return
