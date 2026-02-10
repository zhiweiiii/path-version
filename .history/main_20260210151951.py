#!/usr/bin/env python3
"""版本切换工具主脚本"""

import os
import sys
from modules.scanner import scan_software_versions
from modules.gui import create_gui


def main():
    """主函数"""
    # 检查是否为管理员
if not os.getuid() == 0:
    # 重新启动脚本作为管理员
    print("需要管理员权限，重启脚本...")
    os.execl(sys.executable, sys.executable, *sys.argv)
    # 扫描系统中的软件版本
    software_versions = scan_software_versions()
    
    # 启动GUI界面
    create_gui(software_versions)


if __name__ == "__main__":
    main()
