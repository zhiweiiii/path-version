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
    version_buttons_frame.pack(fill=tk.X, pady=(0, 20))
    
    version_buttons = {}
    
    def update_version_buttons():
        """更新版本选择按钮"""
        for widget in version_buttons_frame.winfo_children():
            widget.destroy()
        
        version_buttons.clear()
        
        current_software = selected_software.get()
        if not current_software or current_software not in software_versions:
            no_version_label = ttk.Label(
                version_buttons_frame, 
                text="请先选择软件", 
                font=('微软雅黑', 10), 
                foreground='#999999'
            )
            no_version_label.pack(anchor=tk.CENTER, pady=30)
            return
        
        versions = software_versions[current_software]
        if not versions:
            no_version_label = ttk.Label(
                version_buttons_frame, 
                text="未检测到版本", 
                font=('微软雅黑', 10), 
                foreground='#999999'
            )
            no_version_label.pack(anchor=tk.CENTER, pady=30)
            return
        
        version_title = ttk.Label(
            version_buttons_frame, 
            text="选择版本", 
            style='SubHeader.TLabel'
        )
        version_title.pack(anchor=tk.W, pady=(0, 15))
        
        # 版本列表框架
        version_list_frame = ttk.Frame(version_buttons_frame, style='Card.TFrame')
        version_list_frame.pack(fill=tk.BOTH, expand=True)
        
        # 创建版本按钮
        for version in versions.keys():
            # 获取路径
            path = versions[version]
            # 只显示路径的目录部分
            dir_path = path.rsplit('\\', 1)[0] if '\\' in path else path
            
            # 创建版本项框架
            version_item_frame = ttk.Frame(version_list_frame, style='Card.TFrame')
            version_item_frame.pack(fill=tk.X, padx=5, pady=5)
            
            # 版本单选按钮
            btn = ttk.Radiobutton(
                version_item_frame, 
                text=version, 
                variable=selected_version, 
                value=version,
                style='TRadiobutton'
            )
            btn.pack(anchor=tk.W, side=tk.LEFT, padx=5, pady=5)
            version_buttons[version] = btn
            
            # 路径显示
            path_label = ttk.Label(
                version_item_frame, 
                text=dir_path, 
                font=('Consolas', 9), 
                foreground='#666666',
                style='Card.TFrame'
            )
            path_label.pack(anchor=tk.W, side=tk.LEFT, padx=20, pady=5, fill=tk.X)
        
        # 默认选择第一个版本
        if versions:
            first_version = list(versions.keys())[0]
            selected_version.set(first_version)
    
    # 操作按钮框架
    button_frame = ttk.Frame(content_frame, style='Main.TFrame')
    button_frame.pack(fill=tk.X, pady=(0, 20))
    
    # 切换版本按钮
    def switch_version():
        """切换版本按钮点击事件"""
        software = selected_software.get()
        version = selected_version.get()
        
        if not software:
            messagebox.showwarning("警告", "请选择软件")
            return
        
        if not version:
            messagebox.showwarning("警告", "请选择版本")
            return
        
        # 获取对应版本的路径
        path = software_versions[software].get(version)
        if not path:
            messagebox.showerror("错误", "未找到对应版本的路径")
            return
        
        # 切换版本（默认更新用户环境变量）
        success = switch_software_version(
            software, 
            version, 
            path, 
            is_system=False
        )
        
        if success:
            messagebox.showinfo("成功", f"已成功切换{software}版本到 {version}")
        else:
            messagebox.showerror("失败", "切换版本失败")
    
    # 按钮容器
    buttons_container = ttk.Frame(button_frame, style='Main.TFrame')
    buttons_container.pack(anchor=tk.CENTER)
    
    switch_button = ttk.Button(
        buttons_container, 
        text="切换版本", 
        command=switch_version, 
        style="Accent.TButton",
        width=15
    )
    switch_button.pack(side=tk.LEFT, padx=15)
    
    # 刷新按钮
    def refresh_versions():
        """刷新版本列表按钮点击事件"""
        from modules.scanner import scan_software_versions
        
        try:
            # 重新扫描版本
            new_versions = scan_software_versions()
            
            # 更新全局变量
            nonlocal software_versions
            software_versions = new_versions
            
            # 重新创建软件按钮
            create_software_buttons()
            
            messagebox.showinfo("成功", "版本列表已刷新")
        except Exception as e:
            messagebox.showerror("错误", f"刷新版本列表失败: {e}")
    
    refresh_button = ttk.Button(
        buttons_container, 
        text="