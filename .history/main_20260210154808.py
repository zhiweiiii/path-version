#!/usr/bin/env python3
"""版本切换工具主程序"""

import os
import sys
import ctypes
from modules.scanner import scan_software_versions
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
        
        if int(ret) <= 32:
            print("用户拒绝了权限请求。")
            return False
        else:
            return True
    except Exception as e:
        print(f"以管理员身份运行失败: {e}")
        return False

def main():
    """主函数"""
    print("版本切换工具")
    print("=================")
    print()
    
    # 检查是否以管理员身份运行
    if not is_admin():
        print("需要管理员权限来修改系统环境变量")
        # 以管理员身份重新运行
        if not run_as_admin():
            print("无法获取管理员权限，程序将退出")
            input("按任意键退出...")
            return
        # 退出当前进程
        return
    
    print("管理员权限检查通过")
    print()
    
    # 扫描软件版本
    print("正在扫描已安装的软件版本...")
    try:
        software_versions = scan_software_versions()
        
        # 显示扫描结果
        print("扫描完成！")
        print(f"发现 {len(software_versions)} 个软件：")
        for software, versions in software_versions.items():
            print(f"- {software}: {len(versions)} 个版本")
        print()
        
        # 创建GUI
        print("正在启动GUI界面...")
        create_gui(software_versions)
    except Exception as e:
        print(f"程序运行失败: {e}")
        input("按任意键退出...")


if __name__ == "__main__":
    main()
