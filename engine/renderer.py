import os
import sys
import shutil
from math import sqrt

from engine.camera import Camera
from engine.universe import Universe
from engine.body.celestial_body import BodyType


class Renderer:
    """Renders the universe to the terminal in ASCII"""

    def __init__(
        self,
        width: int | None = None,
        height: int | None = None,
        *,
        camera: Camera | None = None,
    ) -> None:
        terminal_size = shutil.get_terminal_size((80, 40))
        self.width = width or terminal_size.columns
        self.height = height or terminal_size.lines - 2
        self.camera = camera or Camera()

    def clear(self) -> None:
        os.system("cls" if os.name == "nt" else "clear")

    def render(self, universe: Universe) -> None:
        """Draw all galaxies and systems as ASCII points"""

        # Create empty canvas
        canvas = [[" " for _ in range(self.width)] for _ in range(self.height)]
        half_w = self.width / 2
        half_h = self.height / 2

        def to_screen(wx, wy):
            cam_x, cam_y = self.camera.center
            zoom = self.camera.zoom
            sx = int((wx - cam_x) * zoom + half_w)
            sy = int((wy - cam_y) * zoom + half_h)
            return sx, sy

        # Draw galaxies
        for galaxy in universe.galaxies:
            # Center of galaxy
            gx, gy = to_screen(galaxy.pos[0], galaxy.pos[1])

            # If galaxy is in view
            if 0 <= gx < self.width and 0 <= gy < self.height:
                canvas[gy][gx] = "x"

            # Draw systems
            for system in galaxy.systems:
                # Center of system
                sx, sy = to_screen(system.center.pos[0], system.center.pos[1])

                if system.center.type == BodyType.STAR:
                    self._draw_star(canvas, system.center, sx, sy)
                elif 0 <= sx < self.width and 0 <= sy < self.height:
                    canvas[sy][sx] = system.center.symbol
                
                # Draw bodies
                for body in system.bodies:
                    bx, by = to_screen(body.pos[0], body.pos[1])

                    # If body is in view
                    if 0 <= bx < self.width and 0 <= by < self.height:
                        canvas[by][bx] = body.symbol
        
        # Render to screen
        sys.stdout.write("\033[H")       # move cursor home without clearing
        for row in canvas:
            sys.stdout.write("".join(row) + "\n")
        sys.stdout.flush()

    def _draw_star(self, canvas, star, screen_x: int, screen_y: int) -> None:
        radius_world = max(star.radius, 0.5) # World space radius, avoids 0-size stars
        radius_px = max(1, int(round(radius_world * self.camera.zoom))) # Converted into pixels and adjusted by camera's zoom level, ensures at least 1 pixel wide
        lum = star.luminosity or 1.0 # Luminosity of star, used for brightness
        gradient = [" ", "·", ":", "*", "o", "O", "@"]
        levels = len(gradient) - 1

        for dy in range(-radius_px, radius_px + 1):
            star_pixel_y = screen_y + dy
            if not (0 <= star_pixel_y < self.height):
                continue
            for dx in range(-radius_px, radius_px + 1):
                star_pixel_x = screen_x + dx
                if not (0 <= star_pixel_x < self.width):
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
                    canvas[star_pixel_y][star_pixel_x] = gradient[idx]