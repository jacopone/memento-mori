"""
Configuration management for Memento Mori.

Handles loading, saving, and validating user configuration.
"""

import json
from datetime import date, datetime
from pathlib import Path


class MementoMoriConfig:
    """Manage memento-mori configuration."""

    def __init__(self, config_path: Path | None = None):
        """Initialize configuration manager."""
        self.config_path = config_path or Path.home() / ".config/memento-mori/config.json"
        self.config = self._load_config()

    def _load_config(self) -> dict:
        """Load configuration from file or create default."""
        if not self.config_path.exists():
            return self._create_default_config()

        try:
            with open(self.config_path) as f:
                return json.load(f)
        except Exception:
            return self._create_default_config()

    def _create_default_config(self) -> dict:
        """Create and save default configuration."""
        config = {
            "birthdate": "1990-01-01",
            "expected_lifespan": 80,
            "retirement_age": 67,
            "vacation_weeks_per_year": 3,
            "time_assumptions": {
                "sleep_hours_per_day": 9.0,
                "work_hours_per_day": 8.1,
                "chores_hours_per_day": 2.0,
                "work_hours_per_week": 40.0,
            },
            "life_milestones": {
                "started_working_age": 22,
                "parent_life_expectancy": 80,
            },
            "parents": {
                "father_age": None,
                "mother_age": None,
                "visits_per_year": 10,
                "days_per_visit": 2,
            },
            "notification_time": "08:00",
            "notification_style": "motivational",
            "show_grid": False,
        }

        self.config_path.parent.mkdir(parents=True, exist_ok=True)
        self._save_config(config)
        return config

    def _save_config(self, config: dict) -> None:
        """Save configuration to file."""
        try:
            with open(self.config_path, "w") as f:
                json.dump(config, f, indent=2)
        except Exception as e:
            print(f"Warning: Could not save config: {e}")

    def get_birthdate(self) -> date:
        """Get birthdate from config."""
        birthdate_str = self.config.get("birthdate", "1990-01-01")
        return datetime.strptime(birthdate_str, "%Y-%m-%d").date()

    def get(self, key: str, default=None):
        """Get configuration value."""
        return self.config.get(key, default)

    def get_time_assumption(self, key: str, default: float) -> float:
        """Get time assumption value with fallback."""
        return self.config.get("time_assumptions", {}).get(key, default)

    def get_life_milestone(self, key: str, default: int) -> int:
        """Get life milestone value with fallback."""
        return self.config.get("life_milestones", {}).get(key, default)

    def edit_with_editor(self) -> None:
        """Open config in default editor."""
        import os
        import subprocess

        editor = os.environ.get("EDITOR", "nano")
        subprocess.run([editor, str(self.config_path)])
