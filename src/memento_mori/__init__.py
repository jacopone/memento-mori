"""
Memento Mori - Life in Weeks

A thoughtful daily reminder of life's finite nature and the real time you have left.
"""

from .core import (
    LifeStats,
    FreeTimeStats,
    WorkLifeStats,
    ParentTimeStats,
    WeekendStats,
    calculate_all_stats,
)
from .config import MementoMoriConfig

__version__ = "0.1.0"
__all__ = [
    "LifeStats",
    "FreeTimeStats",
    "WorkLifeStats",
    "ParentTimeStats",
    "WeekendStats",
    "calculate_all_stats",
    "MementoMoriConfig",
]
