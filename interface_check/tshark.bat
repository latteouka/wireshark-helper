@ECHO OFF
chcp 65001
setlocal enableDelayedExpansion
:: 確認wireshark安裝在哪裡
IF exist "C:\Program Files (x86)\Wireshark" (
	SET URL="C:\Program Files (x86)\Wireshark"
)

IF exist "C:\Program Files\Wireshark" (
	SET URL="C:\Program Files\Wireshark"
)

(%URL%\tshark -D) > all_interfaces.txt

set "file=all_interfaces.txt"
set /A i=0

for /F "usebackq delims=" %%a in ("%file%") do (
set /A i+=1
::call echo %%i%%
call set array[%%i%%]=%%a
call set n=%%i%%
)

for /L %%i in (1,1,%n%) do call echo %%array[%%i]%%

set /p interface="請選擇網路介面卡："

echo !array[%interface%]!

echo !array[%interface%]! > interface.txt

endlocal

del all_interfaces.txt

pause