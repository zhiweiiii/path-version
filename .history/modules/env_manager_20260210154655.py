#!/usr/bin/env python3
"""环境变量管理模块"""

import os
import sys
import ctypes
from ctypes import wintypes


def is_admin():
    """检查是否以管理员身份运行"""
    try:
        admin_status = ctypes.windll.shell32.IsUserAnAdmin() != 0
        print(f"管理员权限: {'✓ 已获取' if admin_status else '✗ 未获取'}")
        return admin_status
    except Exception as e:
        print(f"管理员权限检查失败: {e}")
        return False

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
    try:
        import winreg
        
        with winreg.OpenKey(
            winreg.HKEY_LOCAL_MACHINE,
            r"SYSTEM\CurrentControlSet\Control\Session Manager\Environment"
        ) as key:
            value, _ = winreg.QueryValueEx(key, name)
            return value
    except Exception as e:
        print(f"获取环境变量时出错: {e}")
        return None


def add_to_path(path):
    """将路径添加到PATH环境变量
    
    Args:
        path (str): 要添加的路径
    
    Returns:
        bool: 更新是否成功
    """
    # 检查是否以管理员身份运行
    if not is_admin():
        print("没有管理员权限，无法修改系统环境变量！")
        print("请以管理员身份运行程序")
        return False
    
    current_path = get_environment_variable("PATH")
    
    if current_path:
        # 检查路径是否已存在
        paths = current_path.split(';')
        
        # 清理空路径
        paths = [p for p in paths if p.strip()]
        
        if path in paths:
            print(f"路径已存在于PATH中: {path}")
            
            # 检查是否已经在第一个位置
            if paths[0] == path:
                print("路径已经在第一个位置，无需操作")
                return True
            else:
                print("路径不在第一个位置，移动到最前面")
                # 移除路径
                paths.remove(path)
                # 添加到最前面
                paths.insert(0, path)
                # 重新构建PATH
                new_path = ';'.join(paths)
                # 更新环境变量
                success = update_environment_variable("PATH", new_path)
                if success:
                    print("PATH更新成功")
                return success
        else:
            print(f"路径不存在于PATH中，添加到最前面: {path}")
            # 添加到最前面
            new_path = f"{path};{current_path}"
            # 更新环境变量
            success = update_environment_variable("PATH", new_path)
            if success:
                print("PATH更新成功")
            return success
    else:
        print(f"当前PATH为空，创建新的PATH: {path}")
        success = update_environment_variable("PATH", path)
        if success:
            print("PATH创建成功")
        return success
