import os
import shutil
import sys
from typing import Optional
from engine.body.base import CelestialBody
from engine.camera import Camera
from engine.renderer.base_renderer import get_renderer
from engine.universe import Universe

class AsciiRenderer:
    """Responsible for traversing the universe and delegating drawing."""

    def __init__(self, width=None, height=None, *, camera: Optional[Camera]=None):
        terminal_size = shutil.get_terminal_size((80, 40))
        self.width = width or terminal_size.columns
        self.height = height or terminal_size.lines - 2
        self.half_width = self.width / 2
        self.half_height = self.height / 2
        self.camera = camera or Camera()

    def clear(self) -> None:
        os.system("cls" if os.name == "nt" else "clear")

    def to_screen(self, wx, wy):
        """
        Returns the objects screen position relative to the camera
        """
        cam_x, cam_y = self.camera.center
        zoom = self.camera.zoom
        
        sx = int((wx - cam_x) * zoom + self.half_width)
        sy = int((wy - cam_y) * zoom + self.half_height)
        
        return sx, sy

    def render(self, universe: Universe, status: Optional[str] = None) -> None:
        """
        Renders the universe to the terminal
        """
        canvas = [[" " for _ in range(self.width)] for _ in range(self.height)]

        # Draw galaxies
        for galaxy in universe.galaxies:
            # Center of galaxy
            gx, gy = self.to_screen(*galaxy.pos)

            # If galaxy is in view
            if 0 <= gx < self.width and 0 <= gy < self.height:
                canvas[gy][gx] = "x"

            # Draw systems
            for system in galaxy.systems:
                # Center of system
                sx, sy = self.to_screen(*system.center.pos)

                if 0 <= sx < self.width and 0 <= sy < self.height:
                    self._draw_body(system.center, canvas, sx, sy)

                # Draw bodies
                for body in system.bodies:
                    bx, by = self.to_screen(*body.pos)

                    # If body is in view
                    if 0 <= bx < self.width and 0 <= by < self.height:
                        self._draw_body(body, canvas, bx, by)
        
        # Render status on the last line if provided
        if status is not None:
            s = status[:self.width]
            last_row = canvas[-1]
            for i, ch in enumerate(s):
                last_row[i] = ch

        # Render to screen
        self._print(canvas)
        

    def _draw_body(self, body: CelestialBody, canvas, sx, sy):
        renderer_cls = get_renderer(body.type)
        if renderer_cls:
            renderer_cls().draw(body, canvas, sx, sy, self.width, self.height, self.camera)

    def _print(self, canvas):
        sys.stdout.write("\033[H")       # move cursor home without clearing
        for y, row in enumerate(canvas):
            line = "".join(row)
            if y < self.height - 1:
                sys.stdout.write(line + "\n")
            else:
                sys.stdout.write(line)
        sys.stdout.flush()
