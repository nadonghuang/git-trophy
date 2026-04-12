"""
git-trophy 🏆 — 成就定义模块
每个成就包含：id, 名称, 描述, 图标, 检查函数
"""

from dataclasses import dataclass


@dataclass
class Trophy:
    """奖杯定义"""
    trophy_id: str
    name: str
    description: str
    icon: str
    rarity: str  # common, uncommon, rare, epic, legendary

    def __str__(self):
        return f"{self.icon} {self.name}"


# 稀有度颜色映射
RARITY_COLORS = {
    "common": "\033[37m",       # 白色
    "uncommon": "\033[32m",     # 绿色
    "rare": "\033[34m",         # 蓝色
    "epic": "\033[35m",         # 紫色
    "legendary": "\033[33m",    # 金色
}

RARITY_LABELS = {
    "common": "普通",
    "uncommon": "稀有",
    "rare": "精良",
    "epic": "史诗",
    "legendary": "传说",
}


def check_first_commit(stats):
    """🎯 初次提交 — 完成第一次 commit"""
    return stats["total_commits"] >= 1, Trophy(
        "first_commit", "First Commit", "Make your first commit",
        "🎯", "common"
    )


def check_hundred_commits(stats):
    """💯 百次贡献 — 累计 100 次提交"""
    return stats["total_commits"] >= 100, Trophy(
        "centurion", "Centurion", "Reach 100 total commits",
        "💯", "uncommon"
    )


def check_thousand_commits(stats):
    """🔥 千次贡献 — 累计 1000 次提交"""
    return stats["total_commits"] >= 1000, Trophy(
        "millennial", "Millennial", "Reach 1,000 total commits",
        "🔥", "epic"
    )


def check_night_owl(stats):
    """🦉 夜猫子 — 在凌晨 0-5 点提交"""
    return len(stats["night_commits"]) >= 10, Trophy(
        "night_owl", "Night Owl", "Commit 10+ times between midnight and 5 AM",
        "🦉", "uncommon"
    )


def check_early_bird(stats):
    """🌅 早起鸟 — 在 5-8 点提交"""
    return len(stats["early_commits"]) >= 10, Trophy(
        "early_bird", "Early Bird", "Commit 10+ times between 5 AM and 8 AM",
        "🌅", "uncommon"
    )


def check_weekend_warrior(stats):
    """⚔️ 周末战士 — 在周末提交超过 20 次"""
    return stats["weekend_commits"] >= 20, Trophy(
        "weekend_warrior", "Weekend Warrior", "Commit 20+ times on weekends",
        "⚔️", "uncommon"
    )


def check_polyglot(stats):
    """🌐 多语言大师 — 涉及 5+ 种文件类型"""
    return len(stats["file_extensions"]) >= 5, Trophy(
        "polyglot", "Polyglot", "Touch 5+ different file types",
        "🌐", "rare"
    )


def check_polyglot_10(stats):
    """🎓 语言大师 — 涉及 10+ 种文件类型"""
    return len(stats["file_extensions"]) >= 10, Trophy(
        "polyglot_pro", "Polyglot Pro", "Touch 10+ different file types",
        "🎓", "epic"
    )


def check_streak_7(stats):
    """🔥 七日之焰 — 连续 7 天提交"""
    return stats["max_streak"] >= 7, Trophy(
        "streak_7", "Week On Fire", "Maintain a 7-day commit streak",
        "🔥", "rare"
    )


def check_streak_30(stats):
    """⚡ 月度之焰 — 连续 30 天提交"""
    return stats["max_streak"] >= 30, Trophy(
        "streak_30", "Monthly Blaze", "Maintain a 30-day commit streak",
        "⚡", "epic"
    )


def check_streak_100(stats):
    """💎 百日传奇 — 连续 100 天提交"""
    return stats["max_streak"] >= 100, Trophy(
        "streak_100", "Legendary Streak", "Maintain a 100-day commit streak",
        "💎", "legendary"
    )


def check_big_commit(stats):
    """🐘 大象提交 — 单次提交修改 500+ 行"""
    return stats["max_lines_changed"] >= 500, Trophy(
        "elephant", "Elephant", "Change 500+ lines in a single commit",
        "🐘", "uncommon"
    )


def check_mega_commit(stats):
    """🏔️ 超级提交 — 单次提交修改 2000+ 行"""
    return stats["max_lines_changed"] >= 2000, Trophy(
        "mountain", "Mountain Mover", "Change 2,000+ lines in a single commit",
        "🏔️", "rare"
    )


def check_variety_hour(stats):
    """🎪 全天候 — 在 12+ 个不同小时段提交过"""
    return len(stats["hour_distribution"]) >= 12, Trophy(
        "all_hours", "Around The Clock", "Commit during 12+ different hours of the day",
        "🎪", "uncommon"
    )


def check_insomniac(stats):
    """🌙 失眠者 — 在每个小时段 (0-23) 都提交过"""
    return len(stats["hour_distribution"]) >= 24, Trophy(
        "insomniac", "Insomniac", "Commit during every hour of the day (0-23)",
        "🌙", "legendary"
    )


def check_many_authors(stats):
    """👥 社交蝴蝶 — 与 3+ 个不同的合作者协作"""
    return len(stats["co_authors"]) >= 3, Trophy(
        "social", "Social Butterfly", "Co-author commits with 3+ different people",
        "👥", "rare"
    )


def check_long_message(stats):
    """📝 长篇大论 — 写过 200+ 字符的 commit message"""
    return stats["max_message_length"] >= 200, Trophy(
        "storyteller", "Storyteller", "Write a commit message with 200+ characters",
        "📝", "uncommon"
    )


def check_concise(stats):
    """✂️ 简洁大师 — 所有 commit message 都少于 50 字符 (至少 10 次提交)"""
    return (stats["total_commits"] >= 10 and
            stats["max_message_length"] <= 50), Trophy(
        "concise", "Straight To The Point",
        "Keep all commit messages under 50 characters (10+ commits)",
        "✂️", "rare"
    )


def check_fixer(stats):
    """🐛 修复大师 — 20+ 次 fix 相关提交"""
    return stats["fix_commits"] >= 20, Trophy(
        "fixer", "Bug Squasher", "Make 20+ fix-related commits",
        "🐛", "uncommon"
    )


def check_feature(stats):
    """✨ 功能工厂 — 20+ 次 feature 相关提交"""
    return stats["feature_commits"] >= 20, Trophy(
        "feature_factory", "Feature Factory", "Make 20+ feature-related commits",
        "✨", "uncommon"
    )


def check_monday(stats):
    """😩 周一战士 — 周一提交最多"""
    return (stats["weekday_top"] is not None and
            stats["weekday_top"] == 0), Trophy(
        "monday", "Monday Warrior", "Monday is your most productive day",
        "😩", "uncommon"
    )


def check_friday(stats):
    """🎉 TGIF — 周五提交占比最高"""
    return (stats["weekday_top"] is not None and
            stats["weekday_top"] == 4), Trophy(
        "tgif", "Thank Git It's Friday", "Friday is your most productive day",
        "🎉", "uncommon"
    )


def check_new_years(stats):
    """🎆 新年代码 — 在 1 月 1 日提交过"""
    return stats["new_year_commits"] > 0, Trophy(
        "new_year", "New Year Coder", "Commit on January 1st",
        "🎆", "rare"
    )


# 所有检查函数列表，按稀有度排列
ALL_CHECKS = [
    # Common
    check_first_commit,
    # Uncommon
    check_hundred_commits,
    check_night_owl,
    check_early_bird,
    check_weekend_warrior,
    check_big_commit,
    check_long_message,
    check_fixer,
    check_feature,
    check_monday,
    check_friday,
    check_variety_hour,
    # Rare
    check_polyglot,
    check_streak_7,
    check_mega_commit,
    check_many_authors,
    check_concise,
    check_new_years,
    # Epic
    check_thousand_commits,
    check_polyglot_10,
    check_streak_30,
    # Legendary
    check_streak_100,
    check_insomniac,
]
