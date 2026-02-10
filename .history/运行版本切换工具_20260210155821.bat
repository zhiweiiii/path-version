@echo off

cls
echo 版本切换工具
echo ================================
echo
echo 此工具用于管理和切换系统中的软件版本
echo 支持 Python、Node.js、Java、Git 等软件
echo
echo 注意: 需要管理员权限来修改系统环境变量
echo
echo 按任意键继续...
pause >nul

rem 以管理员身份运行版本切换工具
echo 正在请求管理员权限...
echo

PowerShell -Command "Start-Process 'python.exe' -ArgumentList 'main.py' -Verb RunAs"

echo
echo 工具已启动，请在新窗口中操作
echo
echo 按任意键退出...
pause >nul
