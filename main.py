import time
import msvcrt

from engine.body import Star, Planet
from engine.system import SolarSystem
from engine.galaxy import Galaxy
from engine.universe import Universe
from engine.renderer.ascii_renderer import AsciiRenderer
from engine.camera import Camera
from engine.body.planet import PlanetType

DELTA_TIME = 0.1 # Simulation delta (how far things move each frame)
SLEEP = 0.05  # FPS Control (how often screen updates)
PAN_STEP = 2.0
ZOOM_IN_FACTOR = 1.1
ZOOM_OUT_FACTOR = 0.9
MAX_ZOOM = 10.0
MIN_ZOOM = 0.1

def main():
    # Create simple universe
    sun = Star(name="Sun", pos=(5, 0), velocity=(0, 0), mass=1000, radius=5)
    planet1 = Planet(name="PlanetA", pos=(0, 10), velocity=(0, 0), mass=1, radius=1, planet_type=PlanetType.GAS_GIANT)
    planet2 = Planet(name="PlanetB", pos=(20, 0), velocity=(0, 0), mass=1, radius=1, planet_type=PlanetType.ICE_GIANT)
    planet3 = Planet(name="PlanetC", pos=(0, -10), velocity=(0, 0), mass=1, radius=1, planet_type=PlanetType.TERRESTRIAL)
    planet4 = Planet(name="PlanetD", pos=(-10, 0), velocity=(0, 0), mass=1, radius=1, planet_type=PlanetType.LAVA_GIANT)
    system = SolarSystem(name="SystemA", center=sun, bodies=[planet1, planet2, planet3, planet4])
    galaxy = Galaxy(name="Milky-ish", pos=(0, 0), systems=[system])
    universe = Universe(galaxies=[galaxy])

    camera = Camera(center=sun.pos, zoom=0.5, max_zoom=MAX_ZOOM, min_zoom=MIN_ZOOM)
    renderer = AsciiRenderer(width=100, height=40, camera=camera)

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
        renderer.render(universe, status=f"Time: {t:.2f}s")
        time.sleep(SLEEP)
        t += DELTA_TIME


if __name__ == "__main__":
    main()
