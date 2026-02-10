import winreg
import ctypes
from ctypes import wintypes

def update_environment_variable(name, value):
    """
    永久更新系统环境变量（需要管理员权限运行 Python）
    """
    try:
        # 1. 直接写入注册表 (HKEY_LOCAL_MACHINE)
        # 注意：如果是用户变量，改用 HKEY_CURRENT_USER
        reg_path = r"SYSTEM\CurrentControlSet\Control\Session Manager\Environment"
        
        with winreg.OpenKey(winreg.HKEY_LOCAL_MACHINE, reg_path, 0, winreg.KEY_ALL_ACCESS) as key:
            winreg.SetValueEx(key, name, 0, winreg.REG_EXPAND_SZ, value)

        # 2. 广播通知系统（让其他程序如 CMD 知道环境变量变了，无需重启电脑）
        SendMessageTimeout = ctypes.WinDLL('user32').SendMessageTimeoutW
        HWND_BROADCAST = 0xFFFF
        WM_SETTINGCHANGE = 0x001A
        
        # 必须传递 "Environment" 字符串指针，通知系统是环境变量发生了改变
        SendMessageTimeout(
            HWND_BROADCAST, WM_SETTINGCHANGE, 0, "Environment",
            0x0002, 5000, None
        )
        return True
    except PermissionError:
        print("错误：请以管理员身份运行此脚本！")
        return False
    except Exception as e:
        print(f"更新失败: {e}")
        return False

# 对应的 get 函数也建议统一使用 winreg
def get_system_env(name):
    try:
        reg_path = r"SYSTEM\CurrentControlSet\Control\Session Manager\Environment"
        with winreg.OpenKey(winreg.HKEY_LOCAL_MACHINE, reg_path, 0, winreg.KEY_READ) as key:
            value, _ = winreg.QueryValueEx(key, name)
            return value
    except FileNotFoundError:
        return None
