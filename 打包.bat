@echo off
F:\Python27WorkSp\MJSInterface
pyinstaller -w  GS_InterFaceServer.py

CD F:\Python27WorkSp\MJSInterface\dist
copy /y F:\Python27WorkSp\MJSInterface\dist\Config.ini F:\Python27WorkSp\MJSInterface\dist\GS_InterFaceServer
copy /y F:\Python27WorkSp\MJSInterface\dist\_mssql.pyd F:\Python27WorkSp\MJSInterface\dist\GS_InterFaceServer
md F:\Python27WorkSp\MJSInterface\dist\GS_InterFaceServer\log

