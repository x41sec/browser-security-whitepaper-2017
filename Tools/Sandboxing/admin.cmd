@ECHO OFF
:: Check if we are already running as admin
FSUTIL dirty query %systemdrive% >nul
IF NOT ERRORLEVEL 1 (
  COLOR 1F
  IF "%~1" == "" EXIT /B 0
  %*
  EXIT /B %ERRORLEVEL%
)
SETLOCAL
CALL :SET_DRIVE_AND_FOLDER "%CD%"
SET ADMIN_TMP_CMD=%TEMP%\admin_%RANDOM%%RANDOM%%RANDOM%%RANDOM%.cmd
ECHO @ECHO OFF >"%ADMIN_TMP_CMD%"
ECHO COLOR 1F >>"%ADMIN_TMP_CMD%"
ECHO TITLE Admin >>"%ADMIN_TMP_CMD%"
FOR /F "tokens=1,2,3,*" %%I IN ('NET USE') DO (
  IF "%%~I"=="OK" (
    ECHO NET USE "%%~J" "%%~K" ^>nul 2^>^&1 >>"%ADMIN_TMP_CMD%"
  )
)
ECHO %DRIVE% >>"%ADMIN_TMP_CMD%"
ECHO CD "%FOLDER%" >>"%ADMIN_TMP_CMD%"
IF "%~1" == "" (
  :: No arguments? Start cmd.exe and continue
  ECHO START %ComSpec% /T:1F>>"%ADMIN_TMP_CMD%"
) ELSE (
  :: With arguments: run command and wait
  ECHO CALL %*>>"%ADMIN_TMP_CMD%"
)
CALL "%~dp0admin.cmd.lnk"
DEL "%ADMIN_TMP_CMD%" & EXIT /B %ERRORLEVEL%

:SET_DRIVE_AND_FOLDER
  SET DRIVE=%~d1
  SET FOLDER=%~pnx1
  EXIT /B 0
