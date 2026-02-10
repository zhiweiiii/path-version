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
    root.geometry("900x600")
    root.resizable(True, True)
    
    # 设置图标（可选）
    # root.iconbitmap('icon.ico')
    
    # 配置全局样式
    style = ttk.Style()
    style.theme_use('clam')
    
    # 自定义样式
    style.configure('Main.TFrame', background='#f8f9fa')
    style.configure('Sidebar.TFrame', background='#ffffff', relief='raised', borderwidth=1)
    style.configure('Content.TFrame', background='#f8f9fa')
    style.configure('Header.TLabel', font=('微软雅黑', 16, 'bold'), foreground='#333333', background='#ffffff')
    style.configure('NavItem.TButton', font=('微软雅黑', 10), foreground='#666666', background='#ffffff', width=20)
    style.map('NavItem.TButton', background=[('active', '#f0f0f0'), ('selected', '#e3f2fd')], foreground=[('selected', '#1976d2')])
    style.configure('Accent.TButton', font=('微软雅黑', 9, 'bold'), foreground='#ffffff', background='#4CAF50')
    style.map('Accent.TButton', background=[('active', '#45a049')])
    style.configure('Table.Treeview', font=('微软雅黑', 10), rowheight=30)
    style.configure('Table.Treeview.Heading', font=('微软雅黑', 10, 'bold'), background='#e0e0e0', foreground='#333333')
    
    # 创建主框架
    main_frame = ttk.Frame(root, style='Main.TFrame')
    main_frame.pack(fill=tk.BOTH, expand=True)
    
    # 创建左侧导航栏
    sidebar_frame = ttk.Frame(main_frame, width=200, style='Sidebar.TFrame', borderwidth=0, relief='flat')
    sidebar_frame.pack(side=tk.LEFT, fill=tk.Y, padx=(0, 0))
    
    # 添加分类标题样式
    style.configure('Category.TLabel', font=('微软雅黑', 9, 'bold'), foreground='#999999', background='#ffffff')
    
    # 导航项
    nav_items = {
        'Languages': ['Python', 'Node.js', 'Java', 'Git'],
        'All': ['All']
    }
    
    # 当前选中的导航项
    current_nav = tk.StringVar(value='All')
    current_category = tk.StringVar(value='All')
    
    # 导航项点击事件
    def on_nav_click(category, item):
        """导航项点击事件"""
        current_category.set(category)
        current_nav.set(item)
        update_table(item)
    
    # 创建导航项
    for category, items in nav_items.items():
        # 分类标题
        category_label = ttk.Label(
            sidebar_frame, 
            text=category, 
            style='Category.TLabel'
        )
        category_label.pack(anchor=tk.W, padx=20, pady=(15, 5))
        
        # 分类项
        for item in items:
            nav_button = ttk.Button(
                sidebar_frame, 
                text=item, 
                style='NavItem.TButton',
                command=lambda c=category, i=item: on_nav_click(c, i)
            )
            nav_button.pack(anchor=tk.W, padx=20, pady=2)
    
    # 创建右侧内容区域
    content_frame = ttk.Frame(main_frame, style='Content.TFrame')
    content_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True, padx=(0, 0))
    
    # 添加新样式
    style.configure('TableContainer.TFrame', background='#ffffff', relief='flat', borderwidth=0)
    
    # 创建表格
    table_frame = ttk.Frame(content_frame, style='TableContainer.TFrame')
    table_frame.pack(fill=tk.BOTH, expand=True, padx=0, pady=0)
    
    # 表格列
    columns = ('package', 'version', 'status', 'action')
    
    # 创建树状表格
    tree = ttk.Treeview(
        table_frame, 
        columns=columns, 
        show='headings',
        style='Table.Treeview'
    )
    
    # 配置列
    tree.heading('package', text='软件名称')
    tree.heading('version', text='版本')
    tree.heading('status', text='状态')
    tree.heading('action', text='操作')
    
    # 配置列宽
    tree.column('package', width=150, anchor=tk.W)
    tree.column('version', width=100, anchor=tk.CENTER)
    tree.column('status', width=100, anchor=tk.CENTER)
    tree.column('action', width=100, anchor=tk.CENTER)
    
    # 添加滚动条
    scrollbar = ttk.Scrollbar(table_frame, orient=tk.VERTICAL, command=tree.yview)
    tree.configure(yscroll=scrollbar.set)
    scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
    
    tree.pack(fill=tk.BOTH, expand=True)
    
    # 存储版本路径映射
    version_paths = {}
    # 存储当前启用的版本
    enabled_versions = {}
    
    # 更新表格数据
    def update_table(filter_item):
        """更新表格数据"""
        # 清空表格
        for item in tree.get_children():
            tree.delete(item)
        
        # 清空版本路径映射
        version_paths.clear()
        
        # 填充数据
        for software, versions in software_versions.items():
            # 过滤
            if filter_item != 'All' and software != filter_item:
                continue
            
            for version, path in versions.items():
                # 获取路径的目录部分
                dir_path = path.rsplit('\\', 1)[0] if '\\' in path else path
                # 合并软件名称和安装目录
                package_name = f"{software}\n{dir_path}"
                
                # 检查是否已启用
                status = '已启用' if enabled_versions.get(software) == version else '未启用'
                
                # 生成唯一键
                key = f"{software}_{version}"
                version_paths[key] = (software, version, path)
                
                # 添加到表格
                item_id = tree.insert('', tk.END, values=(
                    package_name, 
                    version, 
                    status, 
                    '激活'
                ))
                # 存储键到item_id
                tree.set(item_id, 'action', key)
    
    # 激活版本
    def activate_version(software, version, path):
        """激活版本"""
        # 切换版本
        success = switch_software_version(
            software, 
            version, 
            path, 
            is_system=False
        )
        
        if success:
            messagebox.showinfo("成功", f"已成功激活{software} {version}")
            # 更新表格
            update_table(current_nav.get())
        else:
            messagebox.showerror("失败", "激活版本失败")
    
    # 表格双击事件处理
    def on_tree_double_click(event):
        """表格双击事件处理"""
        # 获取点击的列
        region = tree.identify_region(event.x, event.y)
        if region == "cell":
            # 获取点击的项和列
            item_id = tree.identify_row(event.y)
            column = tree.identify_column(event.x)
            
            # 检查是否点击了action列
            if column == '#5':  # action列的索引
                # 获取键
                key = tree.set(item_id, 'action')
                if key in version_paths:
                    software, version, path = version_paths[key]
                    activate_version(software, version, path)
    
    # 绑定双击事件
    tree.bind('<Double-1>', on_tree_double_click)
    
    # 刷新按钮
    refresh_frame = ttk.Frame(content_frame)
    refresh_frame.pack(side=tk.TOP, anchor=tk.E, padx=20, pady=10)
    
    def refresh_versions():
        """刷新版本列表"""
        from modules.scanner import scan_software_versions
        
        try:
            # 重新扫描版本
            new_versions = scan_software_versions()
            
            # 更新全局变量
            nonlocal software_versions
            software_versions = new_versions
            
            # 更新表格
            update_table(current_nav.get())
            
            messagebox.showinfo("成功", "版本列表已刷新")
        except Exception as e:
            messagebox.showerror("错误", f"刷新版本列表失败: {e}")
    
    refresh_button = ttk.Button(
        refresh_frame, 
        text="刷新", 
        style='Accent.TButton',
        command=refresh_versions
    )
    refresh_button.pack(side=tk.RIGHT)
    
    # 初始化表格
    update_table('All')
    
    # 启动主循环
    root.mainloop()
