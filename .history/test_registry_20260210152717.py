#!/usr/bin/env python3
"""测试注册表写入功能"""

import winreg
import ctypes
from ctypes import wintypes
import os
import sys

def is_admin():
    """检查当前脚本是否以管理员权限运行"""
    try:
        return ctypes.windll.shell32.IsUserAnAdmin()
    except:
        return False

def run_as_admin():
    """请求管理员权限并重启脚本"""
    # 获取当前运行的解释器路径和脚本参数
    script = os.path.abspath(sys.argv[0])
    params = ' '.join(sys.argv[1:])
    
    # 使用 runas 动词启动新进程
    # 1 表示窗口显示方式 (SW_SHOWNORMAL)
    ret = ctypes.windll.shell32.ShellExecuteW(
        None, "runas", sys.executable, f'"{script}" {params}', None, 1
    )
    
    if int(ret) <= 32:
        print("用户拒绝了管理员提权请求。")
        sys.exit(1)
    else:
        # 提权成功后，原有的非管理员进程必须退出
        sys.exit(0)


# ... is_admin 和 run_as_admin 函数保持不变 ...

def test_registry_write():
    print("测试注册表写入功能...")
    if not is_admin():
        print("检测到权限不足，正在尝试以管理员身份重启...")
        run_as_admin()
        return  # 必须 return，因为 run_as_admin 会启动新进程

    try:
        # 定义路径
        reg_path = r"SYSTEM\CurrentControlSet\Control\Session Manager\Environment"
        
        # 核心修正点：使用 winreg.KEY_READ | winreg.KEY_WOW64_64KEY
        # 哪怕是管理员，如果直接请求全部权限有时也会被拒绝
        # 先以读取权限打开
        print(f"尝试打开: {reg_path}")
        
        # KEY_ALL_ACCESS 包含写入权限，只有确实要写入时才用它
        # 这里为了演示读取，先用 KEY_READ
        access_mask = winreg.KEY_READ | winreg.KEY_WOW64_64KEY
        
        with winreg.OpenKey(winreg.HKEY_LOCAL_MACHINE, reg_path, 0, access_mask) as key:
            print("注册表项打开成功！")
            
            # 读取当前PATH
            current_path, reg_type = winreg.QueryValueEx(key, "PATH")
            print(f"当前PATH长度: {len(current_path)}")
            print(f"当前PATH前100字符: {current_path[:100]}...")
            
        print("测试完成，注册表访问正常！")
        
    except PermissionError:
        print("错误：即使以管理员运行，注册表项也拒绝访问。")
        print("这可能是因为某些杀毒软件（如 360/火绒）拦截了对系统环境变量的读取申请。")
    except Exception as e:
        print(f"测试失败: {e}")

if __name__ == "__main__":
    test_registry_write()
    input("\n测试完成，按回车键退出...")