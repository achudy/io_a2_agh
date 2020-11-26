@ECHO OFF

setlocal
call :setESC

ECHO %ESC%[32m================================================================================%ESC%[0m
ECHO %ESC%[32mVehicle Detector v1.33.7 installation wizard%ESC%[0m
ECHO %ESC%[32m================================================================================%ESC%[0m
ECHO:
ECHO This tool will help you setup Vehicle Detector.
ECHO:
ECHO Press 1 to perform full installation, Visual Studio is required %ESC%[32m(recomended)%ESC%[0m
ECHO Press 2 to install Python 3.8.0 and all necessary modules, %ESC%[31mversion 3.9 is not supported%ESC%[0m
CHOICE  /c 123 /m "Press 3 to install CUDA 10.1, other versions are not supported"

IF ERRORLEVEL==3 CALL :cuda
IF ERRORLEVEL==2 CALL :python
IF ERRORLEVEL==1 CALL :full

ECHO %ESC%[32m================================================================================%ESC%[0m
ECHO %ESC%[32mThank you for choosing our product%ESC%[0m
ECHO %ESC%[32m================================================================================%ESC%[0m
PAUSE

EXIT /B %ERRORLEVEL%

:full
call :python
call :cuda
EXIT /B 0

:python
ECHO %ESC%[32m================================================================================%ESC%[0m
ECHO %ESC%[32mPlease select "Add Python 3.8 to PATH"%ESC%[0m
ECHO %ESC%[32m================================================================================%ESC%[0m
START /W .\files\python.exe
setx path "C:\Users\%USERNAME%\AppData\Local\Programs\Python\Python38\Scripts\" /M
python get-pip.py
START /W C:\Users\%USERNAME%\AppData\Local\Programs\Python\Python38\Scripts\pip.exe install -r .\files\requ.txt
EXIT /B 0

:cuda
ECHO %ESC%[32m================================================================================%ESC%[0m
ECHO %ESC%[32mPlease do not change installation folder%ESC%[0m
ECHO %ESC%[32m================================================================================%ESC%[0m
START /W .\files\cuda.exe
xcopy .\files\cudnn.h C:\"Program Files"\"NVIDIA GPU Computing Toolkit"\CUDA\v10.1\include\
xcopy .\files\cudnn.lib C:\"Program Files"\"NVIDIA GPU Computing Toolkit"\CUDA\v10.1\lib\x64\
xcopy .\files\cudnn64_7.dll C:\"Program Files"\"NVIDIA GPU Computing Toolkit"\CUDA\v10.1\bin\
EXIT /B 0

:setESC
for /F "tokens=1,2 delims=#" %%a in ('"prompt #$H#$E# & echo on & for %%b in (1) do rem"') do (
  set ESC=%%b
  exit /B 0
)

