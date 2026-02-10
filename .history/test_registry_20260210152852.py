import winreg
import ctypes
import os
import sys

def is_admin():
    try:
        return ctypes.windll.shell32.IsUserAnAdmin()
    except:
        return False

def run_as_admin():
    script = os.path.abspath(sys.argv[0])
    params = ' '.join(sys.argv[1:])
    # 关键：确保 shell 为 True 或者直接调用解释器
    ret = ctypes.windll.shell32.ShellExecuteW(
        None, "runas", sys.executable, f'"{script}" {params}', None, 1
    )
    if int(ret) <= 32:
        print("用户拒绝了权限请求。")
        sys.exit(1)
    else:
        sys.exit(0)

def test_registry_write_permanent():
    """真正的写入测试：创建一个测试变量"""
    print("--- 开始注册表写入测试 ---")
    
    if not is_admin():
        print("当前不是管理员，准备提权...")
        run_as_admin()
        return

    reg_path = r"SYSTEM\CurrentControlSet\Control\Session Manager\Environment"
    test_key_name = "PYTHON_WRITE_TEST"
    test_value = "Success_At_2026"

    try:
        # 核心：使用 KEY_ALL_ACCESS 或至少 KEY_SET_VALUE | KEY_READ
        # 同时必须包含 KEY_WOW64_64KEY 确保在 64 位系统上访问正确的路径
        access_mask = winreg.KEY_ALL_ACCESS | winreg.KEY_WOW64_64KEY
        
        print(f"尝试打开注册表进行写入: {reg_path}")
        with winreg.OpenKey(winreg.HKEY_LOCAL_MACHINE, reg_path, 0, access_mask) as key:
            
            # 执行写入操作
            winreg.SetValueEx(key, test_key_name, 0, winreg.REG_SZ, test_value)
            print(f"写入成功！创建了变量: {test_key_name}")

            # 验证写入
            val, _ = winreg.QueryValueEx(key, test_key_name)
            print(f"验证读取新变量值: {val}")

        # 广播通知系统（非常重要，否则其他程序不知道变了）
        print("正在广播环境变更通知...")
        HWND_BROADCAST = 0xFFFF
        WM_SETTINGCHANGE = 0x001A
        result = ctypes.windll.user32.SendMessageTimeoutW(
            HWND_BROADCAST, WM_SETTINGCHANGE, 0, "Environment", 0x0002, 5000, None
        )
        print("广播完成！")
        print("\n[结果]：你现在可以在『系统属性-环境变量』中看到 PYTHON_WRITE_TEST 了。")

    except PermissionError:
        print("\n[失败]：权限不足！")
        print("即使是管理员，如果你的 Python 被杀毒软件（如火绒、360、Windows Defender）监控，")
        print("直接修改系统级注册表依然会被拦截。请尝试暂时关闭监控。")
    except Exception as e:
        print(f"\n[错误]：{e}")

if __name__ == "__main__":
    test_registry_write_permanent()
    print("\n按回车键退出测试...")
    input()