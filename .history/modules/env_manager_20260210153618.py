#!/usr/bin/env python3
"""环境变量管理模块"""

import os
import sys
import ctypes
from ctypes import wintypes

def update_environment_variable(name, value):
    """更新环境变量
    
    Args:
        name (str): 环境变量名称
        value (str): 环境变量值
    
    Returns:
        bool: 更新是否成功
    """
    try:
        # 使用winreg直接修改注册表中的系统环境变量
        import winreg
        
        # 打开系统环境变量注册表项
        with winreg.OpenKey(
            winreg.HKEY_LOCAL_MACHINE,
            r"SYSTEM\CurrentControlSet\Control\Session Manager\Environment",
            0,
            winreg.KEY_SET_VALUE | winreg.KEY_WOW64_64KEY
        ) as key:
            # 设置环境变量值
            winreg.SetValueEx(key, name, 0, winreg.REG_EXPAND_SZ, value)
        
        # 广播环境变量变更
        SendMessageTimeout = ctypes.WinDLL('user32').SendMessageTimeoutW
        SendMessageTimeout.argtypes = [
            wintypes.HWND, wintypes.UINT, wintypes.WPARAM, 
            wintypes.LPWSTR, wintypes.UINT, wintypes.UINT, ctypes.POINTER(wintypes.DWORD)]
        HWND_BROADCAST = 0xFFFF
        WM_SETTINGCHANGE = 0x001A
        SMTO_ABORTIFHUNG = 0x0002
        
        SendMessageTimeout(
            HWND_BROADCAST, WM_SETTINGCHANGE, 0, "Environment",
            SMTO_ABORTIFHUNG, 5000, None
        )
        
        return True
    except PermissionError as e:
        print(f"更新环境变量时权限不足: {e}")
        print("请以管理员身份运行程序")
        return False
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


def add_to_path(path):
    """将路径添加到PATH环境变量
    
    Args:
        path (str): 要添加的路径
    
    Returns:
        bool: 更新是否成功
    """
    current_path = get_environment_variable("PATH")

    if current_path:
        # 检查路径是否已存在
        paths = current_path.split(';')
        if path not in paths:
            new_path = f"{path};{current_path}"
            return update_environment_variable("PATH", new_path)
        return True
    else:
        return update_environment_variable("PATH", path)
