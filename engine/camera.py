from __future__ import annotations
from typing import Optional


class Camera:
    """Viewport state handling smooth panning and zooming."""

    def __init__(
        self,
        *,
        center: Optional[tuple[float, float]] = None,
        zoom: float = 1.0,
        target_zoom: Optional[float] = None,
        min_zoom: float = 0.1,
        max_zoom: float = 10.0,
        zoom_smoothing: float = 6.0,
    ) -> None:
        self.center = center or (0.0, 0.0)
        self.zoom = zoom
        self.target_zoom = target_zoom if target_zoom is not None else zoom
        self.min_zoom = min_zoom
        self.max_zoom = max_zoom
        self.zoom_smoothing = zoom_smoothing

    def pan(self, dx: float, dy: float) -> None:
        """Move the camera by (dx, dy)"""
        cx, cy = self.center
        self.center = (cx + dx, cy + dy)
    
    def zoom_by(self, factor: float) -> None:
        """Zoom the camera by a factor"""
        new_target = self.target_zoom * factor
        new_target = max(self.min_zoom, min(self.max_zoom, new_target))
        self.target_zoom = new_target

    def update(self, dt: float) -> None:
        """Update the camera state"""
        diff = self.target_zoom - self.zoom
        if abs(diff) < 1e-4:
            self.zoom = self.target_zoom
            return
        lerp = min(1.0, self.zoom_smoothing * dt)
        self.zoom += diff * lerp