#!/usr/bin/env python3
"""环境变量管理模块"""

import os
import ctypes
from ctypes import wintypes


def update_environment_variable(name, value, is_system=False):
    """更新环境变量
    
    Args:
        name (str): 环境变量名称
        value (str): 环境变量值
        is_system (bool): 是否更新系统环境变量
    
    Returns:
        bool: 更新是否成功
    """
    try:
        # 定义Windows API函数
        if is_system:
            # 系统环境变量需要管理员权限
            kernel32 = ctypes.WinDLL('kernel32', use_last_error=True)
            kernel32.SetEnvironmentVariableW.argtypes = [wintypes.LPWSTR, wintypes.LPWSTR]
            kernel32.SetEnvironmentVariableW.restype = wintypes.BOOL
            
            # 设置环境变量
            result = kernel32.SetEnvironmentVariableW(name, value)
            if not result:
                print(f"设置系统环境变量失败: {ctypes.get_last_error()}")
                return False
            
            # 广播环境变量变更
            SendMessageTimeout = ctypes.WinDLL('user32').SendMessageTimeoutW
            SendMessageTimeout.argtypes = [
                wintypes.HWND, wintypes.UINT, wintypes.WPARAM, 
                wintypes.LPWSTR, wintypes.UINT, wintypes.UINT, 
                ctypes.POINTER(wintypes.DWORD)
            ]
            HWND_BROADCAST = 0xFFFF
            WM_SETTINGCHANGE = 0x001A
            SMTO_ABORTIFHUNG = 0x0002
            
            SendMessageTimeout(
                HWND_BROADCAST, WM_SETTINGCHANGE, 0, "Environment",
                SMTO_ABORTIFHUNG, 5000, None
            )
        else:
            # 用户环境变量
            os.environ[name] = value
        
        return True
    except Exception as e:
        print(f"更新环境变量时出错: {e}")
        return False


def get_environment_variable(name):
    """获取环境变量值
    
    Args:
        name (str): 环境变量名称
    Returns:
        str: 环境变量值
    """
  
    # 获取系统环境变量
    import winreg
    try:
        with winreg.OpenKey(
            winreg.HKEY_LOCAL_MACHINE,
            r"SYSTEM\CurrentControlSet\Control\Session Manager\Environment"
        ) as key:
            value, _ = winreg.QueryValueEx(key, name)
            return value
    except Exception:
        return None


def add_to_path(path, is_system=False):
    """将路径添加到PATH环境变量
    
    Args:
        path (str): 要添加的路径
        is_system (bool): 是否更新系统PATH
    
    Returns:
        bool: 更新是否成功
    """
    current_path = get_environment_variable("PATH", is_system)
    if current_path:
        # 检查路径是否已存在
        paths = current_path.split(';')
        if path not in paths:
            new_path = f"{path};{current_path}"
            return update_environment_variable("PATH", new_path)
        return True
    else:
        return update_environment_variable("PATH", path)
