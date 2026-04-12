"""
git-trophy 🏆 — 终端渲染器
漂亮的终端输出，包括奖杯柜、进度条等
"""

import os
import sys
from datetime import datetime

from .trophies import RARITY_COLORS, RARITY_LABELS, Trophy

# ANSI 颜色码
RESET = "\033[0m"
BOLD = "\033[1m"
DIM = "\033[2m"
ITALIC = "\033[3m"
RED = "\033[31m"
GREEN = "\033[32m"
YELLOW = "\033[33m"
BLUE = "\033[34m"
MAGENTA = "\033[35m"
CYAN = "\033[36m"
WHITE = "\033[37m"
GRAY = "\033[90m"

# Box-drawing 字符
TL = "╔"
TR = "╗"
BL = "╚"
BR = "╝"
H = "═"
V = "║"
LT = "╠"
RT = "╣"
TT = "╦"
TB = "╩"
X = "╬"

# Unicode 方块
BLOCK_FULL = "█"
BLOCK_LIGHT = "░"


def supports_color():
    """检测终端是否支持颜色"""
    if os.getenv("NO_COLOR"):
        return False
    if not hasattr(sys.stdout, "isatty"):
        return False
    return sys.stdout.isatty() or os.getenv("FORCE_COLOR")


def colorize(text, color, use_color=True):
    """给文本上色"""
    if not use_color:
        return text
    return f"{color}{text}{RESET}"


def get_terminal_width():
    """获取终端宽度"""
    try:
        return os.get_terminal_size().columns
    except OSError:
        return 80


class Renderer:
    """终端渲染器"""

    def __init__(self, use_color=None):
        self.use_color = use_color if use_color is not None else supports_color()
        self.width = min(get_terminal_width(), 80)

    def _c(self, text, color):
        return colorize(text, color, self.use_color)

    def render_header(self, repo_name):
        """渲染头部横幅"""
        lines = []
        title = f"🏆 git-trophy — {repo_name}"
        lines.append(self._c(TL + H * (self.width - 2) + TR, CYAN))
        lines.append(self._c(V, CYAN) + self._c(title.center(self.width - 2), BOLD + YELLOW) + self._c(V, CYAN))
        lines.append(self._c(LT + H * (self.width - 2) + RT, CYAN))
        return "\n".join(lines)

    def render_stats_summary(self, stats):
        """渲染统计摘要"""
        lines = []

        # 统计信息行
        total = stats["total_commits"]
        streak = stats["max_streak"]
        exts = len(stats["file_extensions"])
        hours = len(stats["hour_distribution"])

        row1 = (
            f"  📊 Total Commits: {self._c(str(total), BOLD + GREEN)}"
            f"  │  🔥 Best Streak: {self._c(str(streak) + ' days', BOLD + YELLOW)}"
        )
        row2 = (
            f"  🌐 File Types: {self._c(str(exts), BOLD + BLUE)}"
            f"  │  ⏰ Active Hours: {self._c(str(hours) + '/24', BOLD + MAGENTA)}"
        )

        lines.append(self._c(V, CYAN) + " " * (self.width - 2) + self._c(V, CYAN))
        lines.append(self._c(V, CYAN) + row1.ljust(self.width - 2) + self._c(V, CYAN))
        lines.append(self._c(V, CYAN) + row2.ljust(self.width - 2) + self._c(V, CYAN))
        lines.append(self._c(LT + H * (self.width - 2) + RT, CYAN))

        return "\n".join(lines)

    def render_weekday_chart(self, stats):
        """渲染星期几活跃度图表"""
        lines = []
        lines.append(self._c(V, CYAN) + self._c("  📅 Weekly Activity", BOLD).ljust(self.width - 2) + self._c(V, CYAN))

        weekday_names = ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"]
        max_count = max(stats["weekday_counts"].values()) if stats["weekday_counts"] else 1

        for i, name in enumerate(weekday_names):
            count = stats["weekday_counts"].get(i, 0)
            bar_len = int((count / max(max_count, 1)) * 25)
            bar = BLOCK_FULL * bar_len + BLOCK_LIGHT * (25 - bar_len)

            line = f"  {name} {self._c(bar, GREEN)} {self._c(str(count), DIM)}"
            lines.append(self._c(V, CYAN) + line.ljust(self.width - 2) + self._c(V, CYAN))

        lines.append(self._c(LT + H * (self.width - 2) + RT, CYAN))
        return "\n".join(lines)

    def render_trophy(self, trophy, index, unlocked=True):
        """渲染单个奖杯"""
        rarity_color = RARITY_COLORS.get(trophy.rarity, WHITE)
        rarity_label = RARITY_LABELS.get(trophy.rarity, "?")

        if unlocked:
            status_icon = "✅"
            name_str = self._c(trophy.name, BOLD + rarity_color)
            desc_str = self._c(trophy.description, DIM)
        else:
            status_icon = "🔒"
            name_str = self._c(trophy.name, GRAY)
            desc_str = self._c(trophy.description, GRAY)

        rarity_str = self._c(f"[{rarity_label}]", rarity_color)

        line = f"  {trophy.icon} {status_icon} {name_str} {rarity_str}"
        desc_line = f"     {desc_str}"

        lines = []
        lines.append(self._c(V, CYAN) + line.ljust(self.width - 2) + self._c(V, CYAN))
        lines.append(self._c(V, CYAN) + desc_line.ljust(self.width - 2) + self._c(V, CYAN))

        return "\n".join(lines)

    def render_trophy_case(self, unlocked, locked):
        """渲染奖杯柜"""
        lines = []

        total = len(unlocked) + len(locked)
        unlock_pct = int((len(unlocked) / max(total, 1)) * 100)

        header = f"  🏆 Trophy Case — {len(unlocked)}/{total} Unlocked ({unlock_pct}%)"
        lines.append(self._c(V, CYAN) + self._c(header, BOLD + YELLOW).ljust(self.width - 2) + self._c(V, CYAN))
        lines.append(self._c(V, CYAN) + " " * (self.width - 2) + self._c(V, CYAN))

        # 已解锁奖杯
        if unlocked:
            lines.append(self._c(V, CYAN) + self._c("  ✨ Earned:", GREEN).ljust(self.width - 2) + self._c(V, CYAN))
            lines.append(self._c(V, CYAN) + " " * (self.width - 2) + self._c(V, CYAN))
            for i, (trophy, _) in enumerate(unlocked):
                lines.append(self.render_trophy(trophy, i, unlocked=True))
                lines.append(self._c(V, CYAN) + " " * (self.width - 2) + self._c(V, CYAN))

        # 未解锁奖杯（仅显示提示）
        if locked:
            lines.append(self._c(V, CYAN) + self._c("  🔒 Locked:", GRAY).ljust(self.width - 2) + self._c(V, CYAN))
            lines.append(self._c(V, CYAN) + " " * (self.width - 2) + self._c(V, CYAN))
            for i, trophy in enumerate(locked):
                lines.append(self.render_trophy(trophy, i, unlocked=False))
                lines.append(self._c(V, CYAN) + " " * (self.width - 2) + self._c(V, CYAN))

        return "\n".join(lines)

    def render_hour_chart(self, stats):
        """渲染 24 小时活跃度热力图"""
        lines = []
        lines.append(self._c(V, CYAN) + self._c("  ⏰ Hourly Heatmap", BOLD).ljust(self.width - 2) + self._c(V, CYAN))

        hours = list(range(24))
        bar = ""
        for h in hours:
            if h in stats["hour_distribution"]:
                bar += self._c(BLOCK_FULL, GREEN)
            else:
                bar += self._c(BLOCK_LIGHT, GRAY)

        # 标尺
        ruler = ""
        for h in range(24):
            if h % 6 == 0:
                ruler += f"{h:2d}"
            elif h % 3 == 0:
                ruler += " ·"
            else:
                ruler += "  "

        lines.append(self._c(V, CYAN) + f"  {bar}".ljust(self.width - 2) + self._c(V, CYAN))
        lines.append(self._c(V, CYAN) + f"  {ruler}".ljust(self.width - 2) + self._c(V, CYAN))
        lines.append(self._c(LT + H * (self.width - 2) + RT, CYAN))

        return "\n".join(lines)

    def render_footer(self):
        """渲染页脚"""
        lines = []
        lines.append(self._c(V, CYAN) + " " * (self.width - 2) + self._c(V, CYAN))
        footer = "  Keep coding, keep earning! 🚀"
        lines.append(self._c(V, CYAN) + self._c(footer, DIM + ITALIC).ljust(self.width - 2) + self._c(V, CYAN))
        lines.append(self._c(BL + H * (self.width - 2) + BR, CYAN))
        return "\n".join(lines)

    def render_full_report(self, repo_name, stats, unlocked, locked):
        """渲染完整报告"""
        sections = [
            self.render_header(repo_name),
            self.render_stats_summary(stats),
            self.render_weekday_chart(stats),
            self.render_hour_chart(stats),
            self.render_trophy_case(unlocked, locked),
            self.render_footer(),
        ]
        return "\n".join(sections)
