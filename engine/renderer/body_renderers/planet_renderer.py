from dataclasses import dataclass
from enum import Enum
import math
import random
from typing import List

from engine.body.base import BodyType, CelestialBody
from engine.body.planet import Planet
from engine.camera import Camera
from engine.renderer.base_renderer import BodyRenderer, register_renderer


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
        radius = max(body.radius, 0.5)
        radius_px = max(1, int(round(radius * camera.zoom)))
        lum = body.luminosity or 1.0
        levels = len(self.GRADIENT) - 1

        random.seed(hash(body.name) ^ 0x1CE)
        band_count = random.randint(2, 5)
        band_phase = random.uniform(0.0, 2 * math.pi)
        band_amp = random.uniform(0.15, 0.3)
        turb_amp = random.uniform(0.05, 0.12)
        spot_x = random.uniform(-0.3, 0.3)
        spot_y = random.uniform(-0.3, 0.3)
        spot_sigma = random.uniform(0.10, 0.18)

        for dy in range(-radius_px, radius_px + 1):
            y = sy + dy
            if not (0 <= y < height):
                continue
            for dx in range(-radius_px, radius_px + 1):
                x = sx + dx
                if not (0 <= x < width):
                    continue

                dist = math.sqrt(dx * dx + dy * dy)
                if dist > radius_px:
                    continue

                nx = dx / radius_px
                ny = dy / radius_px
                r = math.sqrt(nx * nx + ny * ny)
                if r > 1:
                    continue

                latitude = ny * math.pi / 2.0
                band = math.cos(latitude * band_count + band_phase) * 0.5 + 0.5
                band_mix = (1.0 - band_amp) * 0.5 + band_amp * band
                turb = math.sin(nx * 6.0 + ny * 2.0 + band_phase * 0.7) * 0.5 + 0.5
                val = band_mix * (1.0 - turb_amp) + turb * turb_amp

                dxs = nx - spot_x
                dys = ny - spot_y
                dsq = dxs * dxs + dys * dys
                spot = math.exp(-dsq / (2.0 * spot_sigma * spot_sigma))

                base = 0.35 + 0.55 * val
                brightness = base * (1.0 - r * 0.5) + 0.35 * spot
                brightness *= lum
                brightness = max(0.0, min(1.0, brightness))
                idx = int(min(levels, max(0, brightness * levels)))
                canvas[y][x] = self.GRADIENT[idx]

    def _draw_terrestrial(self, body: Planet, canvas: List[List[str]], sx: int, sy: int, width: int, height: int, camera: Camera) -> None:
        radius = max(body.radius, 0.5)
        radius_px = max(1, int(round(radius * camera.zoom)))
        levels = len(self.GRADIENT) - 1

        random.seed(hash(body.name) ^ 0x7ED)
        freq1 = random.uniform(3.0, 6.0)
        freq2 = random.uniform(3.0, 6.0)
        freq3 = random.uniform(2.0, 4.0)
        ph1 = random.uniform(0.0, 2 * math.pi)
        ph2 = random.uniform(0.0, 2 * math.pi)
        ph3 = random.uniform(0.0, 2 * math.pi)
        sea_level = random.uniform(-0.15, 0.15)
        mount_gain = random.uniform(0.3, 0.6)
        ocean_dark = random.uniform(0.15, 0.25)
        land_base = random.uniform(0.45, 0.6)
        albedo = body.albedo if body.albedo is not None else 0.3

        for dy in range(-radius_px, radius_px + 1):
            y = sy + dy
            if not (0 <= y < height):
                continue
            for dx in range(-radius_px, radius_px + 1):
                x = sx + dx
                if not (0 <= x < width):
                    continue

                dist = math.sqrt(dx * dx + dy * dy)
                if dist > radius_px:
                    continue

                nx = dx / radius_px
                ny = dy / radius_px
                r = math.sqrt(nx * nx + ny * ny)
                if r > 1:
                    continue

                elev = (
                    math.sin(nx * freq1 + ph1) +
                    math.cos(ny * freq2 + ph2) +
                    math.sin((nx + ny) * freq3 + ph3)
                ) / 3.0

                landness = elev - sea_level
                if landness > 0.0:
                    rough = abs(math.sin(nx * freq1 * 2.0 + ph1 * 1.7) * math.cos(ny * freq2 * 2.0 + ph2 * 1.3))
                    brightness = land_base + mount_gain * landness * (0.5 + 0.5 * rough)
                else:
                    wave = math.sin(nx * 10.0 + ph3) * math.sin(ny * 8.0 + ph2)
                    brightness = ocean_dark + 0.06 * (wave * 0.5 + 0.5)

                polar = max(0.0, abs(ny) - 0.6) / 0.4
                brightness = brightness * (1.0 - 0.6 * polar) + 0.85 * polar
                brightness *= (1.0 - r * 0.7)
                brightness *= (0.7 + 0.6 * albedo)
                brightness = max(0.0, min(1.0, brightness))

                idx = int(min(levels, max(0, brightness * levels)))
                canvas[y][x] = self.GRADIENT[idx]

    def _draw_lava_giant(self, body: Planet, canvas: List[List[str]], sx: int, sy: int, width: int, height: int, camera: Camera) -> None:
        radius = max(body.radius, 0.5)
        radius_px = max(1, int(round(radius * camera.zoom)))
        levels = len(self.GRADIENT) - 1

        random.seed(hash(body.name) ^ 0x1A4A)
        freq1 = random.uniform(8.0, 12.0)
        freq2 = random.uniform(8.0, 12.0)
        freq3 = random.uniform(4.0, 8.0)
        ph1 = random.uniform(0.0, 2 * math.pi)
        ph2 = random.uniform(0.0, 2 * math.pi)
        ph3 = random.uniform(0.0, 2 * math.pi)
        thickness = random.uniform(0.10, 0.18)
        glow = random.uniform(0.6, 0.9)
        base_dark = random.uniform(0.15, 0.25)

        for dy in range(-radius_px, radius_px + 1):
            y = sy + dy
            if not (0 <= y < height):
                continue
            for dx in range(-radius_px, radius_px + 1):
                x = sx + dx
                if not (0 <= x < width):
                    continue

                dist = math.sqrt(dx * dx + dy * dy)
                if dist > radius_px:
                    continue

                nx = dx / radius_px
                ny = dy / radius_px
                r = math.sqrt(nx * nx + ny * ny)
                if r > 1:
                    continue

                u = abs(math.sin(nx * freq1 + ph1))
                v = abs(math.sin(ny * freq2 + ph2))
                w = abs(math.sin((nx - ny) * freq3 + ph3))
                m = min(u, v, w)
                crack = math.exp(- (m / thickness) ** 2)
                pool = max(0.0, math.sin(nx * 3.0 + ny * 2.0 + ph3)) * 0.15

                edge_cool = (1.0 - r * 0.5)
                brightness = base_dark * edge_cool + glow * crack + pool
                brightness = max(0.0, min(1.0, brightness))

                idx = int(min(levels, max(0, brightness * levels)))
                canvas[y][x] = self.GRADIENT[idx]
