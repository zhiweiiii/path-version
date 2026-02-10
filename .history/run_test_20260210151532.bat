@echo off

cls
echo 版本切换工具 - 注册表访问测试
echo ===============================
echo
echo 此脚本将以管理员身份运行测试程序
echo 用于测试系统注册表访问权限
echo
echo 按任意键继续...
pause >nul

rem 以管理员身份运行测试脚本
powershell -Command "
$psi = New-Object System.Diagnostics.ProcessStartInfo
$psi.FileName = 'cmd.exe'
$psi.Arguments = '/k "cd /d "' + $pwd.Path + '" && python test_registry.py"'
$psi.Verb = 'RunAs'
$psi.WindowStyle = 'Normal'
[System.Diagnostics.Process]::Start($psi)
"

echo
echo 测试窗口已启动，请在新窗口中查看结果
echo
echo 按任意键退出...
pause >nul
