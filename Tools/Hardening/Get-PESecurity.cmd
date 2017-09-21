@ECHO OFF
IF "%~1" == "" (
  ECHO Usage:
  ECHO   Get-PESecurity ^<path\to\PE-binary^>
) ELSE (
  POWERSHELL "Import-Module '%~dp0\PESecurity\Get-PESecurity.psm1'; Get-PESecurity -File '%~1';"
)