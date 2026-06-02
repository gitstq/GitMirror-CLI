# 🪞 GitMirror-CLI

<div align="center">

**Lightweight Git Repository Intelligent Mirror & Sync Engine**

**轻量级Git仓库智能镜像与同步引擎**

[![Python](https://img.shields.io/badge/Python-3.8%2B-blue)](https://python.org)
[![License](https://img.shields.io/badge/License-MIT-green)](LICENSE)
[![Zero Dependencies](https://img.shields.io/badge/Zero%20Dependencies-✓-brightgreen)]()
[![Platforms](https://img.shields.io/badge/Platforms-GitHub%20%7C%20GitLab%20%7C%20Gitee%20%7C%20Codeberg-orange)]()

[简体中文](#简体中文) | [繁體中文](#繁體中文) | [English](#english)

</div>

---

## 简体中文

### 🎉 项目介绍

**GitMirror-CLI** 是一款零依赖的轻量级Git仓库智能镜像与同步引擎，专为开发者打造的多平台代码仓库同步解决方案。

在当下的开发环境中，开发者常常需要在多个Git平台（GitHub、GitLab、Gitee、Codeberg等）之间维护相同的代码仓库。手动同步不仅耗时耗力，还容易遗漏分支和标签。GitMirror-CLI 正是为了解决这一痛点而生——**一键配置，智能同步，让代码镜像变得前所未有的简单**。

**灵感来源**：当前GitHub Trending上缺乏一个专注于多平台Git仓库自动镜像同步的轻量级CLI工具。现有方案要么过于复杂（需要完整部署），要么功能单一。GitMirror-CLI 填补了这一空白。

**自研差异化亮点**：
- 🚀 **零依赖设计**：纯Python标准库实现，无需安装任何第三方包
- 🌐 **多平台支持**：GitHub / GitLab / Gitee / Codeberg / Bitbucket 一键同步
- 🧠 **智能增量同步**：仅同步变更的分支和标签，大幅提升效率
- 🔍 **自动健康检查**：监控镜像状态，自动检测异常并给出修复建议
- 📊 **彩色TUI界面**：直观的终端界面，实时展示同步状态

### ✨ 核心特性

| 特性 | 说明 |
|------|------|
| 🚀 **零依赖** | 纯Python 3.8+标准库实现，零第三方依赖 |
| 🌐 **多平台** | 支持GitHub、GitLab、Gitee、Codeberg、Bitbucket |
| 🔄 **智能同步** | 增量同步，仅推送变更的分支和标签 |
| 🏥 **健康检查** | 自动检测仓库可访问性、同步状态、错误次数 |
| 📊 **状态监控** | 实时查看所有仓库的同步状态和最后同步时间 |
| 🎨 **彩色输出** | 美观的终端彩色输出，提升使用体验 |
| 💾 **配置持久化** | JSON格式配置，自动保存和加载 |
| 📝 **完整日志** | 每日日志文件，方便排查问题 |

### 🚀 快速开始

#### 环境要求

- **Python** >= 3.8
- **Git** >= 2.20

#### 安装

```bash
# 从PyPI安装（推荐）
pip install gitmirror-cli

# 或从源码安装
git clone https://github.com/gitstq/GitMirror-CLI.git
cd GitMirror-CLI
pip install -e .
```

#### 基本使用

```bash
# 添加镜像仓库
gitmirror add myrepo \
  https://github.com/username/repo.git \
  https://gitee.com/username/repo.git \
  --branches main,dev

# 查看所有仓库
gitmirror list

# 同步指定仓库
gitmirror sync myrepo

# 同步所有仓库
gitmirror sync

# 查看状态
gitmirror status

# 健康检查
gitmirror health myrepo

# 移除仓库
gitmirror remove myrepo
```

### 📖 详细使用指南

#### 添加仓库

```bash
gitmirror add <名称> <源地址> <目标地址> [选项]

选项:
  --branches    要同步的分支，逗号分隔 (默认: main,master)
  --no-tags     不同步标签
```

#### 同步策略

- **首次同步**：自动使用 `--mirror` 模式克隆完整仓库
- **增量同步**：仅推送变更的分支和标签
- **强制同步**：使用 `--force` 同步所有远程分支

#### 健康检查说明

健康检查会验证以下内容：
- ✅ 源仓库可访问性
- ✅ 目标仓库可访问性
- ✅ 连续失败次数（超过3次报警）
- ✅ 最后同步时间（超过24小时提醒）

### 💡 设计思路与迭代规划

**技术选型原因**：
- 选择纯Python标准库实现，确保零依赖、跨平台兼容
- 使用 `argparse` 构建CLI，简洁稳定
- JSON格式配置，便于人工编辑和版本控制

**后续迭代计划**：
- [ ] Webhook自动触发同步
- [ ] 定时任务调度（cron模式）
- [ ] 并发同步多仓库
- [ ] 同步历史记录与回滚
- [ ] 配置文件加密存储

### 📦 打包与部署

```bash
# 构建分发包
python setup.py sdist bdist_wheel

# 本地安装
pip install dist/gitmirror-cli-1.0.0.tar.gz
```

### 🤝 贡献指南

欢迎提交Issue和PR！请遵循以下规范：
- 使用 [Angular Commit Message](https://github.com/angular/angular/blob/main/CONTRIBUTING.md#-commit-message-format) 格式
- 提交前运行测试：`python tests/test_core.py`
- 确保代码符合PEP 8规范

### 📄 开源协议

本项目采用 [MIT License](LICENSE) 开源协议。

---

## 繁體中文

### 🎉 專案介紹

**GitMirror-CLI** 是一款零依賴的輕量級Git倉庫智慧鏡像與同步引擎，專為開發者打造的多平台程式碼倉庫同步解決方案。

在當下的開發環境中，開發者常常需要在多個Git平台（GitHub、GitLab、Gitee、Codeberg等）之間維護相同的程式碼倉庫。手動同步不僅耗時耗力，還容易遺漏分支和標籤。GitMirror-CLI 正是為了解決這一痛點而生——**一鍵配置，智慧同步，讓程式碼鏡像變得前所未有的簡單**。

**自研差異化亮點**：
- 🚀 **零依賴設計**：純Python標準庫實現，無需安裝任何第三方套件
- 🌐 **多平台支援**：GitHub / GitLab / Gitee / Codeberg / Bitbucket 一鍵同步
- 🧠 **智慧增量同步**：僅同步變更的分支和標籤，大幅提升效率
- 🔍 **自動健康檢查**：監控鏡像狀態，自動檢測異常並給出修復建議

### ✨ 核心特性

| 特性 | 說明 |
|------|------|
| 🚀 **零依賴** | 純Python 3.8+標準庫實現，零第三方依賴 |
| 🌐 **多平台** | 支援GitHub、GitLab、Gitee、Codeberg、Bitbucket |
| 🔄 **智慧同步** | 增量同步，僅推送變更的分支和標籤 |
| 🏥 **健康檢查** | 自動檢測倉庫可訪問性、同步狀態、錯誤次數 |
| 📊 **狀態監控** | 即時查看所有倉庫的同步狀態和最後同步時間 |

### 🚀 快速開始

#### 環境要求

- **Python** >= 3.8
- **Git** >= 2.20

#### 安裝

```bash
pip install gitmirror-cli
```

#### 基本使用

```bash
# 添加鏡像倉庫
gitmirror add myrepo \
  https://github.com/username/repo.git \
  https://gitee.com/username/repo.git \
  --branches main,dev

# 查看所有倉庫
gitmirror list

# 同步指定倉庫
gitmirror sync myrepo

# 同步所有倉庫
gitmirror sync

# 查看狀態
gitmirror status

# 健康檢查
gitmirror health myrepo
```

### 📄 開源協議

本專案採用 [MIT License](LICENSE) 開源協議。

---

## English

### 🎉 Introduction

**GitMirror-CLI** is a zero-dependency, lightweight Git repository intelligent mirror and sync engine designed for developers who need to maintain code repositories across multiple platforms.

In today's development landscape, developers often need to maintain identical code repositories across multiple Git platforms (GitHub, GitLab, Gitee, Codeberg, etc.). Manual synchronization is time-consuming, error-prone, and easy to miss branches and tags. GitMirror-CLI was born to solve this pain point — **configure once, sync intelligently, make code mirroring easier than ever**.

**Key Differentiators**:
- 🚀 **Zero Dependencies**: Pure Python standard library, no third-party packages required
- 🌐 **Multi-Platform**: One-click sync for GitHub / GitLab / Gitee / Codeberg / Bitbucket
- 🧠 **Intelligent Incremental Sync**: Only sync changed branches and tags for maximum efficiency
- 🔍 **Auto Health Check**: Monitor mirror status, detect anomalies and provide fix suggestions

### ✨ Core Features

| Feature | Description |
|---------|-------------|
| 🚀 **Zero Dependencies** | Pure Python 3.8+ standard library, zero third-party dependencies |
| 🌐 **Multi-Platform** | Support GitHub, GitLab, Gitee, Codeberg, Bitbucket |
| 🔄 **Smart Sync** | Incremental sync, only push changed branches and tags |
| 🏥 **Health Check** | Auto-detect repository accessibility, sync status, error count |
| 📊 **Status Monitor** | Real-time view of all repositories' sync status and last sync time |

### 🚀 Quick Start

#### Requirements

- **Python** >= 3.8
- **Git** >= 2.20

#### Installation

```bash
pip install gitmirror-cli
```

#### Basic Usage

```bash
# Add a mirror repository
gitmirror add myrepo \
  https://github.com/username/repo.git \
  https://gitlab.com/username/repo.git \
  --branches main,dev

# List all repositories
gitmirror list

# Sync specific repository
gitmirror sync myrepo

# Sync all repositories
gitmirror sync

# Check status
gitmirror status

# Health check
gitmirror health myrepo
```

### 📄 License

This project is licensed under the [MIT License](LICENSE).

---

<div align="center">

**Made with ❤️ by GitMirror Team**

⭐ Star us on GitHub if you find this useful!

</div>
