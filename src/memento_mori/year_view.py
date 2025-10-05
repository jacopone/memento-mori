"""
Year View - Current year statistics and planning.

Provides a focused view of the current year with weekend planning
and family time suggestions.
"""

from dataclasses import dataclass
from datetime import date, datetime, timedelta

from rich import box
from rich.console import Console
from rich.panel import Panel
from rich.table import Table
from rich.text import Text

console = Console()


@dataclass
class YearStats:
    """Calculate current year statistics."""

    today: date = None

    def __post_init__(self):
        if self.today is None:
            self.today = datetime.now().date()

    @property
    def year_start(self) -> date:
        """First day of current year."""
        return date(self.today.year, 1, 1)

    @property
    def year_end(self) -> date:
        """Last day of current year."""
        return date(self.today.year, 12, 31)

    @property
    def days_in_year(self) -> int:
        """Total days in current year."""
        return (self.year_end - self.year_start).days + 1

    @property
    def days_elapsed(self) -> int:
        """Days elapsed in current year."""
        return (self.today - self.year_start).days

    @property
    def days_remaining(self) -> int:
        """Days remaining in current year."""
        return (self.year_end - self.today).days

    @property
    def weeks_remaining(self) -> float:
        """Weeks remaining in current year."""
        return self.days_remaining / 7

    @property
    def months_remaining(self) -> int:
        """Full months remaining in current year."""
        return 12 - self.today.month

    @property
    def year_progress_percentage(self) -> float:
        """Percentage of year completed."""
        return (self.days_elapsed / self.days_in_year) * 100

    def get_remaining_weekends(self) -> list[tuple[date, date]]:
        """Get all remaining weekends (Sat-Sun) in current year."""
        weekends = []
        current = self.today

        # Find next Saturday
        days_until_saturday = (5 - current.weekday()) % 7
        if days_until_saturday == 0 and current.weekday() != 5:
            days_until_saturday = 7

        next_saturday = current + timedelta(days=days_until_saturday)

        # Collect all weekends until end of year
        while next_saturday <= self.year_end:
            sunday = next_saturday + timedelta(days=1)
            if sunday <= self.year_end:
                weekends.append((next_saturday, sunday))
            next_saturday += timedelta(days=7)

        return weekends

    def get_months_remaining_list(self) -> list[str]:
        """Get list of remaining months by name."""
        months = [
            "January",
            "February",
            "March",
            "April",
            "May",
            "June",
            "July",
            "August",
            "September",
            "October",
            "November",
            "December",
        ]
        return months[self.today.month :]

    def calculate_free_weekend_days(
        self, free_time_percentage: float, obligations_on_weekends: bool = True
    ) -> int:
        """
        Calculate truly free weekend days.

        Args:
            free_time_percentage: Percentage of day that's free (from FreeTimeStats)
            obligations_on_weekends: Whether obligations apply to weekends
        """
        total_weekend_days = len(self.get_remaining_weekends()) * 2

        if obligations_on_weekends:
            # Adjust for sleep/chores even on weekends
            return int(total_weekend_days * (free_time_percentage / 100))
        else:
            # Weekends are fully free
            return total_weekend_days


def create_year_progress_bar(percentage: float, width: int = 50) -> Text:
    """Create a visual progress bar for year completion."""
    filled = int((percentage / 100) * width)
    bar = "█" * filled + "░" * (width - filled)

    color = "green" if percentage < 75 else "yellow" if percentage < 90 else "red"

    text = Text()
    text.append(bar, style=color)
    text.append(f" {percentage:.1f}%", style="bold white")
    return text


def display_year_view(year_stats: YearStats, free_time_percentage: float = 20.4):
    """
    Display current year overview with planning information.

    Args:
        year_stats: YearStats instance with current year calculations
        free_time_percentage: Percentage of day that's free (from FreeTimeStats)
    """
    title = Text(f"📅 YOUR {year_stats.today.year} YEAR OVERVIEW", style="bold white on black")

    # Main statistics table
    table = Table(show_header=False, box=box.SIMPLE, padding=(0, 2))
    table.add_column("Metric", style="cyan")
    table.add_column("Value", style="bold white")

    # Current date info
    current_date = year_stats.today.strftime("%B %d, %Y")
    table.add_row("📅 Today", current_date)
    table.add_row("")

    # Year progress
    progress_text = Text()
    progress_text.append("Year Progress: ", style="bold")
    progress_bar = create_year_progress_bar(year_stats.year_progress_percentage)

    # Time remaining
    table.add_row("⏰ Days Remaining", f"{year_stats.days_remaining:,}")
    table.add_row("📊 Weeks Remaining", f"{year_stats.weeks_remaining:.1f}")
    table.add_row("📆 Months Remaining", str(year_stats.months_remaining))

    # Remaining months list
    remaining_months = year_stats.get_months_remaining_list()
    if remaining_months:
        months_text = ", ".join(remaining_months)
        table.add_row("", Text(months_text, style="dim"))

    # Weekends section
    weekends = year_stats.get_remaining_weekends()
    table.add_row("")
    table.add_row("🌅 Weekends Remaining", f"{len(weekends)} weekends")
    table.add_row("", f"{len(weekends) * 2} weekend days")

    # Free time calculation
    free_weekend_days = year_stats.calculate_free_weekend_days(free_time_percentage)
    table.add_row("")
    table.add_row("💡 Realistic Free Time", f"~{free_weekend_days} truly free weekend days")

    # Weekend list
    weekend_text = Text()
    weekend_text.append("\n🗓️  UPCOMING WEEKENDS\n", style="bold cyan")

    # Group weekends by month
    current_month = None
    for saturday, sunday in weekends:
        month = saturday.strftime("%B")
        if month != current_month:
            weekend_text.append(f"\n{month}:\n", style="bold yellow")
            current_month = month

        weekend_range = f"{saturday.strftime('%b %d')}-{sunday.strftime('%d')}"
        weekend_text.append(f"  • {weekend_range}\n", style="white")

    # Planning suggestions
    planning_text = Text()
    planning_text.append("\n💭 FAMILY TIME PLANNING\n", style="bold cyan")

    suggested_gatherings = max(2, free_weekend_days // 8)  # One gathering every ~8 free days
    planning_text.append(f"  • Available: {len(weekends) * 2} weekend days total\n", style="white")
    planning_text.append(
        f"  • Realistic after obligations: ~{free_weekend_days} days\n", style="white"
    )
    planning_text.append(
        f"  • Suggested gatherings: {suggested_gatherings}-{suggested_gatherings + 1} "
        f"family/friend events\n",
        style="green",
    )
    planning_text.append("  • Time per event: Plan for 1-2 days each\n", style="dim")

    # Compile panel content
    panel_content = Table.grid(padding=(0, 0))
    panel_content.add_row("")
    panel_content.add_row(progress_text)
    panel_content.add_row(progress_bar)
    panel_content.add_row("")
    panel_content.add_row(table)
    panel_content.add_row(weekend_text)
    panel_content.add_row(planning_text)
    panel_content.add_row("")
    panel_content.add_row(
        Text(
            "Make the most of your remaining weekends! Time with loved ones is precious.",
            style="italic dim green",
        )
    )

    panel = Panel(
        panel_content,
        title=title,
        border_style="white",
        padding=(1, 2),
    )

    console.print()
    console.print(panel)
    console.print()
