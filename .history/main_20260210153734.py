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
        admin_status = ctypes.windll.shell32.IsUserAnAdmin() != 0
        print(f"[日志] 管理员权限检查: {'✓ 已获取' if admin_status else '✗ 未获取'}")
        return admin_status
    except Exception as e:
        print(f"[日志] 管理员权限检查失败: {e}")
        return False

def run_as_admin():
    """以管理员身份重新运行程序"""
    print("[日志] 开始以管理员身份重新运行程序")
    
    script = os.path.abspath(sys.argv[0])
    params = ' '.join(sys.argv[1:])
    print(f"[日志] 脚本路径: {script}")
    print(f"[日志] 命令行参数: {params}")
    
    try:
        # 关键：确保使用正确的参数调用
        ret = ctypes.windll.shell32.ShellExecuteW(
            None, "runas", sys.executable, f'"{script}" {params}', None, 1
        )
        
        print(f"[日志] ShellExecuteW 返回值: {ret}")
        
        if int(ret) <= 32:
            print("[错误] 用户拒绝了权限请求。")
            return False
        else:
            print("[日志] 管理员权限请求已发送")
            return True
    except Exception as e:
        print(f"[错误] 以管理员身份运行失败: {e}")
        import traceback
        traceback.print_exc()
        return False

def main():
    """主函数"""
    print("版本切换工具")
    print("=================")
    print()
    print("[日志] 程序启动")
    print(f"[日志] Python版本: {sys.version}")
    print(f"[日志] 程序路径: {os.path.abspath(__file__)}")
    print(f"[日志] 当前工作目录: {os.getcwd()}")
    print()
    
    # 检查是否以管理员身份运行
    print("[日志] 检查管理员权限...")
    if not is_admin():
        print("[提示] 需要管理员权限来修改系统环境变量")
        print("[提示] 正在请求管理员权限...")
        print()
        
        # 以管理员身份重新运行
        if not run_as_admin():
            print("[错误] 无法获取管理员权限，程序将退出")
            input("[提示] 按任意键退出...")
            return
        
        # 退出当前进程
        print("[日志] 已启动管理员权限请求，当前进程退出")
        return
    
    print("[日志] 管理员权限检查通过")
    print()
    
    # 扫描软件版本
    print("[日志] 开始扫描已安装的软件版本...")
    try:
        software_versions = scan_software_versions()
        
        # 显示扫描结果
        print("[日志] 扫描完成！")
        print(f"[日志] 发现 {len(software_versions)} 个软件：")
        for software, versions in software_versions.items():
            print(f"[日志] - {software}: {len(versions)} 个版本")
            for version, path in versions.items():
                print(f"[日志]   - {version}: {path}")
        print()
        
        # 创建GUI
        print("[日志] 开始创建GUI界面...")
        create_gui(software_versions)
        print("[日志] GUI界面创建完成")
    except Exception as e:
        print(f"[错误] 程序运行失败: {e}")
        import traceback
        traceback.print_exc()
        input("[提示] 按任意键退出...")


if __name__ == "__main__":
    main()
