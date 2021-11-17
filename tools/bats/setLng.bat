@ECHO OFF
chcp 65001

echo -----------------------------
echo 1.zh_CN 中文 Chinese
echo -----------------------------

set lng=""

:xz
set /p Choice=请输入要设置的系统语言编号：
if %Choice% == "1" (set lng=zh_CN)
if %Choice% == "0" (exit)

reg add "HEKY_CURRENT_USER\Control Panel\International" /v LocaleName /t reg_sz /d %lng% /f

echo 成功修改系统语言为：%lng%

ping -n 5 127.0.0.1 > nul

EXIT