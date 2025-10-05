"""
Memento Mori CLI - Command-line interface with Rich UI.
"""

import argparse

from rich import box
from rich.console import Console
from rich.panel import Panel
from rich.table import Table
from rich.text import Text

from .config import MementoMoriConfig
from .core import calculate_all_stats
from .year_view import YearStats, display_year_view

console = Console()


def get_wisdom_quote(percentage_lived: float) -> str:
    """Get contextual wisdom based on life stage."""
    quotes = {
        0: "Every beginning is a consequence. — Paul Valéry",
        20: "The days are long but the decades are short. — Sam Altman",
        40: "The only way to do great work is to love what you do. — Steve Jobs",
        60: "Do not regret growing older. It is a privilege denied to many.",
        80: "The fear of death follows from the fear of life. Live fully. — Mark Twain",
    }

    for threshold in sorted(quotes.keys(), reverse=True):
        if percentage_lived >= threshold:
            return quotes[threshold]

    return "Time is the most valuable thing a person can spend. — Theophrastus"


def create_progress_bar(percentage: float, width: int = 50) -> Text:
    """Create a visual progress bar."""
    filled = int((percentage / 100) * width)
    bar = "█" * filled + "░" * (width - filled)

    color = "yellow" if percentage < 50 else "red"

    text = Text()
    text.append(bar, style=color)
    text.append(f" {percentage:.1f}%", style="bold white")
    return text


def display_life_grid(config: MementoMoriConfig):
    """
    Display life as a grid of weeks (90 years × 52 weeks).

    Similar to Wait But Why's visualization - each box is a week.
    """
    birthdate = config.get_birthdate()
    stats = calculate_all_stats(
        birthdate=birthdate,
        expected_lifespan=config.get("expected_lifespan", 80),
        retirement_age=config.get("retirement_age", 67),
        work_hours_per_week=config.get("work_hours_per_week", 40.0),
        vacation_weeks_per_year=config.get("vacation_weeks_per_year", 3),
        sleep_hours_per_day=config.get_time_assumption("sleep_hours_per_day", 9.0),
        work_hours_per_day=config.get_time_assumption("work_hours_per_day", 8.1),
        chores_hours_per_day=config.get_time_assumption("chores_hours_per_day", 2.0),
        started_working_age=config.get_life_milestone("started_working_age", 22),
        father_age=config.get("parents", {}).get("father_age"),
        mother_age=config.get("parents", {}).get("mother_age"),
        visits_per_year=config.get("parents", {}).get("visits_per_year", 10),
        days_per_visit=config.get("parents", {}).get("days_per_visit", 2),
        parent_life_expectancy=config.get_life_milestone("parent_life_expectancy", 80),
    )

    life = stats["life"]
    weeks_lived = life.weeks_lived
    expected_lifespan = life.expected_lifespan

    title = Text("⏳ YOUR LIFE IN WEEKS", style="bold white on black")
    subtitle = Text(
        f"Each box is one week. {expected_lifespan} years = {expected_lifespan * 52:,} weeks total",
        style="dim",
    )

    # Create the grid
    grid_text = Text()

    # Add decade markers and weeks
    for year in range(expected_lifespan):
        # Decade marker every 10 years
        if year % 10 == 0:
            grid_text.append(f"\n{year:>2} ", style="bold yellow")
        else:
            grid_text.append(f"\n{year:>2} ", style="dim")

        # 52 weeks per year
        for week in range(52):
            week_number = year * 52 + week

            if week_number < weeks_lived:
                # Past weeks - filled
                grid_text.append("█", style="green")
            elif week_number == weeks_lived:
                # Current week - highlighted
                grid_text.append("█", style="bold yellow")
            elif week_number < life.total_weeks:
                # Future weeks within expected lifespan
                grid_text.append("□", style="dim white")
            else:
                # Beyond expected lifespan
                grid_text.append("·", style="dim red")

    # Legend
    legend = Text()
    legend.append("\n\nLegend: ", style="bold")
    legend.append("█ ", style="green")
    legend.append("Week lived  ")
    legend.append("█ ", style="bold yellow")
    legend.append("Current week  ")
    legend.append("□ ", style="dim white")
    legend.append("Week remaining  ")
    legend.append("· ", style="dim red")
    legend.append("Beyond expected lifespan")

    # Stats summary
    summary = Text()
    summary.append("\n\n📊 Stats: ", style="bold cyan")
    summary.append(f"{weeks_lived:,} weeks lived ", style="green")
    summary.append("• ")
    summary.append(f"{life.weeks_remaining:,} weeks remaining ", style="white")
    summary.append("• ")
    summary.append(f"{life.percentage_lived:.1f}% complete", style="yellow")

    # Compile panel
    panel_content = Table.grid(padding=(0, 0))
    panel_content.add_row(subtitle)
    panel_content.add_row(grid_text)
    panel_content.add_row(legend)
    panel_content.add_row(summary)
    panel_content.add_row("")
    panel_content.add_row(
        Text("Every week counts. Make them meaningful.", style="italic dim green")
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


def display_summary(config: MementoMoriConfig, notification: bool = False):
    """Display life statistics summary."""
    birthdate = config.get_birthdate()
    stats = calculate_all_stats(
        birthdate=birthdate,
        expected_lifespan=config.get("expected_lifespan", 80),
        retirement_age=config.get("retirement_age", 67),
        work_hours_per_week=config.get("work_hours_per_week", 40.0),
        vacation_weeks_per_year=config.get("vacation_weeks_per_year", 3),
        sleep_hours_per_day=config.get_time_assumption("sleep_hours_per_day", 9.0),
        work_hours_per_day=config.get_time_assumption("work_hours_per_day", 8.1),
        chores_hours_per_day=config.get_time_assumption("chores_hours_per_day", 2.0),
        started_working_age=config.get_life_milestone("started_working_age", 22),
        father_age=config.get("parents", {}).get("father_age"),
        mother_age=config.get("parents", {}).get("mother_age"),
        visits_per_year=config.get("parents", {}).get("visits_per_year", 10),
        days_per_visit=config.get("parents", {}).get("days_per_visit", 2),
        parent_life_expectancy=config.get_life_milestone("parent_life_expectancy", 80),
    )

    life = stats["life"]
    free_time = stats["free_time"]
    work = stats["work"]
    parents = stats["parents"]
    weekends = stats["weekends"]

    if notification:
        # Simple notification format
        msg = f"⏳ Weeks lived: {life.weeks_lived:,} | Remaining: {life.weeks_remaining:,}\n"
        msg += f"💫 {life.percentage_lived:.1f}% of your expected life has passed\n"
        if parents.total_days_left() > 0:
            msg += f"👨‍👩‍👧 ~{parents.total_days_left()} days left with parents\n"
        msg += "⚡ Make today count."
        print(msg)
        return

    # Rich terminal output
    title = Text("⏳ MEMENTO MORI - THE REAL TIME", style="bold white on black")
    subtitle = Text("Remember you will die. Remember you will live.", style="italic dim")

    # Create main statistics table
    table = Table(show_header=False, box=box.SIMPLE, padding=(0, 2))
    table.add_column("Metric", style="cyan")
    table.add_column("Value", style="bold white")

    # Life statistics
    table.add_row("📅 Weeks Lived", f"{life.weeks_lived:,}")
    table.add_row("⏰ Weeks Remaining", f"{life.weeks_remaining:,}")
    table.add_row("📊 Percentage Lived", f"{life.percentage_lived:.1f}%")
    table.add_row("🎂 Current Age", f"{life.age_years:.1f} years")
    table.add_row("🌅 Years Remaining", f"{life.years_remaining:.1f} years")

    # Progress bar
    progress_text = Text()
    progress_text.append("Life Progress: ", style="bold")
    progress_bar = create_progress_bar(life.percentage_lived)

    # Free time section
    free_time_text = Text()
    free_time_text.append("\n💼 TRULY FREE TIME (sleep/work removed)\n", style="bold cyan")
    free_time_text.append(
        f"   Free weeks lived: {free_time.free_weeks_lived:,} | "
        f"Remaining: {free_time.free_weeks_remaining:,}\n",
        style="white",
    )
    free_time_text.append(
        f"   Only {free_time.free_time_percentage:.1f}% of each day is truly yours", style="dim"
    )

    # Work section
    work_text = Text()
    work_text.append("\n🏢 WORKING LIFE\n", style="bold cyan")
    work_text.append(
        f"   Years until retirement: {work.years_until_retirement:.1f} "
        f"({work.weeks_until_retirement:,} weeks)\n",
        style="white",
    )
    work_text.append(
        f"   Vacation weeks remaining: ~{work.vacation_weeks_remaining} weeks", style="white"
    )

    # Parent time section
    parent_text = Text()
    if parents.total_days_left() > 0:
        parent_text.append("\n👨‍👩‍👧 FAMILY TIME\n", style="bold cyan")
        if parents.days_left_with_father():
            parent_text.append(
                f"   Days left with father: ~{parents.days_left_with_father()} days\n",
                style="white",
            )
        if parents.days_left_with_mother():
            parent_text.append(
                f"   Days left with mother: ~{parents.days_left_with_mother()} days\n",
                style="white",
            )
        parent_text.append("   90% of lifetime with them: Already spent", style="yellow")

    # Weekend section
    weekend_text = Text()
    weekend_text.append("\n🌅 WEEKENDS LEFT\n", style="bold cyan")
    weekend_text.append(
        f"   Saturday/Sunday freedom: ~{weekends.weekends_remaining:,} weekends", style="white"
    )

    # Wisdom quote
    wisdom = get_wisdom_quote(life.percentage_lived)

    # Compile panel content
    panel_content = Table.grid(padding=(0, 0))
    panel_content.add_row(subtitle)
    panel_content.add_row("")
    panel_content.add_row(table)
    panel_content.add_row("")
    panel_content.add_row(progress_text)
    panel_content.add_row(progress_bar)
    panel_content.add_row(free_time_text)
    panel_content.add_row(work_text)
    if parents.total_days_left() > 0:
        panel_content.add_row(parent_text)
    panel_content.add_row(weekend_text)
    panel_content.add_row("")
    panel_content.add_row(Text(wisdom, style="italic dim green"))

    panel = Panel(
        panel_content,
        title=title,
        border_style="white",
        padding=(1, 2),
    )

    console.print()
    console.print(panel)
    console.print()


def main():
    """Main CLI entry point."""
    parser = argparse.ArgumentParser(
        description="Memento Mori - Life in Weeks Reminder",
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    parser.add_argument("--grid", action="store_true", help="Show life in weeks grid visualization")
    parser.add_argument(
        "--year", action="store_true", help="Show current year overview with weekend planning"
    )
    parser.add_argument("--notify", action="store_true", help="Notification mode (simple output)")
    parser.add_argument("--config", action="store_true", help="Edit configuration file")

    args = parser.parse_args()

    config = MementoMoriConfig()

    if args.config:
        config.edit_with_editor()
        return

    if args.year:
        # Display year view
        year_stats = YearStats()
        # Calculate free time percentage from config
        birthdate = config.get_birthdate()
        stats = calculate_all_stats(
            birthdate=birthdate,
            expected_lifespan=config.get("expected_lifespan", 80),
            retirement_age=config.get("retirement_age", 67),
            work_hours_per_week=config.get("work_hours_per_week", 40.0),
            vacation_weeks_per_year=config.get("vacation_weeks_per_year", 3),
            sleep_hours_per_day=config.get_time_assumption("sleep_hours_per_day", 9.0),
            work_hours_per_day=config.get_time_assumption("work_hours_per_day", 8.1),
            chores_hours_per_day=config.get_time_assumption("chores_hours_per_day", 2.0),
            started_working_age=config.get_life_milestone("started_working_age", 22),
            father_age=config.get("parents", {}).get("father_age"),
            mother_age=config.get("parents", {}).get("mother_age"),
            visits_per_year=config.get("parents", {}).get("visits_per_year", 10),
            days_per_visit=config.get("parents", {}).get("days_per_visit", 2),
            parent_life_expectancy=config.get_life_milestone("parent_life_expectancy", 80),
        )
        free_time_percentage = stats["free_time"].free_time_percentage
        display_year_view(year_stats, free_time_percentage)
        return

    if args.grid:
        display_life_grid(config)
        return

    display_summary(config, notification=args.notify)


if __name__ == "__main__":
    main()
