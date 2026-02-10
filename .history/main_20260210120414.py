#!/usr/bin/env python3
"""版本切换工具主脚本"""

import os
import sys
from modules.scanner import scan_software_versions
from modules.env_manager import update_environment_variable
from modules.gui import create_gui


def main():
    """主函数"""
    print("=== 版本切换工具 ===")
    
    # 扫描系统中的软件版本
    print("正在扫描系统中的软件版本...")
    software_versions = scan_software_versions()
    
    print("\n已检测到的软件版本:")
    for software, versions in software_versions.items():
        print(f"{software}:")
        for version, path in versions.items():
            print(f"  - {version}: {path}")
    
    # 启动GUI界面
    create_gui(software_versions)


if __name__ == "__main__":
    main()
