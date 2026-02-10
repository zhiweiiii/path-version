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


def find_executable(name):
    """查找可执行文件路径
    
    Args:
        name (str): 可执行文件名称
    
    Returns:
        list: 可执行文件路径列表
    """
    paths = []
    
    # 扫描系统常见安装目录
    common_dirs = [
        # Windows系统目录
        os.environ.get('ProgramFiles', ''),
        os.environ.get('ProgramFiles(x86)', ''),
        os.environ.get('LOCALAPPDATA', ''),
        # 常见的软件安装目录
        os.path.join(os.environ.get('ProgramFiles', ''), 'Python'),
        os.path.join(os.environ.get('LOCALAPPDATA', ''), 'Programs'),
        os.path.join(os.environ.get('LOCALAPPDATA', ''), 'Microsoft', 'WindowsApps'),
        # Java相关目录
        os.path.join(os.environ.get('ProgramFiles', ''), 'Java'),
        # Git相关目录
        os.path.join(os.environ.get('ProgramFiles', ''), 'Git', 'bin'),
    ]
    
    # 扫描常见目录
    for base_dir in common_dirs:
        if base_dir and os.path.exists(base_dir):
            # 递归搜索目录
            for root, dirs, files in os.walk(base_dir):
                # 检查文件
                for file in files:
                    if file == name or file == f"{name}.exe":
                        exe_path = os.path.join(root, file)
                        if os.path.isfile(exe_path):
                            paths.append(exe_path)
    
    # 从系统PATH环境变量中查找（作为补充）
    path_env = os.environ.get('PATH', '')
    for path in path_env.split(';'):
        if path.strip():
            exe_path = os.path.join(path, name)
            if os.path.exists(exe_path):
                paths.append(exe_path)
            # 检查带.exe扩展名的版本
            exe_path_exe = f"{exe_path}.exe"
            if os.path.exists(exe_path_exe):
                paths.append(exe_path_exe)
    
    # 去重并返回
    return list(set(paths))


def scan_python_versions():
    """扫描Python版本"""
    versions = {}
    
    try:
        # 使用Python的方式查找Python可执行文件
        python_paths = find_executable("python")
        
        for path in python_paths:
            if os.path.exists(path):
                # 获取Python版本
                try:
                    version_result = subprocess.run(
                        [path, "--version"], 
                        capture_output=True, 
                        text=True,
                        creationflags=subprocess.CREATE_NO_WINDOW
                    )
                    if version_result.returncode == 0:
                        version_match = re.search(r"Python (\d+\.\d+\.\d+)", version_result.stderr)
                        if version_match:
                            version = version_match.group(1)
                            versions[version] = path
                except:
                    pass
    except:
        pass
    
    return {"Python": versions}


def scan_node_versions():
    """扫描Node.js版本"""
    versions = {}
    
    try:
        # 使用Python的方式查找Node.js可执行文件
        node_paths = find_executable("node")
        
        for path in node_paths:
            if os.path.exists(path):
                # 获取Node.js版本
                try:
                    version_result = subprocess.run(
                        [path, "--version"], 
                        capture_output=True, 
                        text=True,
                        creationflags=subprocess.CREATE_NO_WINDOW
                    )
                    if version_result.returncode == 0:
                        version = version_result.stdout.strip().lstrip('v')
                        versions[version] = path
                except:
                    pass
    except:
        pass
    
    return {"Node.js": versions}


def scan_java_versions():
    """扫描Java版本"""
    versions = {}
    
    try:
        # 使用Python的方式查找Java可执行文件
        java_paths = find_executable("java")
        
        for path in java_paths:
            if os.path.exists(path):
                # 获取Java版本
                try:
                    version_result = subprocess.run(
                        [path, "-version"], 
                        capture_output=True, 
                        text=True,
                        creationflags=subprocess.CREATE_NO_WINDOW
                    )
                    if version_result.returncode == 0:
                        version_match = re.search(r'version "(\d+\.\d+\.\d+.*?)"', version_result.stderr)
                        if version_match:
                            version = version_match.group(1)
                            versions[version] = path
                except:
                    pass
    except:
        pass
    
    return {"Java": versions}


def scan_git_versions():
    """扫描Git版本"""
    versions = {}
    
    try:
        # 使用Python的方式查找Git可执行文件
        git_paths = find_executable("git")
        
        for path in git_paths:
            if os.path.exists(path):
                # 获取Git版本
                try:
                    version_result = subprocess.run(
                        [path, "--version"], 
                        capture_output=True, 
                        text=True,
                        creationflags=subprocess.CREATE_NO_WINDOW
                    )
                    if version_result.returncode == 0:
                        version_match = re.search(r"git version (\d+\.\d+\.\d+.*?)", version_result.stdout)
                        if version_match:
                            version = version_match.group(1)
                            versions[version] = path
                except:
                    pass
    except:
        pass
    
    return {"Git": versions}
