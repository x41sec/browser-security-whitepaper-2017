@ECHO OFF
IF "%~1" == "" (
  ECHO Usage:
  ECHO   Get-ProcessMitigation ^<pid^>
) ELSE (
  POWERSHELL "Import-Module '%~dp0\ProcessMitigations\ProcessMitigations.psd1'; Get-ProcessMitigation -Id '%~1';"
)