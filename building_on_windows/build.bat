rd /s /q dist
cd ..
C:\Python27\python building_on_windows\compile_extensions.py build_ext --inplace
cd building_on_windows
call C:\Python27\Scripts\cxfreeze.bat ..\cplayer.py --include-path=.. --exclude-modules=pyximport
xcopy /e /i ..\resources dist\resources
xcopy /e dlls\*.* dist\
