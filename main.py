import time
import msvcrt

from engine.generator import UniverseGenerator
from engine.renderer.ascii_renderer import AsciiRenderer
from engine.camera import Camera

DELTA_TIME = 0.1 # Simulation delta (how far things move each frame)
SLEEP = 0.05  # FPS Control (how often screen updates)
PAN_STEP = 2.0
ZOOM_IN_FACTOR = 1.1
ZOOM_OUT_FACTOR = 0.9
MAX_ZOOM = 100.0 # Increased max zoom
MIN_ZOOM = 0.01  # Decreased min zoom

def main():
    # Generate universe
    generator = UniverseGenerator(seed=1)
    universe = generator.generate_universe(num_galaxies=2)
    
    # Focus on the first system of the first galaxy
    start_system = universe.galaxies[0].systems[0]
    start_pos = start_system.center.pos

    camera = Camera(center=start_pos, zoom=0.5, max_zoom=MAX_ZOOM, min_zoom=MIN_ZOOM)
    renderer = AsciiRenderer(width=100, height=40, camera=camera)

    t = 0.0
    time_scale = 1.0
    paused = False

    renderer.hide_cursor()
    try:
        while True:
            while msvcrt.kbhit():
                key = msvcrt.getch()
                if key == b"\xe0":
                    key = msvcrt.getch()
                    if key == b"H":  # Arrow up
                        camera.pan(0, -PAN_STEP / camera.zoom)
                    elif key == b"P":  # Arrow down
                        camera.pan(0, PAN_STEP / camera.zoom)
                    elif key == b"K":  # Arrow left
                        camera.pan(-PAN_STEP / camera.zoom, 0)
                    elif key == b"M":  # Arrow right
                        camera.pan(PAN_STEP / camera.zoom, 0)
                elif key in (b"+", b"="):
                    camera.zoom_by(ZOOM_IN_FACTOR)
                elif key == b"-":
                    camera.zoom_by(ZOOM_OUT_FACTOR)
                elif key == b" ":
                    paused = not paused
                elif key == b"]":
                    time_scale *= 2.0
                elif key == b"[":
                    time_scale /= 2.0
                elif key == b"q":
                    return

            if not paused:
                # Update all galaxies/systems
                for galaxy in universe.galaxies:
                    for system in galaxy.systems:
                        system.update(t)
                t += DELTA_TIME * time_scale

            camera.update(DELTA_TIME)
            renderer.render(universe, status=f"Time: {t:.2f}s | Scale: {time_scale:.1f}x | Pos: {camera.center}")
            time.sleep(SLEEP)
    finally:
        renderer.show_cursor()


if __name__ == "__main__":
    main()
