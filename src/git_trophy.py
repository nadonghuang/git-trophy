"""
git-trophy 🏆 — 用 gamification 的方式看待你的 Git 贡献
分析 git 历史，解锁成就奖杯，展示漂亮的终端报告
"""

__version__ = "1.0.0"

from .analyzer import GitAnalyzer
from .trophies import ALL_CHECKS
from .renderer import Renderer


def run(repo_path=".", use_color=None, show_locked=True):
    """
    主入口：分析仓库并渲染结果

    Args:
        repo_path: Git 仓库路径
        use_color: 是否使用颜色 (None=自动检测)
        show_locked: 是否显示未解锁的奖杯

    Returns:
        (unlocked_trophies, locked_trophies, stats)
    """
    # 分析仓库
    analyzer = GitAnalyzer(repo_path)
    stats = analyzer.analyze()
    repo_name = analyzer.get_repo_name()

    # 检查所有成就
    unlocked = []
    locked = []

    for check_fn in ALL_CHECKS:
        earned, trophy = check_fn(stats)
        if earned:
            unlocked.append((trophy, check_fn.__doc__))
        elif show_locked:
            locked.append(trophy)

    # 按稀有度排序
    rarity_order = {"common": 0, "uncommon": 1, "rare": 2, "epic": 3, "legendary": 4}
    unlocked.sort(key=lambda x: rarity_order.get(x[0].rarity, 5))
    locked.sort(key=lambda x: rarity_order.get(x.rarity, 5))

    # 渲染报告
    renderer = Renderer(use_color=use_color)
    report = renderer.render_full_report(repo_name, stats, unlocked, locked)
    print(report)

    return unlocked, locked, stats


def main():
    """CLI 入口"""
    import argparse

    parser = argparse.ArgumentParser(
        prog="git-trophy",
        description="🏆 Analyze your git repo and earn achievement trophies!"
    )
    parser.add_argument(
        "path",
        nargs="?",
        default=".",
        help="Path to git repository (default: current directory)"
    )
    parser.add_argument(
        "--no-color",
        action="store_true",
        help="Disable colored output"
    )
    parser.add_argument(
        "--hide-locked",
        action="store_true",
        help="Hide locked/unearned trophies"
    )
    parser.add_argument(
        "--json",
        action="store_true",
        help="Output results as JSON"
    )
    parser.add_argument(
        "--version",
        action="version",
        version=f"%(prog)s {__version__}"
    )

    args = parser.parse_args()

    if args.json:
        # JSON 输出模式
        import json

        analyzer = GitAnalyzer(args.path)
        stats = analyzer.analyze()

        # 序列化 stats（处理 set/datetime 等不可序列化类型）
        serializable = {}
        for k, v in stats.items():
            if isinstance(v, set):
                serializable[k] = sorted(list(v))
            elif isinstance(v, dict):
                serializable[k] = dict(v)
            elif isinstance(v, list) and v and hasattr(v[0], "isoformat"):
                serializable[k] = [x.isoformat() for x in v]
            else:
                serializable[k] = v

        # 计算成就
        result_trophies = []
        for check_fn in ALL_CHECKS:
            earned, trophy = check_fn(stats)
            result_trophies.append({
                "id": trophy.trophy_id,
                "name": trophy.name,
                "description": trophy.description,
                "icon": trophy.icon,
                "rarity": trophy.rarity,
                "earned": earned,
            })

        output = {
            "repo": analyzer.get_repo_name(),
            "stats": serializable,
            "trophies": result_trophies,
            "version": __version__,
        }
        print(json.dumps(output, indent=2, ensure_ascii=False))
    else:
        run(
            repo_path=args.path,
            use_color=not args.no_color,
            show_locked=not args.hide_locked,
        )


if __name__ == "__main__":
    main()
