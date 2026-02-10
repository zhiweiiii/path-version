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
        print(f"[日志] 管理员权限检查: {'✓ 已获取' if admin_status else '✗ 未获取'}")
        return admin_status
    except Exception as e:
        print(f"[日志] 管理员权限检查失败: {e}")
        return False

def update_environment_variable(name, value):
    """更新环境变量
    
    Args:
        name (str): 环境变量名称
        value (str): 环境变量值
    
    Returns:
        bool: 更新是否成功
    """
    print(f"[日志] 开始更新环境变量: {name}")
    print(f"[日志] 新值: {value[:100]}..." if len(value) > 100 else f"[日志] 新值: {value}")
    
    try:
        # 使用winreg直接修改注册表中的系统环境变量
        print("[日志] 导入winreg模块")
        import winreg
        
        print("[日志] 尝试打开系统环境变量注册表项")
        # 打开系统环境变量注册表项
        with winreg.OpenKey(
            winreg.HKEY_LOCAL_MACHINE,
            r"SYSTEM\CurrentControlSet\Control\Session Manager\Environment",
            0,
            winreg.KEY_SET_VALUE | winreg.KEY_WOW64_64KEY
        ) as key:
            print("[日志] 成功打开注册表项")
            print("[日志] 尝试设置环境变量值")
            # 设置环境变量值
            winreg.SetValueEx(key, name, 0, winreg.REG_EXPAND_SZ, value)
            print("[日志] 环境变量值设置成功")
        
        print("[日志] 开始广播环境变量变更")
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
        print("[日志] 环境变量变更广播完成")
        
        print(f"[日志] 环境变量更新成功: {name}")
        return True
    except PermissionError as e:
        print(f"[错误] 更新环境变量时权限不足: {e}")
        print("[提示] 请以管理员身份运行程序")
        return False
    except Exception as e:
        print(f"[错误] 更新环境变量时出错: {e}")
        import traceback
        traceback.print_exc()
        return False


def get_environment_variable(name):
    """获取环境变量值
    
    Args:
        name (str): 环境变量名称
    
    Returns:
        str: 环境变量值
    """
    print(f"[日志] 开始获取环境变量: {name}")
    
    # 获取系统环境变量
    try:
        print("[日志] 导入winreg模块")
        import winreg
        
        print("[日志] 尝试打开系统环境变量注册表项")
        with winreg.OpenKey(
            winreg.HKEY_LOCAL_MACHINE,
            r"SYSTEM\CurrentControlSet\Control\Session Manager\Environment"
        ) as key:
            print("[日志] 成功打开注册表项")
            print("[日志] 尝试读取环境变量值")
            value, _ = winreg.QueryValueEx(key, name)
            print(f"[日志] 成功获取环境变量值: {value[:100]}..." if len(value) > 100 else f"[日志] 成功获取环境变量值: {value}")
            return value
    except Exception as e:
        print(f"[错误] 获取环境变量时出错: {e}")
        return None


def add_to_path(path):
    """将路径添加到PATH环境变量
    
    Args:
        path (str): 要添加的路径
    
    Returns:
        bool: 更新是否成功
    """
    print(f"[日志] 开始添加路径到PATH: {path}")
    
    # 检查是否以管理员身份运行
    if not is_admin():
        print("[错误] 没有管理员权限，无法修改系统环境变量！")
        print("[提示] 请以管理员身份运行程序")
        return False
    
    print("[日志] 尝试获取当前PATH环境变量")
    current_path = get_environment_variable("PATH")
    
    if current_path:
        print(f"[日志] 当前PATH长度: {len(current_path)}")
        # 检查路径是否已存在
        paths = current_path.split(';')
        if path in paths:
            print("[日志] 路径已存在于PATH中，无需添加")
            return True
        else:
            print("[日志] 路径不存在于PATH中，准备添加")
            new_path = f"{path};{current_path}"
            print("[日志] 准备更新PATH环境变量")
            success = update_environment_variable("PATH", new_path)
            print(f"[日志] PATH更新结果: {'✓ 成功' if success else '✗ 失败'}")
            return success
    else:
        print("[日志] 当前PATH为空，准备创建")
        success = update_environment_variable("PATH", path)
        print(f"[日志] PATH创建结果: {'✓ 成功' if success else '✗ 失败'}")
        return success
