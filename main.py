import time

from engine.body import Body
from engine.system import SolarSystem
from engine.galaxy import Galaxy
from engine.universe import Universe
from engine.renderer import Renderer

DELTA_TIME = 2 # Simulation delta (how far things move each frame)
SLEEP = 0.5  # FPS Control (how often screen updates)

def main():
    # Create simple universe
    sun = Body(name="Sun", pos=(5, 4), velocity=(0, 0), mass=1000, symbol="☉")
    planet = Body(name="PlanetA", pos=(0, 0), velocity=(0, 0), mass=1, symbol="•")
    system = SolarSystem(name="SystemA", center=sun, bodies=[planet])
    galaxy = Galaxy(name="Milky-ish", pos=(0, 0), systems=[system])
    universe = Universe(galaxies=[galaxy])

    renderer = Renderer(width=100, height=40)

    t = 0.0
    while True:
        system.update(DELTA_TIME)
        renderer.render(universe)
        print(f"Time: {t:.2f}s")
        time.sleep(SLEEP)
        t += DELTA_TIME


if __name__ == "__main__":
    main()
