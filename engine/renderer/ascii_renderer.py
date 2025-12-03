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
        # Create canvas (list of lists of single characters)
        canvas = [[" " for _ in range(self.width)] for _ in range(self.height)]

        # Draw galaxies
        for galaxy in universe.galaxies:
            # Check if galaxy is roughly in view (simple culling)
            gx, gy = self.to_screen(*galaxy.pos)
            if 0 <= gx < self.width and 0 <= gy < self.height:
                canvas[gy][gx] = "x"

            # Draw systems
            for system in galaxy.systems:
                # Recursively draw the system hierarchy starting from the center star
                self._draw_hierarchy(system.center, canvas)
        
        # Render status on the last line if provided
        if status is not None:
            s = status[:self.width]
            last_row = canvas[-1]
            for i, ch in enumerate(s):
                last_row[i] = ch

        # Render to screen
        self._print(canvas)

    def _draw_hierarchy(self, body: CelestialBody, canvas):
        """Recursively draw a body and its children."""
        bx, by = self.to_screen(*body.pos)
        
        # Culling: Only draw if within bounds
        if 0 <= bx < self.width and 0 <= by < self.height:
            self._draw_body(body, canvas, bx, by)
            
        # Draw children
        for child in body.children:
            self._draw_hierarchy(child, canvas)
        

        

    def _draw_body(self, body: CelestialBody, canvas, sx, sy):
        renderer_cls = get_renderer(body.type)
        if renderer_cls:
            renderer_cls().draw(body, canvas, sx, sy, self.width, self.height, self.camera)

    def hide_cursor(self):
        sys.stdout.write("\033[?25l")
        sys.stdout.flush()

    def show_cursor(self):
        sys.stdout.write("\033[?25h")
        sys.stdout.flush()

    def _print(self, canvas):
        # Build the entire frame as a single string
        lines = ["".join(row) for row in canvas]
        # Move to home, print all lines joined by newline
        # Note: We avoid printing a newline at the very end to prevent scrolling
        frame = "\033[H" + "\n".join(lines)
        sys.stdout.write(frame)
        sys.stdout.flush()
