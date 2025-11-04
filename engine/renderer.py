import os
import sys
import shutil

from engine.camera import Camera
from engine.universe import Universe


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

                # If system is in view
                if 0 <= sx < self.width and 0 <= sy < self.height:
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