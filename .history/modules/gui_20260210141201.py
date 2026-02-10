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
        header_frame, 
        text="版本切换工具", 
        style='Header.TLabel'
    )
    title_label.pack(anchor=tk.CENTER)
    
    # 创建内容区域
    content_frame = ttk.Frame(main_frame, style='Main.TFrame')
    content_frame.pack(fill=tk.BOTH, expand=True)
    
    # 软件选择卡片
    software_card = ttk.Frame(content_frame, padding="30", style='Card.TFrame')
    software_card.pack(fill=tk.X, pady=(0, 20))
    
    software_title = ttk.Label(
        software_card, 
        text="选择软件", 
        style='SubHeader.TLabel'
    )
    software_title.pack(anchor=tk.W, pady=(0, 20))
    
    # 软件选择变量
    selected_software = tk.StringVar()
    selected_version = tk.StringVar()
    
    # 软件按钮组
    software_buttons_frame = ttk.Frame(software_card, style='Card.TFrame')
    software_buttons_frame.pack(fill=tk.X, pady=(0, 20))
    
    software_buttons = {}
    
    # 创建软件按钮
    def create_software_buttons():
        """创建软件选择按钮"""
        for widget in software_buttons_frame.winfo_children():
            widget.destroy()
        
        software_buttons.clear()
        
        if not software_versions:
            no_software_label = ttk.Label(
                software_buttons_frame, 
                text="未检测到软件", 
                font=('微软雅黑', 10), 
                foreground='#999999'
            )
            no_software_label.pack(anchor=tk.CENTER, pady=30)
            return
        
        for software in software_versions.keys():
            btn = ttk.Radiobutton(
                software_buttons_frame, 
                text=software, 
                variable=selected_software, 
                value=software, 
                command=update_version_buttons,
                style='TRadiobutton'
            )
            btn.pack(fill=tk.X, padx=5, pady=8)
            software_buttons[software] = btn
        
        # 默认选择第一个软件
        if software_versions:
            first_software = list(software_versions.keys())[0]
            selected_software.set(first_software)
            update_version_buttons()
    
    # 版本按钮组
    version_buttons_frame = ttk.Frame(software_card, style='Card.TFrame')
    version_buttons_frame.pack(fill=tk.X, pady=(0,