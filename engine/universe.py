from dataclasses import dataclass, field
from typing import List

from .galaxy import Galaxy


@dataclass
class Universe:
    """The top-level container of galaxies"""

    galaxies: List[Galaxy] = field(default_factory=list)

    def add_galaxy(self, galaxy: Galaxy) -> None:
        self.galaxies.append(galaxy)