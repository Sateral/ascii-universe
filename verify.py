import sys
import os

# Add current directory to path
sys.path.append(os.getcwd())

from engine.generator import UniverseGenerator
from engine.renderer.ascii_renderer import AsciiRenderer
from engine.camera import Camera

def test_universe_generation():
    print("Testing Universe Generation...")
    generator = UniverseGenerator(seed=123)
    universe = generator.generate_universe(num_galaxies=1)
    
    assert len(universe.galaxies) == 1
    galaxy = universe.galaxies[0]
    print(f"Galaxy generated: {galaxy.name} with {len(galaxy.systems)} systems")
    
    assert len(galaxy.systems) > 0
    system = galaxy.systems[0]
    print(f"System generated: {system.name} with center {system.center.name}")
    
    assert len(system.center.children) > 0
    planet = system.center.children[0]
    print(f"Planet generated: {planet.name} with orbit {planet.orbit}")
    
    return universe

def test_physics_update(universe):
    print("\nTesting Physics Update...")
    system = universe.galaxies[0].systems[0]
    planet = system.center.children[0]
    
    start_pos = planet.pos
    print(f"Start Pos: {start_pos}")
    
    # Update system
    system.update(1000.0)
    
    end_pos = planet.pos
    print(f"End Pos: {end_pos}")
    
    assert start_pos != end_pos
    print("Physics update successful (position changed)")

def test_renderer(universe):
    print("\nTesting Renderer...")
    camera = Camera(center=(0,0), zoom=1.0)
    renderer = AsciiRenderer(width=80, height=20, camera=camera)
    
    try:
        renderer.render(universe, status="Test Status")
        print("Render successful")
    except Exception as e:
        print(f"Render failed: {e}")
        raise

if __name__ == "__main__":
    with open("verify.log", "w") as f:
        sys.stdout = f
        sys.stderr = f
        try:
            universe = test_universe_generation()
            test_physics_update(universe)
            test_renderer(universe)
            print("\nAll tests passed!")
        except Exception as e:
            print(f"\nTests failed: {e}")
            sys.exit(1)
