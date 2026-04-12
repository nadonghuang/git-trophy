"""
git-trophy 🏆 — Git 仓库分析器
解析 git log 数据，提取成就相关的统计信息
"""

import os
import re
import subprocess
from datetime import datetime
from collections import defaultdict


class GitAnalyzer:
    """Git 仓库分析器"""

    def __init__(self, repo_path="."):
        self.repo_path = os.path.abspath(repo_path)
        self._verify_repo()

    def _verify_repo(self):
        """验证是否为有效的 git 仓库"""
        try:
            result = subprocess.run(
                ["git", "rev-parse", "--is-inside-work-tree"],
                cwd=self.repo_path,
                capture_output=True, text=True, timeout=10
            )
            if result.returncode != 0:
                raise ValueError(f"Not a git repository: {self.repo_path}")
        except FileNotFoundError:
            raise RuntimeError("git is not installed or not in PATH")

    def _run_git(self, args):
        """运行 git 命令并返回输出"""
        result = subprocess.run(
            ["git"] + args,
            cwd=self.repo_path,
            capture_output=True, text=True, timeout=30
        )
        return result.stdout.strip()

    def analyze(self):
        """分析仓库，返回统计字典"""
        stats = {
            "total_commits": 0,
            "night_commits": [],
            "early_commits": [],
            "weekend_commits": 0,
            "file_extensions": set(),
            "max_streak": 0,
            "max_lines_changed": 0,
            "hour_distribution": set(),
            "co_authors": set(),
            "max_message_length": 0,
            "fix_commits": 0,
            "feature_commits": 0,
            "weekday_top": None,
            "new_year_commits": 0,
            "commit_dates": [],
            "weekday_counts": defaultdict(int),
        }

        self._analyze_commits(stats)
        self._analyze_streak(stats)
        self._analyze_files(stats)

        return stats

    def _analyze_commits(self, stats):
        """分析提交历史"""
        # 获取格式化的 git log
        # 格式: timestamp|message|insertions|deletions
        log_format = "%ct||%s||%b---COMMIT_END---"
        output = self._run_git([
            "log", "--all", "--format=" + log_format,
            "--numstat", "--no-merges"
        ])

        if not output:
            return

        # 获取每个 commit 的统计信息
        numstat_output = self._run_git([
            "log", "--all", "--format=---COMMIT_SEP---",
            "--numstat", "--no-merges"
        ])

        commit_sections = numstat_output.split("---COMMIT_SEP---")
        lines_changed_per_commit = []

        for section in commit_sections[1:]:  # 跳过第一个空段
            total_changed = 0
            for line in section.strip().split("\n"):
                parts = line.split("\t")
                if len(parts) == 3:
                    try:
                        ins = int(parts[0]) if parts[0] != "-" else 0
                        dels = int(parts[1]) if parts[1] != "-" else 0
                        total_changed += ins + dels
                    except ValueError:
                        pass
            if total_changed > 0:
                lines_changed_per_commit.append(total_changed)

        # 解析日志输出
        commits = output.split("---COMMIT_END---")
        line_idx = 0

        for commit in commits:
            commit = commit.strip()
            if not commit:
                continue

            # 分割时间戳和消息
            parts = commit.split("||")
            if len(parts) < 2:
                continue

            try:
                timestamp = int(parts[0])
            except (ValueError, IndexError):
                continue

            message = parts[1] if len(parts) > 1 else ""
            body = parts[2] if len(parts) > 2 else ""

            dt = datetime.fromtimestamp(timestamp)
            stats["total_commits"] += 1

            # 夜猫子：0-5 点
            if 0 <= dt.hour < 5:
                stats["night_commits"].append(dt)

            # 早起鸟：5-8 点
            if 5 <= dt.hour < 8:
                stats["early_commits"].append(dt)

            # 周末提交
            if dt.weekday() >= 5:
                stats["weekend_commits"] += 1

            # 小时分布
            stats["hour_distribution"].add(dt.hour)

            # 星期几分布
            stats["weekday_counts"][dt.weekday()] += 1

            # 新年提交
            if dt.month == 1 and dt.day == 1:
                stats["new_year_commits"] += 1

            # 提交日期
            stats["commit_dates"].append(dt.strftime("%Y-%m-%d"))

            # 消息长度
            msg_len = len(message)
            if msg_len > stats["max_message_length"]:
                stats["max_message_length"] = msg_len

            # Fix/Feature 提交计数
            msg_lower = message.lower()
            if any(w in msg_lower for w in ["fix", "bug", "patch", "hotfix"]):
                stats["fix_commits"] += 1
            if any(w in msg_lower for w in ["feat", "feature", "add", "implement"]):
                stats["feature_commits"] += 1

            # Co-authors
            co_authors = re.findall(r"Co-authored-by:\s*(.+?)<", body)
            for author in co_authors:
                stats["co_authors"].add(author.strip())

            # 最大修改行数
            if line_idx < len(lines_changed_per_commit):
                lc = lines_changed_per_commit[line_idx]
                if lc > stats["max_lines_changed"]:
                    stats["max_lines_changed"] = lc
            line_idx += 1

        # 计算最多提交的星期几
        if stats["weekday_counts"]:
            stats["weekday_top"] = max(
                stats["weekday_counts"],
                key=stats["weekday_counts"].get
            )

    def _analyze_streak(self, stats):
        """计算最长连续提交天数"""
        dates = sorted(set(stats["commit_dates"]))
        if not dates:
            return

        max_streak = 1
        current_streak = 1

        for i in range(1, len(dates)):
            prev = datetime.strptime(dates[i - 1], "%Y-%m-%d")
            curr = datetime.strptime(dates[i], "%Y-%m-%d")
            diff = (curr - prev).days

            if diff == 1:
                current_streak += 1
                max_streak = max(max_streak, current_streak)
            elif diff > 1:
                current_streak = 1

        stats["max_streak"] = max_streak

    def _analyze_files(self, stats):
        """分析涉及的文件类型"""
        output = self._run_git([
            "log", "--all", "--name-only", "--format=", "--no-merges"
        ])

        for line in output.split("\n"):
            line = line.strip()
            if line and "." in line:
                ext = os.path.splitext(line)[1].lower()
                if ext:
                    stats["file_extensions"].add(ext)

    def get_repo_name(self):
        """获取仓库名称"""
        # 尝试从 remote 获取
        remote_url = self._run_git(["config", "--get", "remote.origin.url"])
        if remote_url:
            # 提取最后一段，去掉 .git
            name = remote_url.split("/")[-1]
            if name.endswith(".git"):
                name = name[:-4]
            return name
        # 回退到目录名
        return os.path.basename(self.repo_path)
