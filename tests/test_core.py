#!/usr/bin/env python3
"""
GitMirror Core Tests - 核心引擎测试
"""

import os
import sys
import json
import tempfile
import shutil
from pathlib import Path

# 添加项目根目录到路径
sys.path.insert(0, str(Path(__file__).parent.parent))

from gitmirror.core import GitMirrorEngine, RepositoryConfig, GitMirrorError


def test_repository_config():
    """测试仓库配置"""
    print("测试 RepositoryConfig...")
    
    repo = RepositoryConfig(
        name="test-repo",
        source_url="https://github.com/user/repo.git",
        target_url="https://gitee.com/user/repo.git",
        branches=["main", "dev"],
        tags=True
    )
    
    assert repo.name == "test-repo"
    assert repo.source_url == "https://github.com/user/repo.git"
    assert repo.target_url == "https://gitee.com/user/repo.git"
    assert repo.branches == ["main", "dev"]
    assert repo.tags == True
    
    # 测试序列化
    data = repo.to_dict()
    assert data["name"] == "test-repo"
    
    # 测试反序列化
    repo2 = RepositoryConfig.from_dict(data)
    assert repo2.name == repo.name
    
    print("  ✓ RepositoryConfig 测试通过")


def test_engine_initialization():
    """测试引擎初始化"""
    print("测试 GitMirrorEngine 初始化...")
    
    with tempfile.TemporaryDirectory() as tmpdir:
        engine = GitMirrorEngine(config_dir=tmpdir)
        
        assert engine.config_dir == Path(tmpdir)
        assert (Path(tmpdir) / "config.json").exists() == False  # 初始无配置
        assert (Path(tmpdir) / "repos").exists()
        assert (Path(tmpdir) / "logs").exists()
    
    print("  ✓ GitMirrorEngine 初始化测试通过")


def test_detect_platform():
    """测试平台检测"""
    print("测试平台检测...")
    
    engine = GitMirrorEngine(config_dir=tempfile.mkdtemp())
    
    test_cases = [
        ("https://github.com/user/repo.git", "github"),
        ("https://gitlab.com/user/repo.git", "gitlab"),
        ("https://gitee.com/user/repo.git", "gitee"),
        ("https://codeberg.org/user/repo.git", "codeberg"),
        ("https://bitbucket.org/user/repo.git", "bitbucket"),
        ("https://unknown.com/repo.git", "unknown"),
    ]
    
    for url, expected in test_cases:
        result = engine.detect_platform(url)
        assert result == expected, f"期望 {expected}, 得到 {result} for {url}"
    
    print("  ✓ 平台检测测试通过")


def test_add_remove_repository():
    """测试添加和移除仓库"""
    print("测试添加/移除仓库...")
    
    with tempfile.TemporaryDirectory() as tmpdir:
        engine = GitMirrorEngine(config_dir=tmpdir)
        
        # 添加仓库
        engine.add_repository(
            name="test-repo",
            source_url="https://github.com/user/repo.git",
            target_url="https://gitee.com/user/repo.git",
            branches=["main"]
        )
        
        assert "test-repo" in engine.repositories
        assert engine.repositories["test-repo"].name == "test-repo"
        
        # 重复添加应报错
        try:
            engine.add_repository(
                name="test-repo",
                source_url="https://github.com/user/repo2.git",
                target_url="https://gitee.com/user/repo2.git"
            )
            assert False, "应该抛出异常"
        except GitMirrorError:
            pass
        
        # 移除仓库
        engine.remove_repository("test-repo")
        assert "test-repo" not in engine.repositories
        
        # 移除不存在的仓库应报错
        try:
            engine.remove_repository("non-existent")
            assert False, "应该抛出异常"
        except GitMirrorError:
            pass
    
    print("  ✓ 添加/移除仓库测试通过")


def test_config_persistence():
    """测试配置持久化"""
    print("测试配置持久化...")
    
    with tempfile.TemporaryDirectory() as tmpdir:
        # 创建引擎并添加仓库
        engine1 = GitMirrorEngine(config_dir=tmpdir)
        engine1.add_repository(
            name="persist-test",
            source_url="https://github.com/user/repo.git",
            target_url="https://gitee.com/user/repo.git"
        )
        
        # 创建新引擎实例，验证配置加载
        engine2 = GitMirrorEngine(config_dir=tmpdir)
        assert "persist-test" in engine2.repositories
        assert engine2.repositories["persist-test"].source_url == "https://github.com/user/repo.git"
    
    print("  ✓ 配置持久化测试通过")


def test_invalid_url():
    """测试无效URL"""
    print("测试无效URL...")
    
    with tempfile.TemporaryDirectory() as tmpdir:
        engine = GitMirrorEngine(config_dir=tmpdir)
        
        try:
            engine.add_repository(
                name="bad-url",
                source_url="not-a-valid-url",
                target_url="https://gitee.com/user/repo.git"
            )
            assert False, "应该抛出异常"
        except GitMirrorError as e:
            assert "格式无效" in str(e)
    
    print("  ✓ 无效URL测试通过")


def run_all_tests():
    """运行所有测试"""
    print("=" * 50)
    print("GitMirror-CLI 测试套件")
    print("=" * 50)
    print()
    
    tests = [
        test_repository_config,
        test_engine_initialization,
        test_detect_platform,
        test_add_remove_repository,
        test_config_persistence,
        test_invalid_url,
    ]
    
    passed = 0
    failed = 0
    
    for test in tests:
        try:
            test()
            passed += 1
        except Exception as e:
            print(f"  ✗ {test.__name__} 失败: {e}")
            failed += 1
    
    print()
    print("=" * 50)
    print(f"测试结果: {passed} 通过, {failed} 失败")
    print("=" * 50)
    
    return failed == 0


if __name__ == "__main__":
    success = run_all_tests()
    sys.exit(0 if success else 1)
