@echo off
for /r %%i in (.\src\*.cpp) do (
    if not exist .\exe\%%~ni.exe (
		g++ -Wall "src\%%~nxi" -o "exe\%%~ni.exe"
	)
)

