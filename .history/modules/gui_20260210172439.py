#!/usr/bin/env python3
"""GUI界面模块"""

import os
import tkinter as tk
import logging
from tkinter import ttk, messagebox
from modules.env_manager import add_to_path
from modules.scanner import scan_software_versions


# 配置日志
# 使用绝对路径确保日志文件能正确生成
print(f"日志文件路径: {log_file_path}")


# 全局变量存储
class AppData:
    """应用程序数据"""
    def __init__(self):
        # 存储版本路径映射
        self.version_paths = {}
        # 存储当前启用的版本
        self.enabled_versions = {}
        # 存储item_id到key的映射
        self.item_key_map = {}
        # 软件版本信息
        self.software_versions = {}
        # 当前选中的导航项
        self.current_nav = None
        self.current_category = None
        # UI组件
        self.root = None
        self.tree = None


# 全局应用数据实例
app_data = AppData()


def init_parameters():
    """初始化参数"""
    # 存储版本路径映射
    app_data.version_paths = {}
    # 存储当前启用的版本
    app_data.enabled_versions = {}
    # 存储item_id到key的映射
    app_data.item_key_map = {}
    # 软件版本信息
    app_data.software_versions = {}
    # 当前选中的导航项
    app_data.current_nav = tk.StringVar(value='All')
    app_data.current_category = tk.StringVar(value='All')


def init_ui(root):
    """初始化UI"""
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
    
    # 创建右侧内容区域
    content_frame = ttk.Frame(main_frame, style='Content.TFrame')
    content_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True, padx=(0, 0))
    
    # 添加新样式
    style.configure('TableContainer.TFrame', background='#ffffff', relief='flat', borderwidth=0)
    
    # 创建表格
    table_frame = ttk.Frame(content_frame, style='TableContainer.TFrame')
    table_frame.pack(fill=tk.BOTH, expand=True, padx=0, pady=0)
    
    # 表格列
    columns = ('package', 'version', 'status')
    
    # 创建树状表格
    tree = ttk.Treeview(
        table_frame, 
        columns=columns, 
        show='headings',
        style='Table.Treeview'
    )
    
    # 更新全局应用数据中的tree
    app_data.tree = tree
    
    # 配置列
    tree.heading('package', text='程序')
    tree.heading('version', text='版本')
    tree.heading('status', text='状态')
    
    # 配置列宽
    tree.column('package', width=350, anchor=tk.W)
    tree.column('version', width=100, anchor=tk.CENTER)
    tree.column('status', width=100, anchor=tk.CENTER)
    
    # 添加滚动条
    scrollbar = ttk.Scrollbar(table_frame, orient=tk.VERTICAL, command=tree.yview)
    tree.configure(yscroll=scrollbar.set)
    scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
    
    tree.pack(fill=tk.BOTH, expand=True)
    
    # 操作按钮框架
    button_frame = ttk.Frame(content_frame)
    button_frame.pack(side=tk.TOP, anchor=tk.E, padx=20, pady=10)
    
    return main_frame, sidebar_frame, content_frame, tree, button_frame, nav_items, style


def init_data(enabled_versions):
    """初始化数据"""
    enabled_versions.clear()
    
    # 扫描软件版本
    logger.debug("开始扫描软件版本")
    software_versions = scan_software_versions()
    logger.debug(f"扫描到的软件版本: {software_versions}")
    
    # 获取当前PATH环境变量
    current_path = os.environ.get('PATH', '')
    path_dirs = current_path.split(';')
    logger.debug(f"当前PATH环境变量: {current_path}")
    
    # 对于每个软件，检查其路径是否在PATH的最前面
    for software, versions in software_versions.items():
        logger.debug(f"检查软件: {software}")
        for version, path in versions.items():
            logger.debug(f"检查版本: {version}, 路径: {path}")
            # 获取可执行文件所在目录
            exe_dir = path.rsplit('\\', 1)[0] if '\\' in path else path
            logger.debug(f"可执行文件目录: {exe_dir}")
            # 检查该目录是否在PATH中
            for i, dir_path in enumerate(path_dirs):
                if dir_path.strip() == exe_dir.strip():
                    # 如果是第一个匹配的，设置为启用
                    if software not in enabled_versions:
                        enabled_versions[software] = version
                        logger.debug(f"设置软件 {software} 的启用版本为: {version}")
                    break
    
    logger.debug(f"最终的启用版本: {enabled_versions}")
    return software_versions


def on_nav_click(category, item):
    """导航项点击事件"""
    app_data.current_category.set(category)
    app_data.current_nav.set(item)
    update_table(item)


def init_enabled_status():
    """初始化启用状态"""
    app_data.software_versions = init_data(app_data.enabled_versions)


def update_table(filter_item):
    """更新表格数据"""
    logger.debug(f"开始更新表格，过滤项: {filter_item}")
    
    # 初始化启用状态
    init_enabled_status()
    
    # 清空表格
    logger.debug(f"清空表格，当前子项数量: {len(app_data.tree.get_children())}")
    for item in app_data.tree.get_children():
        app_data.tree.delete(item)
    
    # 清空映射
    app_data.version_paths.clear()
    app_data.item_key_map.clear()
    logger.debug(f"清空映射后，version_paths: {app_data.version_paths}, item_key_map: {app_data.item_key_map}")
    
    # 填充数据
    logger.debug(f"开始填充数据，software_versions: {app_data.software_versions}")
    for software, versions in app_data.software_versions.items():
        # 过滤
        if filter_item != 'All' and software != filter_item:
            logger.debug(f"跳过软件: {software}，因为过滤项为: {filter_item}")
            continue
        
        logger.debug(f"处理软件: {software}")
        for version, path in versions.items():
            logger.debug(f"处理版本: {version}, 路径: {path}")
            # 获取路径的目录部分
            dir_path = path.rsplit('\\', 1)[0] if '\\' in path else path
            # 合并软件名称和安装目录（同一行）
            package_name = f"{software} ({dir_path})"
            
            # 检查是否已启用
            status = '已启用' if app_data.enabled_versions.get(software) == version else '未启用'
            logger.debug(f"软件 {software} 版本 {version} 的状态: {status}")
            
            # 生成唯一键
            key = f"{software}_{version}"
            app_data.version_paths[key] = (software, version, path)
            
            # 添加到表格
            item_id = app_data.tree.insert('', tk.END, values=(
                package_name, 
                version, 
                status
            ))
            # 存储item_id到key的映射
            app_data.item_key_map[item_id] = key
            logger.debug(f"添加到表格: item_id={item_id}, values=({package_name}, {version}, {status})")
    
    logger.debug(f"表格更新完成，最终子项数量: {len(app_data.tree.get_children())}")


def activate_version(software, version, path):
    """激活版本"""
    try:
        # 获取可执行文件所在目录
        exe_dir = os.path.dirname(path)
        
        # 直接添加到系统PATH环境变量（修改注册表）
        success = add_to_path(exe_dir)
        
        if success:
            # 更新启用状态
            app_data.enabled_versions[software] = version
            messagebox.showinfo("成功", f"已成功激活{software} {version}\n环境变量已更新")
            
            # 调用刷新和初始化函数，使用相同的逻辑来更新版本列表，不显示额外消息框
            refresh_and_init(show_message=False)
        else:
            messagebox.showerror("失败", "激活版本失败")
    except Exception as e:
        messagebox.showerror("错误", f"激活版本时出错: {e}")


def handle_activation(item_id):
    """处理版本激活事件"""
    # 从映射中获取键
    if item_id in app_data.item_key_map:
        key = app_data.item_key_map[item_id]
        if key in app_data.version_paths:
            software, version, path = app_data.version_paths[key]
            activate_version(software, version, path)


def on_tree_double_click(event):
    """表格双击事件处理"""
    # 获取点击的列
    region = app_data.tree.identify_region(event.x, event.y)
    if region == "cell":
        # 获取点击的项
        item_id = app_data.tree.identify_row(event.y)
        handle_activation(item_id)


def refresh_and_init(show_message=True):
    """刷新版本列表并初始化
    
    Args:
        show_message (bool): 是否显示操作结果消息框
    """
    try:
        # 更新表格（包含初始化启用状态，会调用init_enabled_status重新扫描版本）
        update_table(app_data.current_nav.get())
        
        if show_message:
            messagebox.showinfo("成功", "版本列表已刷新并初始化")
    except Exception as e:
        if show_message:
            messagebox.showerror("错误", f"刷新版本列表失败: {e}")


def enable_selected():
    """启用选中的版本"""
    selected_item = app_data.tree.selection()
    if not selected_item:
        messagebox.showwarning("警告", "请先选择要启用的版本")
        return
    
    item_id = selected_item[0]
    handle_activation(item_id)


def create_gui():
    """创建GUI界面"""
    logger.debug("开始创建GUI界面")
    
    # 创建主窗口
    root = tk.Tk()
    root.title("版本切换工具")
    root.geometry("900x600")
    root.resizable(True, True)
    logger.debug("创建主窗口完成")
    
    # 初始化参数
    logger.debug("开始初始化参数")
    init_parameters()
    logger.debug(f"初始化参数完成，app_data: {app_data.__dict__}")
    
    # 初始化UI
    logger.debug("开始初始化UI")
    main_frame, sidebar_frame, content_frame, tree, button_frame, nav_items, style = init_ui(root)
    logger.debug("初始化UI完成")
    
    # 更新全局应用数据
    app_data.root = root
    logger.debug("更新全局应用数据完成")
    
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
    
    # 绑定双击事件
    tree.bind('<Double-1>', on_tree_double_click)
    
    # 刷新按钮
    refresh_button = ttk.Button(
        button_frame, 
        text="刷新", 
        style='Accent.TButton',
        command=refresh_and_init
    )
    refresh_button.pack(side=tk.RIGHT, padx=5)
    
    # 启用按钮
    enable_button = ttk.Button(
        button_frame, 
        text="启用", 
        style='Accent.TButton',
        command=enable_selected
    )
    enable_button.pack(side=tk.RIGHT, padx=5)
    
    # 初始化表格
    logger.debug("开始初始化表格")
    update_table('All')
    logger.debug("初始化表格完成")
    
    # 启动主循环
    logger.debug("启动主循环")
    root.mainloop()
    logger.debug("主循环结束")
