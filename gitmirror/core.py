#!/usr/bin/env python3
"""
GitMirror Core Engine - 核心同步引擎
"""

import os
import re
import json
import shutil
import subprocess
import tempfile
from pathlib import Path
from datetime import datetime
from typing import Dict, List, Optional, Tuple, Any
from urllib.parse import urlparse


class GitMirrorError(Exception):
    """GitMirror自定义异常"""
    pass


class RepositoryConfig:
    """仓库配置类"""
    
    def __init__(self, name: str, source_url: str, target_url: str, 
                 branches: List[str] = None, tags: bool = True,
                 sync_interval: int = 3600, auto_sync: bool = False):
        self.name = name
        self.source_url = source_url
        self.target_url = target_url
        self.branches = branches or ["main", "master"]
        self.tags = tags
        self.sync_interval = sync_interval
        self.auto_sync = auto_sync
        self.last_sync = None
        self.status = "pending"
        self.error_count = 0
    
    def to_dict(self) -> Dict[str, Any]:
        return {
            "name": self.name,
            "source_url": self.source_url,
            "target_url": self.target_url,
            "branches": self.branches,
            "tags": self.tags,
            "sync_interval": self.sync_interval,
            "auto_sync": self.auto_sync,
            "last_sync": self.last_sync,
            "status": self.status,
            "error_count": self.error_count
        }
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "RepositoryConfig":
        repo = cls(
            name=data["name"],
            source_url=data["source_url"],
            target_url=data["target_url"],
            branches=data.get("branches", ["main", "master"]),
            tags=data.get("tags", True),
            sync_interval=data.get("sync_interval", 3600),
            auto_sync=data.get("auto_sync", False)
        )
        repo.last_sync = data.get("last_sync")
        repo.status = data.get("status", "pending")
        repo.error_count = data.get("error_count", 0)
        return repo


class GitMirrorEngine:
    """Git镜像同步引擎"""
    
    PLATFORM_PATTERNS = {
        "github": r"github\.com",
        "gitlab": r"gitlab\.com",
        "gitee": r"gitee\.com",
        "codeberg": r"codeberg\.org",
        "bitbucket": r"bitbucket\.org"
    }
    
    def __init__(self, config_dir: Optional[str] = None):
        self.config_dir = Path(config_dir or os.path.expanduser("~/.gitmirror"))
        self.config_file = self.config_dir / "config.json"
        self.repos_dir = self.config_dir / "repos"
        self.log_dir = self.config_dir / "logs"
        
        self._ensure_dirs()
        self.repositories: Dict[str, RepositoryConfig] = {}
        self._load_config()
    
    def _ensure_dirs(self):
        """确保目录结构存在"""
        for d in [self.config_dir, self.repos_dir, self.log_dir]:
            d.mkdir(parents=True, exist_ok=True)
    
    def _load_config(self):
        """加载配置"""
        if self.config_file.exists():
            try:
                with open(self.config_file, "r", encoding="utf-8") as f:
                    data = json.load(f)
                    for name, repo_data in data.get("repositories", {}).items():
                        self.repositories[name] = RepositoryConfig.from_dict(repo_data)
            except (json.JSONDecodeError, KeyError) as e:
                self._log(f"配置加载失败: {e}", level="error")
    
    def _save_config(self):
        """保存配置"""
        data = {
            "repositories": {
                name: repo.to_dict() for name, repo in self.repositories.items()
            },
            "updated_at": datetime.now().isoformat()
        }
        with open(self.config_file, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=2, ensure_ascii=False)
    
    def _log(self, message: str, level: str = "info"):
        """记录日志"""
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        log_entry = f"[{timestamp}] [{level.upper()}] {message}"
        
        log_file = self.log_dir / f"{datetime.now().strftime('%Y-%m-%d')}.log"
        with open(log_file, "a", encoding="utf-8") as f:
            f.write(log_entry + "\n")
        
        return log_entry
    
    def _run_git(self, args: List[str], cwd: Optional[str] = None, 
                 env: Optional[Dict[str, str]] = None) -> Tuple[int, str, str]:
        """执行Git命令"""
        cmd = ["git"] + args
        try:
            result = subprocess.run(
                cmd, cwd=cwd, env={**os.environ, **(env or {})},
                capture_output=True, text=True, timeout=300
            )
            return result.returncode, result.stdout, result.stderr
        except subprocess.TimeoutExpired:
            return -1, "", "Git command timed out"
        except FileNotFoundError:
            return -1, "", "Git not found. Please install Git."
    
    def detect_platform(self, url: str) -> str:
        """检测Git平台类型"""
        for platform, pattern in self.PLATFORM_PATTERNS.items():
            if re.search(pattern, url, re.IGNORECASE):
                return platform
        return "unknown"
    
    def add_repository(self, name: str, source_url: str, target_url: str,
                       branches: Optional[List[str]] = None,
                       tags: bool = True) -> bool:
        """添加镜像仓库"""
        if name in self.repositories:
            raise GitMirrorError(f"仓库 '{name}' 已存在")
        
        # 验证URL格式
        for url, label in [(source_url, "源地址"), (target_url, "目标地址")]:
            parsed = urlparse(url)
            if not parsed.scheme or not parsed.netloc:
                raise GitMirrorError(f"{label}格式无效: {url}")
        
        repo = RepositoryConfig(
            name=name, source_url=source_url, target_url=target_url,
            branches=branches or ["main", "master"], tags=tags
        )
        
        self.repositories[name] = repo
        self._save_config()
        self._log(f"添加仓库: {name}")
        return True
    
    def remove_repository(self, name: str) -> bool:
        """移除镜像仓库"""
        if name not in self.repositories:
            raise GitMirrorError(f"仓库 '{name}' 不存在")
        
        # 清理本地缓存
        repo_dir = self.repos_dir / name
        if repo_dir.exists():
            shutil.rmtree(repo_dir)
        
        del self.repositories[name]
        self._save_config()
        self._log(f"移除仓库: {name}")
        return True
    
    def list_repositories(self) -> List[Dict[str, Any]]:
        """列出所有仓库"""
        return [repo.to_dict() for repo in self.repositories.values()]
    
    def sync_repository(self, name: str, force: bool = False) -> Dict[str, Any]:
        """同步单个仓库"""
        if name not in self.repositories:
            raise GitMirrorError(f"仓库 '{name}' 不存在")
        
        repo = self.repositories[name]
        repo.status = "syncing"
        
        result = {
            "name": name,
            "success": False,
            "branches_synced": [],
            "tags_synced": 0,
            "errors": [],
            "duration": 0
        }
        
        start_time = datetime.now()
        repo_dir = self.repos_dir / name
        
        try:
            # 克隆或更新本地镜像
            if not repo_dir.exists():
                self._log(f"[{name}] 首次克隆仓库...")
                code, out, err = self._run_git(
                    ["clone", "--mirror", repo.source_url, str(repo_dir)]
                )
                if code != 0:
                    raise GitMirrorError(f"克隆失败: {err}")
            else:
                self._log(f"[{name}] 更新本地镜像...")
                code, out, err = self._run_git(
                    ["remote", "update"], cwd=str(repo_dir)
                )
                if code != 0:
                    raise GitMirrorError(f"更新失败: {err}")
            
            # 获取所有远程分支
            code, out, err = self._run_git(
                ["branch", "-r"], cwd=str(repo_dir)
            )
            if code != 0:
                raise GitMirrorError(f"获取分支失败: {err}")
            
            remote_branches = [b.strip() for b in out.split("\n") if b.strip()]
            
            # 同步指定分支
            branches_to_sync = repo.branches
            if force:
                # 强制同步所有分支
                branches_to_sync = list(set([
                    b.split("/")[-1] for b in remote_branches 
                    if "/" in b and not b.endswith("/HEAD")
                ]))
            
            synced_branches = []
            for branch in branches_to_sync:
                remote_branch = f"origin/{branch}"
                if any(remote_branch in rb for rb in remote_branches):
                    code, out, err = self._run_git(
                        ["push", "--force", repo.target_url, f"refs/heads/{branch}"],
                        cwd=str(repo_dir)
                    )
                    if code == 0:
                        synced_branches.append(branch)
                        self._log(f"[{name}] 同步分支: {branch}")
                    else:
                        result["errors"].append(f"分支 {branch} 同步失败: {err}")
                else:
                    self._log(f"[{name}] 分支不存在: {branch}", level="warning")
            
            result["branches_synced"] = synced_branches
            
            # 同步标签
            if repo.tags:
                code, out, err = self._run_git(
                    ["push", "--force", repo.target_url, "--tags"],
                    cwd=str(repo_dir)
                )
                if code == 0:
                    # 统计标签数量
                    code, out, err = self._run_git(
                        ["tag", "-l"], cwd=str(repo_dir)
                    )
                    result["tags_synced"] = len([t for t in out.split("\n") if t.strip()])
                    self._log(f"[{name}] 同步标签: {result['tags_synced']} 个")
                else:
                    result["errors"].append(f"标签同步失败: {err}")
            
            result["success"] = len(result["errors"]) == 0
            repo.status = "success" if result["success"] else "error"
            repo.error_count = 0 if result["success"] else repo.error_count + 1
            
        except GitMirrorError as e:
            repo.status = "error"
            repo.error_count += 1
            result["errors"].append(str(e))
            self._log(f"[{name}] 同步错误: {e}", level="error")
        
        repo.last_sync = datetime.now().isoformat()
        self._save_config()
        
        result["duration"] = (datetime.now() - start_time).total_seconds()
        return result
    
    def sync_all(self, force: bool = False) -> List[Dict[str, Any]]:
        """同步所有仓库"""
        results = []
        for name in self.repositories:
            try:
                result = self.sync_repository(name, force=force)
                results.append(result)
            except Exception as e:
                results.append({
                    "name": name,
                    "success": False,
                    "errors": [str(e)]
                })
        return results
    
    def get_status(self, name: Optional[str] = None) -> Dict[str, Any]:
        """获取仓库状态"""
        if name:
            if name not in self.repositories:
                raise GitMirrorError(f"仓库 '{name}' 不存在")
            repo = self.repositories[name]
            return {
                **repo.to_dict(),
                "source_platform": self.detect_platform(repo.source_url),
                "target_platform": self.detect_platform(repo.target_url)
            }
        
        return {
            "total": len(self.repositories),
            "syncing": sum(1 for r in self.repositories.values() if r.status == "syncing"),
            "success": sum(1 for r in self.repositories.values() if r.status == "success"),
            "error": sum(1 for r in self.repositories.values() if r.status == "error"),
            "pending": sum(1 for r in self.repositories.values() if r.status == "pending"),
            "repositories": [self.get_status(n) for n in self.repositories]
        }
    
    def check_health(self, name: str) -> Dict[str, Any]:
        """检查仓库健康状态"""
        if name not in self.repositories:
            raise GitMirrorError(f"仓库 '{name}' 不存在")
        
        repo = self.repositories[name]
        health = {
            "name": name,
            "healthy": True,
            "checks": {},
            "recommendations": []
        }
        
        # 检查源仓库可访问性
        code, _, err = self._run_git(["ls-remote", repo.source_url, "HEAD"])
        health["checks"]["source_accessible"] = code == 0
        if code != 0:
            health["healthy"] = False
            health["recommendations"].append("源仓库无法访问，请检查URL和权限")
        
        # 检查目标仓库可访问性
        code, _, err = self._run_git(["ls-remote", repo.target_url, "HEAD"])
        health["checks"]["target_accessible"] = code == 0
        if code != 0:
            health["healthy"] = False
            health["recommendations"].append("目标仓库无法访问，请检查URL和权限")
        
        # 检查同步状态
        if repo.error_count > 3:
            health["healthy"] = False
            health["recommendations"].append(f"连续失败 {repo.error_count} 次，建议检查配置")
        
        # 检查最后同步时间
        if repo.last_sync:
            last_sync = datetime.fromisoformat(repo.last_sync)
            hours_since = (datetime.now() - last_sync).total_seconds() / 3600
            health["checks"]["hours_since_sync"] = round(hours_since, 2)
            if hours_since > 24:
                health["recommendations"].append("超过24小时未同步")
        
        return health
