#!/usr/bin/env python3
"""版本切换工具主程序"""

import os
import sys
import ctypes
from modules.gui import create_gui


def is_admin():
    """检查是否以管理员身份运行"""
    try:
        return ctypes.windll.shell32.IsUserAnAdmin() != 0
    except:
        return False

def run_as_admin():
    """以管理员身份重新运行程序"""
    script = os.path.abspath(sys.argv[0])
    params = ' '.join(sys.argv[1:])
    
    try:
        # 关键：确保使用正确的参数调用
        ret = ctypes.windll.shell32.ShellExecuteW(
            None, "runas", sys.executable, f'"{script}" {params}', None, 1
        )
        
        return int(ret) > 32
    except:
        return False

def main():
    """主函数"""
    # 检查是否以管理员身份运行
    if not is_admin():
        # 以管理员身份重新运行
        if not run_as_admin():
            # 无法获取管理员权限，直接退出
            return
        # 退出当前进程
        return
    
    # 创建GUI
    try:
        create_gui()
    except:
        # 发生错误时直接退出，不显示控制台信息
        pass


if __name__ == "__main__":
    main()
