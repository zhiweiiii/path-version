#!/usr/bin/env python3
"""测试注册表写入功能"""

import winreg
import ctypes
from ctypes import wintypes


def test_registry_write():
    """测试注册表写入功能"""
    print("测试注册表写入功能...")
    
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
    input()
    
