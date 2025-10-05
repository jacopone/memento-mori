"""
Memento Mori - Life in Weeks Calculator

Core calculations for life statistics and time tracking.
"""

from dataclasses import dataclass
from datetime import date, datetime
from typing import Optional


@dataclass
class LifeStats:
    """Calculate and store comprehensive life statistics."""

    birthdate: date
    expected_lifespan: int = 80
    retirement_age: int = 67
    work_hours_per_week: float = 40
    vacation_weeks_per_year: int = 3

    @property
    def age_years(self) -> float:
        """Current age in years."""
        delta = datetime.now().date() - self.birthdate
        return delta.days / 365.25

    @property
    def weeks_lived(self) -> int:
        """Weeks lived since birth."""
        delta = datetime.now().date() - self.birthdate
        return delta.days // 7

    @property
    def total_weeks(self) -> int:
        """Total weeks in expected lifespan."""
        return self.expected_lifespan * 52

    @property
    def weeks_remaining(self) -> int:
        """Estimated weeks remaining."""
        return max(0, self.total_weeks - self.weeks_lived)

    @property
    def percentage_lived(self) -> float:
        """Percentage of expected life lived."""
        return (self.weeks_lived / self.total_weeks) * 100

    @property
    def days_remaining(self) -> int:
        """Estimated days remaining."""
        return self.weeks_remaining * 7

    @property
    def years_remaining(self) -> float:
        """Estimated years remaining."""
        return self.weeks_remaining / 52


@dataclass
class FreeTimeStats:
    """Calculate truly free time after obligations."""

    life_stats: LifeStats
    sleep_hours_per_day: float = 9.0
    work_hours_per_day: float = 8.1
    chores_hours_per_day: float = 2.0

    @property
    def total_obligated_hours_per_day(self) -> float:
        """Hours per day spent on obligations."""
        return self.sleep_hours_per_day + self.work_hours_per_day + self.chores_hours_per_day

    @property
    def free_hours_per_day(self) -> float:
        """Truly free hours per day."""
        return max(0, 24 - self.total_obligated_hours_per_day)

    @property
    def free_time_percentage(self) -> float:
        """Percentage of life that is truly free."""
        return (self.free_hours_per_day / 24) * 100

    @property
    def free_weeks_lived(self) -> int:
        """Free weeks lived (adjusted for obligations)."""
        return int(self.life_stats.weeks_lived * (self.free_time_percentage / 100))

    @property
    def free_weeks_remaining(self) -> int:
        """Free weeks remaining (adjusted for obligations)."""
        return int(self.life_stats.weeks_remaining * (self.free_time_percentage / 100))


@dataclass
class WorkLifeStats:
    """Calculate work and vacation statistics."""

    life_stats: LifeStats
    started_working_age: int = 22

    @property
    def years_until_retirement(self) -> float:
        """Years remaining until retirement."""
        return max(0, self.life_stats.retirement_age - self.life_stats.age_years)

    @property
    def weeks_until_retirement(self) -> int:
        """Weeks remaining until retirement."""
        return int(self.years_until_retirement * 52)

    @property
    def vacation_weeks_remaining(self) -> int:
        """Total vacation weeks remaining in working life."""
        return int(self.years_until_retirement * self.life_stats.vacation_weeks_per_year)


@dataclass
class ParentTimeStats:
    """Calculate time remaining with parents ('See Your Folks' style)."""

    father_age: Optional[int] = None
    mother_age: Optional[int] = None
    visits_per_year: int = 10
    days_per_visit: int = 2
    parent_life_expectancy: int = 80

    def days_left_with_father(self) -> Optional[int]:
        """Estimated days left with father."""
        if not self.father_age:
            return None
        years_left = max(0, self.parent_life_expectancy - self.father_age)
        return int(years_left * self.visits_per_year * self.days_per_visit)

    def days_left_with_mother(self) -> Optional[int]:
        """Estimated days left with mother."""
        if not self.mother_age:
            return None
        years_left = max(0, self.parent_life_expectancy - self.mother_age)
        return int(years_left * self.visits_per_year * self.days_per_visit)

    def total_days_left(self) -> int:
        """Combined days left with both parents."""
        father_days = self.days_left_with_father() or 0
        mother_days = self.days_left_with_mother() or 0
        return father_days + mother_days


@dataclass
class WeekendStats:
    """Calculate remaining weekends and free time."""

    life_stats: LifeStats

    @property
    def weekends_remaining(self) -> int:
        """Saturday/Sunday weekends remaining."""
        return int(self.life_stats.weeks_remaining)

    @property
    def weekend_days_remaining(self) -> int:
        """Total weekend days (Sat + Sun) remaining."""
        return self.weekends_remaining * 2


def calculate_all_stats(
    birthdate: date,
    expected_lifespan: int = 80,
    retirement_age: int = 67,
    father_age: Optional[int] = None,
    mother_age: Optional[int] = None,
    visits_per_year: int = 10,
) -> dict:
    """
    Calculate all life statistics.

    Returns dictionary with all stat objects for easy access.
    """
    life_stats = LifeStats(
        birthdate=birthdate,
        expected_lifespan=expected_lifespan,
        retirement_age=retirement_age,
    )

    return {
        "life": life_stats,
        "free_time": FreeTimeStats(life_stats),
        "work": WorkLifeStats(life_stats),
        "parents": ParentTimeStats(father_age, mother_age, visits_per_year),
        "weekends": WeekendStats(life_stats),
    }
