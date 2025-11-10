"""Renderer package initialization."""

# Import body renderers so their registration decorators run at import time.
from .body_renderers import star_renderer
from .body_renderers import planet_renderer