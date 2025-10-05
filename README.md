# ⏳ Memento Mori - Life in Weeks

**A thoughtful daily reminder of life's finite nature and the real time you have left.**

> "Memento Mori" - Remember you will die.
> "Memento Vivere" - Remember you will live.

## What Is This?

Memento Mori is a CLI tool and daily notification system that visualizes your life in weeks, showing not just total time, but the **meaningful time** you actually have:

- **Total weeks**: Traditional "life in weeks" concept (80 years = 4,160 weeks)
- **Free weeks**: Time after removing sleep and work obligations
- **Vacation time**: Remaining vacation weeks in your working life
- **Family time**: Days left with aging parents (the "See Your Folks" calculation)
- **Quality time**: Years of healthy, active living vs. declining health

## The Brutal Truth

Research shows:

- **By age 20**: You've already spent 90% of total lifetime days with your parents
- **After moving out**: Most people see parents only ~10 days/year
- **Daily reality**: ~9 hours sleep + ~8 hours work = only **4-5 hours of truly free time**
- **With children**: 75% of time spent with them happens before age 12

This isn't about being morbid - it's about **making the finite time visible so you actually use it wisely**.

## Features

### 📊 Multi-Perspective Time Tracking

- **Total Life View**: Classic weeks lived vs. remaining
- **Real Free Time**: Adjusted for sleep, work, and obligations
- **Vacation Calculator**: Remaining vacation weeks until retirement
- **Parent Time Tracker**: "See Your Folks" - days left based on visit frequency
- **Children Milestones**: Time remaining in critical development windows
- **Health-Adjusted Time**: Prime years vs. declining health expectations
- **Weekend Counter**: Tangible "free weekends" remaining

### 🎨 Rich Terminal UI

- Beautiful progress bars and statistics powered by Rich library
- Optional grid visualization (90×52 grid showing each week)
- Contextual wisdom quotes based on life stage
- Multiple display modes (summary, grid, notification)

### 🔔 Daily Notifications

- GNOME desktop notifications at configurable time
- Two styles: "motivational" or "sobering"
- Gentle reminders to make today count
- Systemd user timer integration (no sudo required)

### ⚙️ Configurable

Simple JSON config at `~/.config/memento-mori/config.json`:

```json
{
  "birthdate": "1990-01-01",
  "expected_lifespan": 80,
  "retirement_age": 67,
  "vacation_weeks_per_year": 3,
  "parents": {
    "father_age": 65,
    "mother_age": 63,
    "visits_per_year": 10
  },
  "notification_time": "08:00",
  "notification_style": "motivational"
}
```

## Quick Start

### Installation

```bash
# Clone and enter development environment
git clone https://github.com/yourusername/memento-mori
cd memento-mori
direnv allow  # or: devenv shell

# Initialize Python project
uv init
uv add rich

# Run the tool
python3 src/memento_mori/cli.py
```

### Usage

```bash
# View your life statistics
memento-mori

# With full grid visualization
memento-mori --grid

# Edit configuration
memento-mori --config

# Test notification format
memento-mori --notify
```

### Fish Shell Abbreviation

```bash
# Add to Fish config
abbr mm memento-mori
```

## Example Output

```
╔═══════════════════════════════════════════════════════════╗
║              ⏳ MEMENTO MORI - THE REAL TIME             ║
║        Remember you will die. Make the time count.        ║
╠═══════════════════════════════════════════════════════════╣
║                                                           ║
║  YOUR TOTAL LIFE                                          ║
║  ████████████████░░░░░░░░░░░  52.3%                      ║
║  Weeks lived: 2,178  |  Weeks left: 1,982                ║
║                                                           ║
║  YOUR TRULY FREE TIME (sleep/work removed)                ║
║  ████████████████████░░░░░  68.1%                        ║
║  Free weeks used: 682  |  Free weeks left: 318           ║
║                                                           ║
╠═══════════════════════════════════════════════════════════╣
║  💼 WORKING LIFE                                          ║
║    Years until retirement: 25 (1,300 weeks)               ║
║    Vacation weeks remaining: ~75 weeks                    ║
║                                                           ║
║  👨‍👩‍👧 FAMILY TIME                                            ║
║    Days left with parents: ~240 days (visiting 10x/year) ║
║    90% of lifetime with them: Already spent              ║
║                                                           ║
║  🌅 WEEKENDS LEFT                                         ║
║    Saturday/Sunday freedom: ~1,300 weekends              ║
╚═══════════════════════════════════════════════════════════╝

"You may have 30 years left, but you only have 300 days
 left with your parents. Book the visit."
```

## Architecture

- **Language**: Python 3.13 with uv package manager
- **UI**: Rich library for terminal rendering
- **Notifications**: GNOME `notify-send`
- **Automation**: systemd user timers
- **Development**: DevEnv with quality gates (Lizard, JSCPD, Gitleaks)
- **AI Integration**: Claude Code and Cursor AI configurations included

## Quality Standards

This project uses enterprise-grade quality gates:

- **Complexity**: CCN < 10 per function (Lizard)
- **Duplication**: < 5% threshold (JSCPD)
- **Security**: Zero secrets (Gitleaks)
- **Formatting**: Black + Ruff for Python
- **Testing**: 75%+ coverage target
- **Commits**: Conventional Commits format

## Development

```bash
# Enter development environment
devenv shell

# Run quality checks
quality-report
quality-check

# Run tests
pytest

# Format code
ruff format .

# Check complexity
lizard src/
```

## Philosophy

This tool is inspired by:

- **Stoic philosophy**: Memento Mori as a call to action, not despair
- **Wait But Why**: "The Tail End" - visualizing limited time with loved ones
- **See Your Folks calculator**: Making parent mortality tangible
- **Life in Weeks**: Tim Urban's famous grid visualization

The goal is not to create anxiety, but to create **clarity and urgency** around what matters most.

## License

MIT

## Credits

Built with:

- [Rich](https://github.com/Textualize/rich) - Beautiful terminal UI
- [DevEnv](https://devenv.sh/) - Development environment
- AI Quality DevEnv Template - Enterprise development standards

Inspired by:

- Tim Urban's "The Tail End" (Wait But Why)
- "See Your Folks" mortality calculator
- Stoic Memento Mori tradition
- Various life-in-weeks visualizations

---

**Remember: You have less time than you think. Make it count.**
