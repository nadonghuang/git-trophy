#!/usr/bin/env python3
"""
示例：使用 git-trophy 作为 Python 库来分析多个仓库
Example: Use git-trophy as a Python library to analyze multiple repos
"""

import os
import sys

# 将项目根目录加入路径
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.git_trophy import run
from src.analyzer import GitAnalyzer
from src.trophies import ALL_CHECKS


def analyze_multiple(repo_paths):
    """分析多个仓库并比较成就"""
    results = {}

    for path in repo_paths:
        try:
            analyzer = GitAnalyzer(path)
            stats = analyzer.analyze()
            repo_name = analyzer.get_repo_name()

            earned_count = 0
            for check_fn in ALL_CHECKS:
                earned, _ = check_fn(stats)
                if earned:
                    earned_count += 1

            results[repo_name] = {
                "commits": stats["total_commits"],
                "trophies": earned_count,
                "streak": stats["max_streak"],
            }
            print(f"  ✅ {repo_name}: {stats['total_commits']} commits, "
                  f"{earned_count} trophies, streak: {stats['max_streak']} days")
        except Exception as e:
            print(f"  ❌ {path}: {e}")

    if results:
        # 找出最佳仓库
        best = max(results.items(), key=lambda x: x[1]["trophies"])
        print(f"\n  🏆 Best repo: {best[0]} with {best[1]['trophies']} trophies!")


if __name__ == "__main__":
    # 默认分析当前目录的兄弟仓库
    base = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    parent = os.path.dirname(base)

    # 收集所有 git 仓库
    repos = []
    for name in sorted(os.listdir(parent)):
        path = os.path.join(parent, name)
        if os.path.isdir(os.path.join(path, ".git")):
            repos.append(path)

    if repos:
        print(f"🔍 Scanning {len(repos)} repositories...\n")
        analyze_multiple(repos)
    else:
        print("No git repos found. Run: git-trophy <path-to-repo>")
