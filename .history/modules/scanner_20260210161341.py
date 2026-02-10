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
    
    # 从系统PATH环境变量中查找
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
