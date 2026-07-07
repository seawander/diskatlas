"""Aggregates all seed modules.

To add a new survey/system batch: create or extend a module here, exposing
BLOCKS (survey blocks) and/or SYSTEMS (individual systems), then import it below.
"""
from . import alma_proto, alma_debris, scattered, scattered2, scattered3, planets, planets2

ALL_BLOCKS = []
ALL_SYSTEMS = []
for mod in (alma_proto, alma_debris, scattered, scattered2, scattered3, planets, planets2):
    ALL_BLOCKS.extend(getattr(mod, "BLOCKS", []))
    ALL_SYSTEMS.extend(getattr(mod, "SYSTEMS", []))
