from abc import ABC, abstractmethod
from typing import Type, TypeVar, Generic, List

from engine.body.base import BodyType, CelestialBody
from engine.camera import Camera

T = TypeVar("T", bound=CelestialBody)

class BodyRenderer(Generic[T], ABC):
    """Base interface for rendering a single celestial body."""

    @abstractmethod
    def draw(self, body: T, canvas: List[List[str]], sx: int, sy: int, width: int, height: int, camera: Camera) -> None:
        """
        Draw the body to the renderer.
        
        Args:
            body: The body to draw.
            canvas: The canvas to draw to.
            sx: The x coordinate of the system that the body is in. Used for relative positioning.
            sy: The y coordinate of the system that the body is in. Used for relative positioning.
            width: The width of the terminal.
            height: The height of the terminal.
            camera: The camera to use for rendering.
        """
        pass

# --- Renderer Registry ---

RENDERERS: dict[BodyType, Type[BodyRenderer]] = {}

def register_renderer(body_type: BodyType):
    """Decorator to register a renderer for a specific body type."""
    def decorator(cls):
        RENDERERS[body_type] = cls
        return cls
    
    return decorator

def get_renderer(body_type: BodyType) -> Type[BodyRenderer]:
    """Get the renderer for a specific body type."""
    if body_type not in RENDERERS:
        raise ValueError(f"No renderer registered for body type {body_type}") 
    
    return RENDERERS[body_type]