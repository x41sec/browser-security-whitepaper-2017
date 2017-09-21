@ECHO OFF
SETLOCAL

ECHO * Cleaning Edge recovery data...
CALL :DELETE_ALL_SUBFOLDERS "%LocalAppData%\Packages\Microsoft.MicrosoftEdge_8wekyb3d8bbwe\AC\MicrosoftEdge\User\Default\Recovery\Active"
IF ERRORLEVEL 1 GOTO :ERROR

ENDLOCAL & EXIT /B 0

:ERROR
  ECHO - Error %ERRORLEVEL%
  ENDLOCAL & EXIT /B %ERRORLEVEL%

:DELETE_ALL_SUBFOLDERS
  SET DELETED=FALSE
  FOR /D %%I IN ("%~1\*") DO (
    ECHO   - %%~nxI\*
    SET DELETED=TRUE
    RD "%%~I" /s /q
    IF ERRORLEVEL 1 EXIT /B 1
  )
  FOR %%I IN ("%~1\*") DO (
    ECHO   - %%~nxI
    SET DELETED=TRUE
    DEL "%%~I" /q
    IF ERRORLEVEL 1 EXIT /B 1
  )
  IF "%DELETED%" == "FALSE" (
    ECHO   * Nothing to delete
  )
  EXIT /B 0
