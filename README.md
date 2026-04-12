<p align="center">
  <img src="https://img.shields.io/badge/Python-3.8+-3776AB?style=for-the-badge&logo=python&logoColor=white" alt="Python"/>
  <img src="https://img.shields.io/badge/License-MIT-green?style=for-the-badge" alt="License"/>
  <img src="https://img.shields.io/badge/Zero_Deps-✅-success?style=for-the-badge" alt="Zero Deps"/>
  <img src="https://img.shields.io/badge/Trophies-23_🏆-yellow?style=for-the-badge" alt="Trophies"/>
</p>

<h1 align="center">🏆 git-trophy</h1>

<p align="center">
  <strong>Analyze your git repo and earn achievement trophies — gamify your contributions!</strong>
</p>

<p align="center">
  <a href="#-features">Features</a> •
  <a href="#-installation">Install</a> •
  <a href="#-usage">Usage</a> •
  <a href="#-all-trophies">Trophies</a> •
  <a href="#-license">License</a>
</p>

---

## ✨ What It Does

**git-trophy** scans your git commit history and awards you trophies based on your coding habits — like Xbox achievements, but for your codebase.

```
╔══════════════════════════════════════════════════════════════════╗
║                    🏆 git-trophy — my-project                   ║
╠══════════════════════════════════════════════════════════════════╣
║  📊 Total Commits: 342  │  🔥 Best Streak: 14 days              ║
║  🌐 File Types: 8       │  ⏰ Active Hours: 18/24               ║
╠══════════════════════════════════════════════════════════════════╣
║  📅 Weekly Activity                                               ║
║  Mon ████████████████████████████ 52                              ║
║  Tue █████████████████████████ 44                                 ║
║  ...                                                              ║
╠══════════════════════════════════════════════════════════════════╣
║  🏆 Trophy Case — 9/23 Unlocked (39%)                            ║
║                                                                   ║
║  ✨ Earned:                                                       ║
║  🎯 ✅ First Commit [普通]                                         ║
║  🦉 ✅ Night Owl [稀有]                                            ║
║  🌐 ✅ Polyglot [精良]                                            ║
║  ...                                                              ║
╚══════════════════════════════════════════════════════════════════╝
```

## ✨ Features

- 🏆 **23 unique trophies** across 5 rarity tiers (Common → Legendary)
- 📊 **Beautiful terminal UI** with box-drawing characters and color-coded output
- 📅 **Weekly activity chart** — visualize your most productive days
- ⏰ **Hourly heatmap** — see when you code (night owl? early bird?)
- 🔥 **Streak tracking** — longest consecutive commit streaks
- 📝 **JSON output** for scripting, CI integration, and custom dashboards
- 🔌 **Python API** — use as a library in your own tools
- ⚡ **Zero dependencies** — pure Python 3.8+ standard library only
- 🎮 **Gamification** — earn achievements like "Night Owl", "Polyglot", "Insomniac"

## 📦 Installation

```bash
# Clone and install
git clone https://github.com/nadonghuang/git-trophy.git
cd git-trophy
pip install -e .
```

Or run directly without installing:

```bash
python3 -m src.git_trophy /path/to/your/repo
```

## 🚀 Usage

### Basic — analyze current directory

```bash
cd your-project
git-trophy
```

### Analyze a specific repo

```bash
git-trophy /path/to/repo
```

### JSON output for scripts

```bash
git-trophy /path/to/repo --json | jq '.trophies[] | select(.earned)'
```

### Hide locked trophies

```bash
git-trophy --hide-locked
```

### No color mode

```bash
git-trophy --no-color
```

### Use as Python library

```python
from src.git_trophy import run
from src.analyzer import GitAnalyzer
from src.trophies import ALL_CHECKS

# Full interactive report
run("/path/to/repo")

# Or just get the data
analyzer = GitAnalyzer("/path/to/repo")
stats = analyzer.analyze()

for check_fn in ALL_CHECKS:
    earned, trophy = check_fn(stats)
    if earned:
        print(f"Unlocked: {trophy.icon} {trophy.name}")
```

## 🏅 All Trophies

### Common
| Trophy | Icon | How to Earn |
|--------|------|-------------|
| First Commit | 🎯 | Make your first commit |

### Uncommon
| Trophy | Icon | How to Earn |
|--------|------|-------------|
| Centurion | 💯 | Reach 100 total commits |
| Night Owl | 🦉 | Commit 10+ times between midnight and 5 AM |
| Early Bird | 🌅 | Commit 10+ times between 5 AM and 8 AM |
| Weekend Warrior | ⚔️ | Commit 20+ times on weekends |
| Elephant | 🐘 | Change 500+ lines in a single commit |
| Storyteller | 📝 | Write a commit message with 200+ characters |
| Bug Squasher | 🐛 | Make 20+ fix-related commits |
| Feature Factory | ✨ | Make 20+ feature-related commits |
| Monday Warrior | 😩 | Monday is your most productive day |
| TGIF | 🎉 | Friday is your most productive day |
| Around The Clock | 🎪 | Commit during 12+ different hours |

### Rare
| Trophy | Icon | How to Earn |
|--------|------|-------------|
| Polyglot | 🌐 | Touch 5+ different file types |
| Week On Fire | 🔥 | Maintain a 7-day commit streak |
| Mountain Mover | 🏔️ | Change 2,000+ lines in a single commit |
| Social Butterfly | 👥 | Co-author commits with 3+ different people |
| Straight To The Point | ✂️ | Keep all messages under 50 chars (10+ commits) |
| New Year Coder | 🎆 | Commit on January 1st |

### Epic
| Trophy | Icon | How to Earn |
|--------|------|-------------|
| Millennial | 🔥 | Reach 1,000 total commits |
| Polyglot Pro | 🎓 | Touch 10+ different file types |
| Monthly Blaze | ⚡ | Maintain a 30-day commit streak |

### Legendary
| Trophy | Icon | How to Earn |
|--------|------|-------------|
| Legendary Streak | 💎 | Maintain a 100-day commit streak |
| Insomniac | 🌙 | Commit during every hour of the day (0-23) |

## 📁 Project Structure

```
git-trophy/
├── src/
│   ├── git_trophy.py    # Main entry point & CLI
│   ├── analyzer.py      # Git repository analyzer
│   ├── trophies.py      # Trophy definitions & check functions
│   ├── renderer.py      # Terminal UI renderer
│   └── __init__.py
├── bin/
│   └── git-trophy       # CLI executable
├── examples/
│   └── multi_repo.py    # Multi-repo analysis example
├── pyproject.toml
├── LICENSE
└── README.md
```

## 🔧 Tech Stack

| Component | Technology |
|-----------|-----------|
| Language | Python 3.8+ |
| Dependencies | Zero (stdlib only) |
| Git Integration | subprocess + git CLI |
| Terminal UI | ANSI escape codes + Unicode box-drawing |
| Package Manager | pip / pyproject.toml |

## 🤝 Contributing

Found a bug? Have an idea for a new trophy?

1. Fork the repo
2. Create your feature branch (`git checkout -b feature/amazing-trophy`)
3. Add your trophy in `src/trophies.py`
4. Commit your changes (`git commit -m '🏆 Add amazing trophy'`)
5. Push to the branch (`git push origin feature/amazing-trophy`)
6. Open a Pull Request

## 📄 License

MIT — see [LICENSE](LICENSE) for details.

---

<p align="center">
  Made with ⚡ by <a href="https://github.com/nadonghuang">nadonghuang</a>
  <br/>
  <sub>If you find this fun, please give it a ⭐!</sub>
</p>
