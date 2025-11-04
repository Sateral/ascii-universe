import os
import shutil

from engine.universe import Universe


class Renderer:
    """Renders the universe to the terminal in ASCII"""

    def __init__(self, width: int | None = None, height: int | None = None):
        terminal_size = shutil.get_terminal_size((80, 40))
        self.width = width or terminal_size.columns
        self.height = height or terminal_size.lines - 2

    def clear(self) -> None:
        os.system("cls" if os.name == "nt" else "clear")

    def render(self, universe: Universe) -> None:
        """Draw all galaxies and systems as ASCII points"""

        # Create empty canvas
        canvas = [[" " for _ in range(self.width)] for _ in range(self.height)]
        cx, cy = self.width // 2, self.height // 2

        # Draw galaxies
        for galaxy in universe.galaxies:
            # Center of galaxy
            gx, gy = int(cx + galaxy.pos[0]), int(cy + galaxy.pos[1])

            # If galaxy is in view
            if 0 <= gx < self.width and 0 <= gy < self.height:
                canvas[gy][gx] = "x"

            # Draw systems
            for system in galaxy.systems:
                # Center of system  
                sx, sy = int(gx + system.center.pos[0]), int(gy + system.center.pos[1])

                # If system is in view
                if 0 <= sx < self.width and 0 <= sy < self.height:
                    canvas[sy][sx] = system.center.symbol
                
                # Draw bodies
                for body in system.bodies:
                    offset_x = body.pos[0] - system.center.pos[0]
                    offset_y = body.pos[1] - system.center.pos[1]
                    bx, by = int(sx + offset_x), int(sy + offset_y)

                    # If body is in view
                    if 0 <= bx < self.width and 0 <= by < self.height:
                        canvas[by][bx] = body.symbol
        
        # Render to screen
        self.clear()
        for row in canvas:
            print("".join(row))