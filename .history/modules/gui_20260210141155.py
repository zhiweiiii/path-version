#!/usr/bin/env python3
"""GUI界面模块"""

import tkinter as tk
from tkinter import ttk, messagebox
from modules.env_manager import switch_software_version


def create_gui(software_versions):
    """创建GUI界面
    
    Args:
        software_versions (dict): 软件版本信息
    """
    # 创建主窗口
    root = tk.Tk()
    root.title("版本切换工具")
    root.geometry("600x500")
    root.resizable(True, True)
    
    # 设置图标（可选）
    # root.iconbitmap('icon.ico')
    
    # 配置全局样式
    style = ttk.Style()
    style.theme_use('clam')
    
    # 自定义样式
    style.configure('Main.TFrame', background='#f0f0f0')
    style.configure('Header.TLabel', font=('微软雅黑', 18, 'bold'), foreground='#333333', background='#f0f0f0')
    style.configure('SubHeader.TLabel', font=('微软雅黑', 12, 'bold'), foreground='#555555', background='#ffffff')
    style.configure('Accent.TButton', font=('微软雅黑', 10, 'bold'), foreground='#ffffff', background='#4CAF50')
    style.map('Accent.TButton', background=[('active', '#45a049')])
    style.configure('Standard.TButton', font=('微软雅黑', 10), foreground='#333333', background='#e0e0e0')
    style.map('Standard.TButton', background=[('active', '#d0d0d0')])
    style.configure('Card.TFrame', background='#ffffff', relief='raised', borderwidth=1)
    
    # 创建主框架
    main_frame = ttk.Frame(root, padding="20", style='Main.TFrame')
    main_frame.pack(fill=tk.BOTH, expand=True)
    
    # 创建标题
    header_frame = ttk.Frame(main_frame, style='Main.TFrame')
    header_frame.pack(fill=tk.X, pady=(0, 30))
    
    title_label = ttk.Label(
        header