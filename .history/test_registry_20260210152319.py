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


def test_registry_write():
    """测试注册表写入功能"""
    print("测试注册表写入功能...")
    # 检查是否为管理员
    

    try:
        # 打开系统环境变量注册表项
        print("打开注册表项...")
        key = winreg.OpenKey(
            winreg.HKEY_LOCAL_MACHINE,
            r"SYSTEM\CurrentControlSet\Control\Session Manager\Environment",
            0,
            winreg.KEY_SET_VALUE | winreg.KEY_WOW64_64KEY
        )
        
        print("注册表项打开成功！")
        
        # 读取当前PATH
        current_path, _ = winreg.QueryValueEx(key, "PATH")
        print(f"当前PATH长度: {len(current_path)}")
        print(f"当前PATH前100字符: {current_path[:100]}...")
        
        # 关闭键
        key.Close()
        print("测试完成，注册表访问正常！")
        
    except Exception as e:
        print(f"测试失败: {e}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    test_registry_write()
    print("\n测试完成，按任意键退出...")
    while True:
        input()
    
