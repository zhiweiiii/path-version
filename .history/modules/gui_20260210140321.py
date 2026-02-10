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
    root.geometry("700x600")
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
    
    # 创建左侧软件选择卡片
    left_frame = ttk.Frame(content_frame, width=300, style='Main.TFrame')
    left_frame.pack(side=tk.LEFT, fill=tk.BOTH, padx=(0, 15))
    
    # 软件选择卡片
    software_card = ttk.Frame(left_frame, padding="20", style='Card.TFrame')
    software_card.pack(fill=tk.BOTH, pady=(0, 15))
    
    software_title = ttk.Label(
        software_card, 
        text="选择软件", 
        style='SubHeader.TLabel'
    )
    software_title.pack(anchor=tk.W, pady=(0, 15))
    
    # 软件选择变量
    selected_software = tk.StringVar()
    selected_version = tk.StringVar()
    system_var = tk.BooleanVar()
    
    # 软件按钮组
    software_buttons_frame = ttk.Frame(software_card, style='Card.TFrame')
    software_buttons_frame.pack(fill=tk.X, pady=(0, 15))
    
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
            no_software_label.pack(anchor=tk.CENTER, pady=20)
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
            btn.pack(fill=tk.X, padx=5, pady=5)
            software_buttons[software] = btn
        
        # 默认选择第一个软件
        if software_versions:
            first_software = list(software_versions.keys())[0]
            selected_software.set(first_software)
            update_version_buttons()
    
    # 版本按钮组
    version_buttons_frame = ttk.Frame(software_card, style='Card.TFrame')
    version_buttons_frame.pack(fill=tk.X, pady=(0, 15))
    
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
            no_version_label.pack(anchor=tk.CENTER, pady=20)
            return
        
        versions = software_versions[current_software]
        if not versions:
            no_version_label = ttk.Label(
                version_buttons_frame, 
                text="未检测到版本", 
                font=('微软雅黑', 10), 
                foreground='#999999'
            )
            no_version_label.pack(anchor=tk.CENTER, pady=20)
            return
        
        version_title = ttk.Label(
            version_buttons_frame, 
            text="选择版本", 
            style='SubHeader.TLabel'
        )
        version_title.pack(anchor=tk.W, pady=(0, 10))
        
        for version in versions.keys():
            btn = ttk.Radiobutton(
                version_buttons_frame, 
                text=version, 
                variable=selected_version, 
                value=version,
                style='TRadiobutton'
            )
            btn.pack(fill=tk.X, padx=5, pady=5)
            version_buttons[version] = btn
        
        # 默认选择第一个版本
        if versions:
            first_version = list(versions.keys())[0]
            selected_version.set(first_version)
    
    # 系统环境变量选项
    system_frame = ttk.Frame(software_card, style='Card.TFrame')
    system_frame.pack(fill=tk.X, pady=(0, 15))
    
    system_checkbutton = ttk.Checkbutton(
        system_frame, 
        text="更新系统环境变量（需要管理员权限）", 
        variable=system_var,
        style='TCheckbutton'
    )
    system_checkbutton.pack(anchor=tk.W, padx=5, pady=5)
    
    # 操作按钮
    button_frame = ttk.Frame(software_card, style='Card.TFrame')
    button_frame.pack(fill=tk.X)
    
    # 切换版本按钮
    def switch_version():
        """切换版本按钮点击事件"""
        software = selected_software.get()
        version = selected_version.get()
        is_system = system_var.get()
        
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
        
        # 切换版本
        success = switch_software_version(
            software, 
            version, 
            path, 
            is_system
        )
        
        if success:
            messagebox.showinfo("成功", f"已成功切换{software}版本到 {version}")
        else:
            messagebox.showerror("失败", "切换版本失败")
    
    switch_button = ttk.Button(
        button_frame, 
        text="切换版本", 
        command=switch_version, 
        style="Accent.TButton"
    )
    switch_button.pack(fill=tk.X, pady=(0, 10))
    
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
            
            # 更新版本信息
            update_version_info()
            
            messagebox.showinfo("成功", "版本列表已刷新")
        except Exception as e:
            messagebox.showerror("错误", f"刷新版本列表失败: {e}")
    
    refresh_button = ttk.Button(
        button_frame, 
        text="刷新版本", 
        command=refresh_versions, 
        style="Standard.TButton"
    )
    refresh_button.pack(fill=tk.X)
    
    # 创建右侧版本信息卡片
    right_frame = ttk.Frame(content_frame, style='Main.TFrame')
    right_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)
    
    # 版本信息卡片
    info_card = ttk.Frame(right_frame, padding="20", style='Card.TFrame')
    info_card.pack(fill=tk.BOTH, expand=True)
    
    info_title = ttk.Label(
        info_card, 
        text="版本信息", 
        style='SubHeader.TLabel'
    )
    info_title.pack(anchor=tk.W, pady=(0, 15))
    
    # 创建版本信息文本框
    info_text = tk.Text(
        info_card, 
        wrap=tk.WORD, 
        font=('Consolas', 10),
        bg='#f9f9f9',
        fg='#333333',
        borderwidth=1,
        relief='sunken'
    )
    info_text.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
    
    # 添加滚动条
    scrollbar = ttk.Scrollbar(info_text, command=info_text.yview)
    scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
    info_text.config(yscrollcommand=scrollbar.set)
    
    # 填充版本信息
    def update_version_info():
        """更新版本信息文本框"""
        info_text.delete(1.0, tk.END)
        
        if not software_versions:
            info_text.insert(tk.END, "未检测到任何软件版本\n")
            return
        
        for software, versions in software_versions.items():
            info_text.insert(tk.END, f"{software}:\n", 'software')
            if versions:
                for version, path in versions.items():
                    info_text.insert(tk.END, f"  版本: {version}\n", 'version')
                    info_text.insert(tk.END, f"  路径: {path}\n\n", 'path')
            else:
                info_text.insert(tk.END, "  未检测到版本\n\n", 'none')
    
    # 配置文本样式
    info_text.tag_configure('software', font=('微软雅黑', 10, 'bold'), foreground='#333333')
    info_text.tag_configure('version', font=('Consolas', 10), foreground='#4CAF50')
    info_text.tag_configure('path', font=('Consolas', 10), foreground='#666666')
    info_text.tag_configure('none', font=('Consolas', 10), foreground='#999999')
    
    # 创建状态栏
    status_frame = ttk.Frame(root, style='Main.TFrame')
    status_frame.pack(fill=tk.X, side=tk.BOTTOM)
    
    status_label = ttk.Label(
        status_frame, 
        text="就绪", 
        font=('微软雅黑', 9),
        foreground='#666666',
        relief=tk.FLAT, 
        anchor=tk.W,
        style='Main.TFrame'
    )
    status_label.pack(fill=tk.X, padx=20, pady=10)
    
    # 初始化界面
    create_software_buttons()
    update_version_info()
    
    # 启动主循环
    root.mainloop()
