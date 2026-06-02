#!/usr/bin/env python3
"""
GitMirror-CLI Setup
"""

from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="gitmirror-cli",
    version="1.0.0",
    author="GitMirror Team",
    author_email="gitmirror@example.com",
    description="轻量级Git仓库智能镜像与同步引擎 - Lightweight Git Repository Intelligent Mirror & Sync Engine",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/gitstq/GitMirror-CLI",
    packages=find_packages(),
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "Topic :: Software Development :: Version Control :: Git",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.8",
    entry_points={
        "console_scripts": [
            "gitmirror=gitmirror.cli:main",
        ],
    },
    keywords="git mirror sync github gitlab gitee codeberg cli tool",
    project_urls={
        "Bug Reports": "https://github.com/gitstq/GitMirror-CLI/issues",
        "Source": "https://github.com/gitstq/GitMirror-CLI",
    },
)
