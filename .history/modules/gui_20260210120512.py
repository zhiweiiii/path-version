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
    
    # 创建主框架
    main_frame = ttk.Frame(root, padding="20")
    main_frame.pack(fill=tk.BOTH, expand=True)
    
    # 创建标题
    title_label = ttk.Label(
        main_frame, 
        text="版本切换工具", 
        font=("微软雅黑", 16, "bold")
    )
    title_label.pack(pady=(0, 20))
    
    # 创建软件选择框架
    software_frame = ttk.LabelFrame(main_frame, text="选择软件", padding="10")
    software_frame.pack(fill=tk.X, pady=(0, 15))
    
    # 软件下拉菜单
    software_var = tk.StringVar()
    software_label = ttk.Label(software_frame, text="软件:")
    software_label.grid(row=0, column=0, padx=5, pady=5, sticky=tk.W)
    
    software_combobox = ttk.Combobox(
        software_frame, 
        textvariable=software_var, 
        state="readonly"
    )
    software_combobox['values'] = list(software_versions.keys())
    software_combobox.grid(row=0, column=1, padx=5, pady=5, sticky=tk.W+tk.E)
    
    # 版本下拉菜单
    version_var = tk.StringVar()
    version_label = ttk.Label(software_frame, text="版本:")
    version_label.grid(row=1, column=0, padx=5, pady=5, sticky=tk.W)
    
    version_combobox = ttk.Combobox(
        software_frame, 
        textvariable=version_var, 
        state="readonly"
    )
    version_combobox.grid(row=1, column=1, padx=5, pady=5, sticky=tk.W+tk.E)
    
    # 系统环境变量选项
    system_var = tk.BooleanVar()
    system_checkbutton = ttk.Checkbutton(
        software_frame, 
        text="更新系统环境变量（需要管理员权限）", 
        variable=system_var
    )
    system_checkbutton.grid(row=2, column=0, columnspan=2, padx=5, pady=5, sticky=tk.W)
    
    # 绑定软件选择事件
    def on_software_change(event):
        """软件选择变化时更新版本列表"""
        selected_software = software_var.get()
        if selected_software in software_versions:
            versions = list(software_versions[selected_software].keys())
            version_combobox['values'] = versions
            if versions:
                version_var.set(versions[0])
            else:
                version_var.set("")
        else:
            version_combobox['values'] = []
            version_var.set("")
    
    software_combobox.bind("<<ComboboxSelected>>", on_software_change)
    
    # 初始化第一个软件的版本列表
    if software_versions:
        first_software = list(software_versions.keys())[0]
        software_var.set(first_software)
        versions = list(software_versions[first_software].keys())
        version_combobox['values'] = versions
        if versions:
            version_var.set(versions[0])
    
    # 创建操作按钮框架
    button_frame = ttk.Frame(main_frame)
    button_frame.pack(pady=15)
    
    # 切换版本按钮
    def switch_version():
        """切换版本按钮点击事件"""
        selected_software = software_var.get()
        selected_version = version_var.get()
        is_system = system_var.get()
        
        if not selected_software:
            messagebox.showwarning("警告", "请选择软件")
            return
        
        if not selected_version:
            messagebox.showwarning("警告", "请选择版本")
            return
        
        # 获取对应版本的路径
        path = software_versions[selected_software].get(selected_version)
        if not path:
            messagebox.showerror("错误", "未找到对应版本的路径")
            return
        
        # 切换版本
        success = switch_software_version(
            selected_software, 
            selected_version, 
            path, 
            is_system
        )
        
        if success:
            messagebox.showinfo("成功", f"已成功切换{selected_software}版本到 {selected_version}")
        else:
            messagebox.showerror("失败", "切换版本失败")
    
    switch_button = ttk.Button(
        button_frame, 
        text="切换版本", 
        command=switch_version, 
        style="Accent.TButton"
    )
    switch_button.pack(side=tk.LEFT, padx=10)
    
    # 刷新按钮
    def refresh_versions():
        """刷新版本列表按钮点击事件"""
        from modules.scanner import scan_software_versions
        
        try:
            # 重新扫描版本
            new_versions = scan_software_versions()
            
            # 更新软件下拉菜单
            software_combobox['values'] = list(new_versions.keys())
            
            # 更新全局变量
            nonlocal software_versions
            software_versions = new_versions
            
            # 重新初始化
            if software_versions:
                first_software = list(software_versions.keys())[0]
                software_var.set(first_software)
                versions = list(software_versions[first_software].keys())
                version_combobox['values'] = versions
                if versions:
                    version_var.set(versions[0])
            
            messagebox.showinfo("成功", "版本列表已刷新")
        except Exception as e:
            messagebox.showerror("错误", f"刷新版本列表失败: {e}")
    
    refresh_button = ttk.Button(
        button_frame, 
        text="刷新版本", 
        command=refresh_versions
    )
    refresh_button.pack(side=tk.LEFT, padx=10)
    
    # 创建版本信息框架
    info_frame = ttk.LabelFrame(main_frame, text="版本信息", padding="10")
    info_frame.pack(fill=tk.BOTH, expand=True, pady=(0, 15))
    
    # 创建文本框显示版本信息
    info_text = tk.Text(info_frame, wrap=tk.WORD, height=10)
    info_text.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
    
    # 添加滚动条
    scrollbar = ttk.Scrollbar(info_text, command=info_text.yview)
    scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
    info_text.config(yscrollcommand=scrollbar.set)
    
    # 填充版本信息
    def fill_info_text():
        """填充版本信息到文本框"""
        info_text.delete(1.0, tk.END)
        
        if not software_versions:
            info_text.insert(tk.END, "未检测到任何软件版本")
            return
        
        for software, versions in software_versions.items():
            info_text.insert(tk.END, f"{software}:\n")
            if versions:
                for version, path in versions.items():
                    info_text.insert(tk.END, f"  - {version}: {path}\n")
            else:
                info_text.insert(tk.END, "  - 未检测到版本\n")
            info_text.insert(tk.END, "\n")
    
    fill_info_text()
    
    # 绑定刷新按钮事件
    def on_refresh_button():
        """刷新按钮点击事件"""
        refresh_versions()
        fill_info_text()
    
    # 更新刷新按钮的命令
    refresh_button.config(command=on_refresh_button)
    
    # 创建状态栏
    status_frame = ttk.Frame(root)
    status_frame.pack(fill=tk.X, side=tk.BOTTOM)
    
    status_label = ttk.Label(
        status_frame, 
        text="就绪", 
        relief=tk.SUNKEN, 
        anchor=tk.W
    )
    status_label.pack(fill=tk.X, padx=5, pady=5)
    
    # 配置样式
    style = ttk.Style()
    style.configure("Accent.TButton", foreground="black", background="#4CAF50")
    
    # 启动主循环
    root.mainloop()
