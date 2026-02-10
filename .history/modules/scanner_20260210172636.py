#!/usr/bin/env python3
"""软件版本扫描模块"""

import os
import re
import ctypes
from ctypes import wintypes


# 定义常量
CREATE_NO_WINDOW = 0x08000000


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
    print(f"开始查找可执行文件: {name}")
    paths = []
    
    # 从系统PATH环境变量中查找
    path_env = os.environ.get('PATH', '')
    print(f"PATH环境变量: {path_env}")
    
    for path in path_env.split(';'):
        if path.strip():
            exe_path = os.path.join(path, name)
            print(f"检查路径: {exe_path}")
            if os.path.exists(exe_path):
                print(f"找到可执行文件: {exe_path}")
                paths.append(exe_path)
            # 检查带.exe扩展名的版本
            exe_path_exe = f"{exe_path}.exe"
            print(f"检查路径: {exe_path_exe}")
            if os.path.exists(exe_path_exe):
                print(f"找到可执行文件: {exe_path_exe}")
                paths.append(exe_path_exe)
    
    # 去重并返回
    print(f"找到的可执行文件路径: {list(set(paths))}")
    return list(set(paths))


def run_command(cmd, cwd=None):
    """运行命令，不显示控制台窗口
    
    Args:
        cmd (list): 命令及其参数
        cwd (str, optional): 工作目录
    
    Returns:
        tuple: (stdout, stderr, returncode)
    """
    # 设置进程信息
    class STARTUPINFO(ctypes.Structure):
        _fields_ = [
            ('cb', wintypes.DWORD),
            ('lpReserved', wintypes.LPWSTR),
            ('lpDesktop', wintypes.LPWSTR),
            ('lpTitle', wintypes.LPWSTR),
            ('dwX', wintypes.DWORD),
            ('dwY', wintypes.DWORD),
            ('dwXSize', wintypes.DWORD),
            ('dwYSize', wintypes.DWORD),
            ('dwXCountChars', wintypes.DWORD),
            ('dwYCountChars', wintypes.DWORD),
            ('dwFillAttribute', wintypes.DWORD),
            ('dwFlags', wintypes.DWORD),
            ('wShowWindow', wintypes.WORD),
            ('cbReserved2', wintypes.WORD),
            ('lpReserved2', ctypes.POINTER(wintypes.BYTE)),
            ('hStdInput', wintypes.HANDLE),
            ('hStdOutput', wintypes.HANDLE),
            ('hStdError', wintypes.HANDLE),
        ]
    
    class PROCESS_INFORMATION(ctypes.Structure):
        _fields_ = [
            ('hProcess', wintypes.HANDLE),
            ('hThread', wintypes.HANDLE),
            ('dwProcessId', wintypes.DWORD),
            ('dwThreadId', wintypes.DWORD),
        ]
    
    # 初始化STARTUPINFO
    si = STARTUPINFO()
    si.cb = ctypes.sizeof(STARTUPINFO)
    si.dwFlags = 0x00000100  # STARTF_USESTDHANDLES
    
    # 创建管道用于捕获输出
    hStdOutRead, hStdOutWrite = ctypes.windll.kernel32.CreatePipe(None, 0, None, 0)
    hStdErrRead, hStdErrWrite = ctypes.windll.kernel32.CreatePipe(None, 0, None, 0)
    
    si.hStdOutput = hStdOutWrite
    si.hStdError = hStdErrWrite
    
    # 准备命令行
    cmd_line = ' '.join(cmd)
    # CreateProcessW 需要一个可变的字符串缓冲区
    cmd_line_buffer = ctypes.create_unicode_buffer(cmd_line)
    
    # 创建进程
    pi = PROCESS_INFORMATION()
    success = ctypes.windll.kernel32.CreateProcessW(
        None,
        cmd_line_buffer,
        None,
        None,
        True,  # 继承句柄
        CREATE_NO_WINDOW,  # 不创建窗口
        None,
        cwd,
        ctypes.byref(si),
        ctypes.byref(pi)
    )
    
    if not success:
        return '', '', -1
    
    # 关闭写入端
    ctypes.windll.kernel32.CloseHandle(hStdOutWrite)
    ctypes.windll.kernel32.CloseHandle(hStdErrWrite)
    
    # 读取输出
    def read_pipe(handle):
        buffer = ctypes.create_unicode_buffer(4096)
        output = []
        while True:
            bytes_read = wintypes.DWORD(0)
            if ctypes.windll.kernel32.ReadFile(handle, buffer, 4096, ctypes.byref(bytes_read), None):
                if bytes_read.value > 0:
                    output.append(buffer.value[:bytes_read.value])
                else:
                    break
            else:
                break
        return ''.join(output)
    
    stdout = read_pipe(hStdOutRead)
    stderr = read_pipe(hStdErrRead)
    
    # 关闭读取端
    ctypes.windll.kernel32.CloseHandle(hStdOutRead)
    ctypes.windll.kernel32.CloseHandle(hStdErrRead)
    
    # 等待进程结束
    ctypes.windll.kernel32.WaitForSingleObject(pi.hProcess, -1)
    
    # 获取退出码
    exit_code = wintypes.DWORD(0)
    ctypes.windll.kernel32.GetExitCodeProcess(pi.hProcess, ctypes.byref(exit_code))
    
    # 关闭进程和线程句柄
    ctypes.windll.kernel32.CloseHandle(pi.hProcess)
    ctypes.windll.kernel32.CloseHandle(pi.hThread)
    
    return stdout, stderr, exit_code.value


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
                    stdout, stderr, returncode = run_command([path, "--version"])
                    if returncode == 0:
                        version_match = re.search(r"Python (\d+\.\d+\.\d+)", stderr)
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
                    stdout, stderr, returncode = run_command([path, "--version"])
                    if returncode == 0:
                        version = stdout.strip().lstrip('v')
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
                    stdout, stderr, returncode = run_command([path, "-version"])
                    if returncode == 0:
                        version_match = re.search(r'version "(\d+\.\d+\.\d+.*?)"', stderr)
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
                    stdout, stderr, returncode = run_command([path, "--version"])
                    if returncode == 0:
                        version_match = re.search(r"git version (\d+\.\d+\.\d+.*?)", stdout)
                        if version_match:
                            version = version_match.group(1)
                            versions[version] = path
                except:
                    pass
    except:
        pass
    
    return {"Git": versions}
