from dataclasses import dataclass, field
from typing import List, Tuple

from .system import SolarSystem


@dataclass
class Galaxy:
    """A galaxy containing multiple solar systems"""

    name: str
    pos: Tuple[float, float]
    systems: List[SolarSystem] = field(default_factory=list)