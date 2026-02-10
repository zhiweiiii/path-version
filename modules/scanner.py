#!/usr/bin/env python3
"""软件版本扫描模块"""

import os
import re
import subprocess
import threading
import time
import json
import tempfile


# 缓存文件路径
CACHE_FILE = os.path.join(tempfile.gettempdir(), "software_scan_cache.json")
CACHE_DURATION = 3600  # 缓存有效期（秒）

# 全局变量
full_scan_running = False
full_scan_results = {}


def load_cache():
    """加载缓存"""
    try:
        if os.path.exists(CACHE_FILE):
            with open(CACHE_FILE, 'r', encoding='utf-8') as f:
                cache_data = json.load(f)
            # 检查缓存是否过期
            if time.time() - cache_data.get('timestamp', 0) < CACHE_DURATION:
                return cache_data.get('results', {})
    except:
        pass
    return {}


def save_cache(results):
    """保存缓存"""
    try:
        cache_data = {
            'timestamp': time.time(),
            'results': results
        }
        with open(CACHE_FILE, 'w', encoding='utf-8') as f:
            json.dump(cache_data, f, ensure_ascii=False, indent=2)
    except:
        pass


def scan_software_versions():
    """扫描系统中已安装的软件版本
    
    Returns:
        dict: 软件名称 -> {版本号 -> 安装路径}
    """
    # 尝试加载缓存
    cached_results = load_cache()
    if cached_results:
        return cached_results
    
    software_versions = {}
    
    # 扫描常见软件
    software_versions.update(scan_python_versions())
    software_versions.update(scan_node_versions())
    software_versions.update(scan_java_versions())
    software_versions.update(scan_git_versions())
    
    # 保存缓存
    save_cache(software_versions)
    
    # 启动异步全盘扫描
    start_full_scan()
    
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


def get_all_drives():
    """获取所有驱动器"""
    drives = []
    if os.name == 'nt':  # Windows系统
        import ctypes
        drives_bitmask = ctypes.windll.kernel32.GetLogicalDrives()
        for letter in 'ABCDEFGHIJKLMNOPQRSTUVWXYZ':
            if drives_bitmask & 1:
                drives.append(f"{letter}:\\")
            drives_bitmask >>= 1
    else:
        # 非Windows系统，返回常见路径
        drives = ['/']
    return drives


def full_scan():
    """全盘扫描软件"""
    global full_scan_running, full_scan_results
    
    if full_scan_running:
        return
    
    full_scan_running = True
    full_scan_results = {}
    
    try:
        # 获取所有驱动器
        drives = get_all_drives()
        
        # 要扫描的可执行文件
        executables = {
            "python": "Python",
            "node": "Node.js",
            "java": "Java",
            "git": "Git"
        }
        
        # 扫描结果
        scan_results = {}
        
        # 遍历所有驱动器
        for drive in drives:
            if os.path.exists(drive):
                # 遍历驱动器中的文件
                for root, dirs, files in os.walk(drive):
                    # 跳过系统目录和隐藏目录
                    dirs[:] = [d for d in dirs if not d.startswith('.') and d not in ['Windows', 'System32', 'Program Files', 'Program Files (x86)', '$Recycle.Bin']]
                    
                    # 检查文件
                    for file in files:
                        for exe_name, software_name in executables.items():
                            if file == exe_name or file == f"{exe_name}.exe":
                                exe_path = os.path.join(root, file)
                                if os.path.isfile(exe_path):
                                    # 尝试获取版本信息
                                    version = get_version_info(exe_name, exe_path)
                                    if version:
                                        if software_name not in scan_results:
                                            scan_results[software_name] = {}
                                        scan_results[software_name][version] = exe_path
        
        # 更新全局结果
        full_scan_results = scan_results
        
        # 如果有新结果，更新缓存
        if scan_results:
            # 加载现有缓存
            current_results = load_cache()
            # 合并结果
            for software, versions in scan_results.items():
                if software not in current_results:
                    current_results[software] = {}
                current_results[software].update(versions)
            # 保存更新后的缓存
            save_cache(current_results)
            
    except:
        pass
    finally:
        full_scan_running = False


def get_version_info(exe_name, exe_path):
    """获取可执行文件版本信息
    
    Args:
        exe_name (str): 可执行文件名称
        exe_path (str): 可执行文件路径
    
    Returns:
        str: 版本号或None
    """
    try:
        if exe_name == "python":
            result = subprocess.run(
                [exe_path, "--version"], 
                capture_output=True, 
                text=True,
                creationflags=subprocess.CREATE_NO_WINDOW
            )
            if result.returncode == 0:
                match = re.search(r"Python (\d+\.\d+\.\d+)", result.stderr)
                if match:
                    return match.group(1)
        
        elif exe_name == "node":
            result = subprocess.run(
                [exe_path, "--version"], 
                capture_output=True, 
                text=True,
                creationflags=subprocess.CREATE_NO_WINDOW
            )
            if result.returncode == 0:
                return result.stdout.strip().lstrip('v')
        
        elif exe_name == "java":
            result = subprocess.run(
                [exe_path, "-version"], 
                capture_output=True, 
                text=True,
                creationflags=subprocess.CREATE_NO_WINDOW
            )
            if result.returncode == 0:
                match = re.search(r'version "(\d+\.\d+\.\d+.*?)"', result.stderr)
                if match:
                    return match.group(1)
        
        elif exe_name == "git":
            result = subprocess.run(
                [exe_path, "--version"], 
                capture_output=True, 
                text=True,
                creationflags=subprocess.CREATE_NO_WINDOW
            )
            if result.returncode == 0:
                match = re.search(r"git version (\d+\.\d+\.\d+.*?)", result.stdout)
                if match:
                    return match.group(1)
    except:
        pass
    return None


def start_full_scan():
    """启动异步全盘扫描"""
    global full_scan_running
    
    if not full_scan_running:
        scan_thread = threading.Thread(target=full_scan)
        scan_thread.daemon = True
        scan_thread.start()
