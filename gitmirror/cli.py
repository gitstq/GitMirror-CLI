#!/usr/bin/env python3
"""
GitMirror CLI - 命令行接口
"""

import sys
import argparse
from typing import List, Optional

from .core import GitMirrorEngine, GitMirrorError


class GitMirrorCLI:
    """GitMirror命令行界面"""
    
    def __init__(self):
        self.engine = GitMirrorEngine()
    
    def _print_success(self, message: str):
        print(f"\033[32m✓ {message}\033[0m")
    
    def _print_error(self, message: str):
        print(f"\033[31m✗ {message}\033[0m", file=sys.stderr)
    
    def _print_info(self, message: str):
        print(f"\033[36mℹ {message}\033[0m")
    
    def _print_warning(self, message: str):
        print(f"\033[33m⚠ {message}\033[0m")
    
    def cmd_add(self, args):
        """添加仓库"""
        try:
            branches = args.branches.split(",") if args.branches else None
            self.engine.add_repository(
                name=args.name,
                source_url=args.source,
                target_url=args.target,
                branches=branches,
                tags=not args.no_tags
            )
            self._print_success(f"仓库 '{args.name}' 添加成功")
            self._print_info(f"  源地址: {args.source}")
            self._print_info(f"  目标地址: {args.target}")
            if branches:
                self._print_info(f"  同步分支: {', '.join(branches)}")
        except GitMirrorError as e:
            self._print_error(str(e))
            return 1
        return 0
    
    def cmd_remove(self, args):
        """移除仓库"""
        try:
            self.engine.remove_repository(args.name)
            self._print_success(f"仓库 '{args.name}' 移除成功")
        except GitMirrorError as e:
            self._print_error(str(e))
            return 1
        return 0
    
    def cmd_list(self, args):
        """列出仓库"""
        repos = self.engine.list_repositories()
        if not repos:
            self._print_info("暂无配置的仓库")
            return 0
        
        print(f"\n{'名称':<20} {'状态':<10} {'源平台':<10} {'目标平台':<10} {'最后同步':<20}")
        print("-" * 75)
        
        for repo in repos:
            source_platform = self.engine.detect_platform(repo["source_url"])
            target_platform = self.engine.detect_platform(repo["target_url"])
            last_sync = repo["last_sync"] or "从未"
            status_icon = {
                "success": "\033[32m●\033[0m",
                "error": "\033[31m●\033[0m",
                "syncing": "\033[33m●\033[0m",
                "pending": "\033[37m●\033[0m"
            }.get(repo["status"], "○")
            
            print(f"{repo['name']:<20} {status_icon} {repo['status']:<8} "
                  f"{source_platform:<10} {target_platform:<10} {last_sync:<20}")
        
        print()
        return 0
    
    def cmd_sync(self, args):
        """同步仓库"""
        if args.name:
            try:
                self._print_info(f"开始同步仓库 '{args.name}'...")
                result = self.engine.sync_repository(args.name, force=args.force)
                
                if result["success"]:
                    self._print_success(f"同步完成 ({result['duration']:.2f}s)")
                    self._print_info(f"  同步分支: {', '.join(result['branches_synced']) or '无'}")
                    self._print_info(f"  同步标签: {result['tags_synced']} 个")
                else:
                    self._print_error("同步失败")
                    for error in result["errors"]:
                        self._print_error(f"  - {error}")
                    return 1
            except GitMirrorError as e:
                self._print_error(str(e))
                return 1
        else:
            self._print_info("开始同步所有仓库...")
            results = self.engine.sync_all(force=args.force)
            
            success_count = sum(1 for r in results if r["success"])
            total_count = len(results)
            
            print()
            for result in results:
                status = "\033[32m✓\033[0m" if result["success"] else "\033[31m✗\033[0m"
                print(f"{status} {result['name']}")
            
            print()
            self._print_info(f"同步完成: {success_count}/{total_count} 成功")
        
        return 0
    
    def cmd_status(self, args):
        """查看状态"""
        try:
            status = self.engine.get_status(args.name)
            
            if args.name:
                print(f"\n📦 仓库: {status['name']}")
                print(f"   源地址: {status['source_url']}")
                print(f"   目标地址: {status['target_url']}")
                print(f"   源平台: {status['source_platform']}")
                print(f"   目标平台: {status['target_platform']}")
                print(f"   状态: {status['status']}")
                print(f"   同步分支: {', '.join(status['branches'])}")
                print(f"   同步标签: {'是' if status['tags'] else '否'}")
                print(f"   最后同步: {status['last_sync'] or '从未'}")
                print(f"   错误次数: {status['error_count']}")
                print()
            else:
                print(f"\n📊 全局状态")
                print(f"   总仓库数: {status['total']}")
                print(f"   同步中: {status['syncing']}")
                print(f"   成功: {status['success']}")
                print(f"   错误: {status['error']}")
                print(f"   待同步: {status['pending']}")
                print()
        except GitMirrorError as e:
            self._print_error(str(e))
            return 1
        return 0
    
    def cmd_health(self, args):
        """健康检查"""
        try:
            health = self.engine.check_health(args.name)
            
            print(f"\n🏥 健康检查: {health['name']}")
            status_str = "\033[32m健康\033[0m" if health['healthy'] else "\033[31m异常\033[0m"
            print(f"   整体状态: {status_str}")
            print()
            
            print("   检查项:")
            for check, value in health["checks"].items():
                icon = "\033[32m✓\033[0m" if value else "\033[31m✗\033[0m"
                if isinstance(value, bool):
                    print(f"     {icon} {check}: {'正常' if value else '异常'}")
                else:
                    print(f"     ℹ {check}: {value}")
            
            if health["recommendations"]:
                print()
                print("   建议:")
                for rec in health["recommendations"]:
                    self._print_warning(f"   - {rec}")
            
            print()
        except GitMirrorError as e:
            self._print_error(str(e))
            return 1
        return 0
    
    def run(self, args: Optional[List[str]] = None) -> int:
        """运行CLI"""
        parser = argparse.ArgumentParser(
            prog="gitmirror",
            description="GitMirror-CLI - 轻量级Git仓库智能镜像与同步引擎",
            formatter_class=argparse.RawDescriptionHelpFormatter,
            epilog="""
示例:
  gitmirror add myrepo https://github.com/user/repo.git https://gitee.com/user/repo.git
  gitmirror sync myrepo
  gitmirror sync --all
  gitmirror status
  gitmirror list
            """
        )
        
        parser.add_argument("--version", action="version", version="%(prog)s 1.0.0")
        
        subparsers = parser.add_subparsers(dest="command", help="可用命令")
        
        # add 命令
        add_parser = subparsers.add_parser("add", help="添加镜像仓库")
        add_parser.add_argument("name", help="仓库名称")
        add_parser.add_argument("source", help="源仓库URL")
        add_parser.add_argument("target", help="目标仓库URL")
        add_parser.add_argument("--branches", help="要同步的分支，逗号分隔 (默认: main,master)")
        add_parser.add_argument("--no-tags", action="store_true", help="不同步标签")
        
        # remove 命令
        remove_parser = subparsers.add_parser("remove", help="移除镜像仓库")
        remove_parser.add_argument("name", help="仓库名称")
        
        # list 命令
        subparsers.add_parser("list", help="列出所有仓库")
        
        # sync 命令
        sync_parser = subparsers.add_parser("sync", help="同步仓库")
        sync_parser.add_argument("name", nargs="?", help="仓库名称 (不指定则同步所有)")
        sync_parser.add_argument("--force", action="store_true", help="强制同步所有分支")
        
        # status 命令
        status_parser = subparsers.add_parser("status", help="查看状态")
        status_parser.add_argument("name", nargs="?", help="仓库名称")
        
        # health 命令
        health_parser = subparsers.add_parser("health", help="健康检查")
        health_parser.add_argument("name", help="仓库名称")
        
        parsed = parser.parse_args(args)
        
        if not parsed.command:
            parser.print_help()
            return 0
        
        command_map = {
            "add": self.cmd_add,
            "remove": self.cmd_remove,
            "list": self.cmd_list,
            "sync": self.cmd_sync,
            "status": self.cmd_status,
            "health": self.cmd_health
        }
        
        handler = command_map.get(parsed.command)
        if handler:
            return handler(parsed)
        
        return 0


def main():
    """入口函数"""
    cli = GitMirrorCLI()
    sys.exit(cli.run())


if __name__ == "__main__":
    main()
