#!/usr/bin/env python3
"""软件版本扫描模块"""

import os
import re
import subprocess


def scan_software_versions():
    """扫描系统中已安装的软件版本
    
    Returns:
        dict: 软件名称 -> {版本号 -> 安装路径}
    """
    software_versions = {}
    
    # 扫描常见软件
    software_versions.update(scan_python_versions())
    software_versions.update(scan_node_versions())
    software_versions.update(scan_java_versions())
    software_versions.update(scan_git_versions())
    
    return software_versions


def scan_python_versions():
    """扫描Python版本"""
    versions = {}
    
    try:
        # 检查系统PATH中的Python
        result = subprocess.run(["where", "python"], capture_output=True, text=True)
        if result.returncode == 0:
            python_paths = result.stdout.strip().split('\n')
            for path in python_paths:
                if os.path.exists(path):
                    # 获取Python版本
                    version_result = subprocess.run(
                        [path, "--version"], 
                        capture_output=True, 
                        text=True
                    )
                    if version_result.returncode == 0:
                        version_match = re.search(r"Python (\d+\.\d+\.\d+)", version_result.stderr)
                        if version_match:
                            version = version_match.group(1)
                            versions[version] = path
    except Exception as e:
        print(f"扫描Python版本时出错: {e}")
    
    return {"Python": versions}


def scan_node_versions():
    """扫描Node.js版本"""
    versions = {}
    
    try:
        # 检查系统PATH中的Node.js
        result = subprocess.run(["where", "node"], capture_output=True, text=True)
        if result.returncode == 0:
            node_paths = result.stdout.strip().split('\n')
            for path in node_paths:
                if os.path.exists(path):
                    # 获取Node.js版本
                    version_result = subprocess.run(
                        [path, "--version"], 
                        capture_output=True, 
                        text=True
                    )
                    if version_result.returncode == 0:
                        version = version_result.stdout.strip().lstrip('v')
                        versions[version] = path
    except Exception as e:
        print(f"扫描Node.js版本时出错: {e}")
    
    return {"Node.js": versions}


def scan_java_versions():
    """扫描Java版本"""
    versions = {}
    
    try:
        # 检查系统PATH中的Java
        result = subprocess.run(["where", "java"], capture_output=True, text=True)
        if result.returncode == 0:
            java_paths = result.stdout.strip().split('\n')
            for path in java_paths:
                if os.path.exists(path):
                    # 获取Java版本
                    version_result = subprocess.run(
                        [path, "-version"], 
                        capture_output=True, 
                        text=True
                    )
                    if version_result.returncode == 0:
                        version_match = re.search(r"version "(\d+\.\d+\.\d+.*?)"", version_result.stderr)
                        if version_match:
                            version = version_match.group(1)
                            versions[version] = path
    except Exception as e:
        print(f"扫描Java版本时出错: {e}")
    
    return {"Java": versions}


def scan_git_versions():
    """扫描Git版本"""
    versions = {}
    
    try:
        # 检查系统PATH中的Git
        result = subprocess.run(["where", "git"], capture_output=True, text=True)
        if result.returncode == 0:
            git_paths = result.stdout.strip().split('\n')
            for path in git_paths:
                if os.path.exists(path):
                    # 获取Git版本
                    version_result = subprocess.run(
                        [path, "--version"], 
                        capture_output=True, 
                        text=True
                    )
                    if version_result.returncode == 0:
                        version_match = re.search(r"git version (\d+\.\d+\.\d+.*?)", version_result.stdout)
                        if version_match:
                            version = version_match.group(1)
                            versions[version] = path
    except Exception as e:
        print(f"扫描Git版本时出错: {e}")
    
    return {"Git": versions}
