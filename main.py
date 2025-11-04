import time
import msvcrt

from engine.body import Body
from engine.system import SolarSystem
from engine.galaxy import Galaxy
from engine.universe import Universe
from engine.renderer import Renderer
from engine.camera import Camera

DELTA_TIME = 1 # Simulation delta (how far things move each frame)
SLEEP = 0.02  # FPS Control (how often screen updates)
PAN_STEP = 2.0
ZOOM_IN_FACTOR = 0.9
ZOOM_OUT_FACTOR = 1.1
MAX_ZOOM = 2.0
MIN_ZOOM = 0.1

def main():
    # Create simple universe
    sun = Body.star(name="Sun", pos=(15, 15), velocity=(0, 0), mass=1000, radius=1)
    planet = Body.planet(name="PlanetA", pos=(0, 0), velocity=(0, 0), mass=1, radius=1)
    system = SolarSystem(name="SystemA", center=sun, bodies=[planet])
    galaxy = Galaxy(name="Milky-ish", pos=(0, 0), systems=[system])
    universe = Universe(galaxies=[galaxy])

    camera = Camera(center=sun.pos, zoom=0.5, max_zoom=MAX_ZOOM, min_zoom=MIN_ZOOM)
    renderer = Renderer(width=100, height=40, camera=camera)

    t = 0.0
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

        camera.update(DELTA_TIME)
        system.update(DELTA_TIME)
        renderer.render(universe)
        print(f"Time: {t:.2f}s")
        time.sleep(SLEEP)
        t += DELTA_TIME


if __name__ == "__main__":
    main()
