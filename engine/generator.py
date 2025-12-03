import random
import math
from typing import List, Tuple

from engine.universe import Universe
from engine.galaxy import Galaxy
from engine.system import SolarSystem
from engine.body.base import CelestialBody, BodyType
from engine.body.star import Star
from engine.body.planet import Planet, PlanetType
from engine.physics import Orbit

class UniverseGenerator:
    """Generates a procedural universe."""

    def __init__(self, seed: int = None):
        if seed:
            random.seed(seed)

    def generate_universe(self, num_galaxies: int = 3) -> Universe:
        galaxies = []
        for i in range(num_galaxies):
            pos = (random.uniform(-1000, 1000), random.uniform(-1000, 1000))
            galaxies.append(self.generate_galaxy(f"Galaxy-{i}", pos))
        return Universe(galaxies=galaxies)

    def generate_galaxy(self, name: str, pos: Tuple[float, float], num_systems: int = 5) -> Galaxy:
        systems = []
        for i in range(num_systems):
            # Scatter systems around galaxy center
            angle = random.uniform(0, 2 * math.pi)
            dist = random.uniform(10, 200)
            sys_pos = (pos[0] + dist * math.cos(angle), pos[1] + dist * math.sin(angle))
            
            systems.append(self.generate_system(f"{name}-Sys-{i}", sys_pos))
        
        return Galaxy(name=name, pos=pos, systems=systems)

    def generate_system(self, name: str, pos: Tuple[float, float]) -> SolarSystem:
        # Create a star
        star = Star(
            name=f"{name}-Star",
            pos=pos,
            velocity=(0, 0),
            mass=random.uniform(0.5, 5.0) * 1000,
            radius=random.uniform(2, 10)
        )

        # Generate planets
        num_planets = random.randint(1, 8)
        for i in range(num_planets):
            dist = random.uniform(10, 100) + (i * 15)
            planet = self.generate_planet(f"{name}-P{i}", dist)
            star.add_child(planet, planet.orbit)

        return SolarSystem(name=name, center=star)

    def generate_planet(self, name: str, distance: float) -> Planet:
        p_type = random.choice(list(PlanetType))
        mass = random.uniform(0.1, 10)
        radius = random.uniform(0.5, 2)
        
        # Create orbit
        orbit = Orbit(
            semi_major_axis=distance,
            eccentricity=random.uniform(0, 0.2),
            inclination=0,
            argument_of_periapsis=random.uniform(0, 2 * math.pi),
            mean_anomaly_at_epoch=random.uniform(0, 2 * math.pi),
            period=math.sqrt(distance**3) # Simplified Kepler's 3rd law (ignoring G and M for now)
        )

        planet = Planet(
            name=name,
            pos=(0, 0), # Position will be calculated by orbit
            velocity=(0, 0),
            mass=mass,
            radius=radius,
            planet_type=p_type
        )
        planet.orbit = orbit

        # Chance for moons
        if random.random() < 0.5:
            num_moons = random.randint(1, 3)
            for i in range(num_moons):
                moon_dist = random.uniform(2, 5) + (i * 1)
                moon = self.generate_moon(f"{name}-M{i}", moon_dist)
                planet.add_child(moon, moon.orbit)

        return planet

    def generate_moon(self, name: str, distance: float) -> Planet:
        # Moons are just small planets for now
        orbit = Orbit(
            semi_major_axis=distance,
            eccentricity=random.uniform(0, 0.1),
            inclination=0,
            argument_of_periapsis=random.uniform(0, 2 * math.pi),
            mean_anomaly_at_epoch=random.uniform(0, 2 * math.pi),
            period=math.sqrt(distance**3) * 0.2 # Faster orbits for moons
        )
        
        moon = Planet(
            name=name,
            pos=(0, 0),
            velocity=(0, 0),
            mass=0.01,
            radius=0.2,
            planet_type=PlanetType.TERRESTRIAL
        )
        moon.orbit = orbit
        return moon
