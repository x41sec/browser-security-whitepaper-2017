@ECHO OFF
SETLOCAL
SET PYTHONDONTWRITEBYTECODE=1

REM Set this to the IP address of another machine on your local network in
REM order to test connecting to it on the specified port as part of the intranet
REM connection tests. If set to "-" (the default), these tests will only try to
REM connect to the local machine using it's intranet IP address.
SET INTRANET_IP_ADDRESS=10.10.0.1
SET INTRANET_PORT=80

REM This script will run all browsers, or a single browser if you specify it
REM on the command-line ("chrome", "edge", "msie").
REM Each browser is run in a modified version of BugId, that runs `fTestProcess`
REM for every process it sees after letting it run for a number of seconds to
REM make sure everything is loaded in the process.
REM fTestProcess\fTestProcess.py will look at the binaries loaded in a process
REM to determine the "type" of the process. (e.g. one of the Edge
REM AppContainers, chrome renderer, WebGL process, etc...). It will run a
REM number of tests from James Foreshaw's suite to find out what an attacker
REM is able to do from within the process. If the process is sandboxed well,
REM the list of things an attacker can do is small or empty.
REM Some of these tests (especially the registry tests) take a long while to
REM run as they recursively check access for every single registry key in the
REM system. You may want to disable them temporarily if you are testing things.
REM It will also gather information about what hardening is applied to the
REM process and the binaries it loads.

REM The results for each proces is stored in a sub-folder of the "Results"
REM folder. The name of the sub-folder describes the tested process.
IF NOT EXIST "%~dp0\ddsCapabilityDetails_by_sName.py" (
  ECHO A capability SID translation table needs to be created to convert these SIDs
  ECHO into human readable values. This only needs to be done once, as the table is
  ECHO saved to disk and re-used in future tests.
  ECHO.
  CALL "%~dp0\Create SID translation table.cmd"
)

IF "%PROCESSOR_ARCHITEW6432%" == "AMD64" (
  SET OSISA=x64
) ELSE IF "%PROCESSOR_ARCHITECTURE%" == "AMD64" (
  SET OSISA=x64
) ELSE (
  SET OSISA=x86
)

IF NOT EXIST "%~dp0\BugId\BugId.cmd" (
  ECHO %~dp0\BugId\BugId.cmd not found!
  ECHO.
  ECHO Please download BugId from this URL and store it in the BugId folder:
  ECHO     https://github.com/SkyLined/BugId
  ENDLOCAL
  EXIT /B 1
)
IF NOT EXIST "%~dp0\cBugId\cBugId.py" (
  ECHO %~dp0\cBugId\cBugId.py not found!
  ECHO.
  ECHO Please download cBugId from this URL and store it in the cBugId folder:
  ECHO     https://github.com/SkyLined/cBugId
  ENDLOCAL
  EXIT /B 1
)
IF NOT EXIST "%~dp0\FileSystem\FileSystem.py" (
  ECHO %~dp0\FileSystem\FileSystem.py not found!
  ECHO.
  ECHO Please download FileSystem from this URL and store it in the FileSystem folder:
  ECHO     https://github.com/SkyLined/FileSystem
  ENDLOCAL
  EXIT /B 1
)
IF NOT EXIST "%~dp0\Kill\Kill.py" (
  ECHO %~dp0\Kill\Kill.py not found!
  ECHO.
  ECHO Please download Kill from this URL and store it in the Kill folder:
  ECHO     https://github.com/SkyLined/Kill
  ENDLOCAL
  EXIT /B 1
)
IF NOT DEFINED PYTHON (
  IF EXIST "%SystemDrive%\Python27\python.exe" (
    SET PYTHON=%SystemDrive%\Python27\python.exe
  ) ELSE (
    SET PYTHON=%~dp0Python_%OSISA%\python.exe
  )
)
IF NOT EXIST "%PYTHON%" (
  ECHO - Cannot find python.exe at %PYTHON%!
  ECHO - Please set the %%PYTHON%% environment variable to the full path to python.exe.
  ECHO.
  ECHO If you haven't installed Python 2.7 yet, please download and install it now.
  ECHO   https://www.python.org/download/releases/2.7/
  ENDLOCAL
  EXIT /B 1
)
IF NOT DEFINED CDB (
  CALL :SET_CDB_IF_EXISTS "%~dp0WinDbg_%OSISA%\cdb.exe"
  CALL :SET_CDB_IF_EXISTS "%ProgramFiles%\Windows Kits\10\Debuggers\%OSISA%\cdb.exe"
  CALL :SET_CDB_IF_EXISTS "%ProgramFiles%\Windows Kits\8.1\Debuggers\%OSISA%\cdb.exe"
  CALL :SET_CDB_IF_EXISTS "%ProgramFiles%\Windows Kits\8.0\Debuggers\%OSISA%\cdb.exe"
  IF EXIST "%ProgramFiles(x86)%" (
    CALL :SET_CDB_IF_EXISTS "%ProgramFiles(x86)%\Windows Kits\10\Debuggers\%OSISA%\cdb.exe"
    CALL :SET_CDB_IF_EXISTS "%ProgramFiles(x86)%\Windows Kits\8.1\Debuggers\%OSISA%\cdb.exe"
    CALL :SET_CDB_IF_EXISTS "%ProgramFiles(x86)%\Windows Kits\8.0\Debuggers\%OSISA%\cdb.exe"
  )
  IF NOT DEFINED CDB (
    ECHO Please set the %%CDB%% environment variable to the full path to cdb.exe.
    ECHO.
    ECHO If you haven't installed the DEbugging Tools for Windows yet, please download
    ECHO and install it now.
    ECHO   https://docs.microsoft.com/en-us/windows-hardware/drivers/debugger/
    ENDLOCAL
    EXIT /B 1
  )
) ELSE (
  :: Make sure cdb is quoted
  SET CDB="%CDB:"=%"
)
IF NOT EXIST %CDB% (
  ECHO - Cannot find cdb.exe at %PYTHON%!
    ECHO Please set the %%CDB%% environment variable to the full path to cdb.exe.
    ECHO.
    ECHO If you haven't installed the DEbugging Tools for Windows yet, please download
    ECHO and install it now.
    ECHO   https://docs.microsoft.com/en-us/windows-hardware/drivers/debugger/
  ENDLOCAL
  EXIT /B 1
)

SET BugId=%~dp0\BugId\BugId.py
IF "%PROCESSOR_ARCHITECTURE%" == "x86" (
  SET Kill=%~dp0\Kill\bin\Kill_x86.exe
) ELSE (
  SET Kill=%~dp0\Kill\bin\Kill_x64.exe
)

REM Start a web server so we can access intranet pages and accept connections
REM on the loopback device. If this is already running from a previous testrun,
REM it will silently fail, so the old server is used which is fine.
START /MIN "HTTP server used for testing" %PYTHON% oHTTPServer.py 

SET BugIdArguments="--nApplicationMaxRunTime=60" "--cBugId.bEnsurePageHeap=false"
SET TestURL="http://127.0.0.1:28876/index.html"
IF EXIST "%ProgramFiles%\Google\Chrome\Application\chrome.exe" (
  SET ChromePath="%ProgramFiles%\Google\Chrome\Application\chrome.exe"
) ELSE (
  SET ChromePath="%ProgramFiles(x86)%\Google\Chrome\Application\chrome.exe"
)

IF NOT EXIST "%~dp0Results" (
  mkdir "%~dp0Results"
)

IF "%~1" == "chrome" (
  CALL :TEST_CHROME
  IF ERRORLEVEL 1 GOTO :ERROR
) ELSE IF "%~1" == "edge" (
  CALL :TEST_EDGE
  IF ERRORLEVEL 1 GOTO :ERROR
) ELSE IF "%~1" == "msie" (
  CALL :TEST_MSIE
  IF ERRORLEVEL 1 GOTO :ERROR
) ELSE IF "%~1" == "pid" (
  CALL :TEST_PID %~2
  IF ERRORLEVEL 1 GOTO :ERROR
) ELSE (
  If NOT "%~1" == "--i-know" (
    ECHO This script will automatomatically start Google Chrome, Microsoft Edge and
    ECHO Microsoft Internet Explorer in a modified version of BugId in order to
    ECHO run a number of tests.
    ECHO.
    ECHO Prerequisites:
    ECHO - You will need to allow Powershell to run unsigned scripts by executing the
    ECHO   following command as an administrator:
    ECHO      powershell.exe Set-ExecutionPolicy -ExecutionPolicy Bypass
    ECHO - You may see popups from the built-in Windows Firewall asking you if you want
    ECHO   to allow a certain process access to the network. Please allow *ALL* of these
    ECHO   requests to get proper test results.
    ECHO - You will need to open Google Chrome, Microsoft Edge and Internet Explorer now
    ECHO   and browse to:
    ECHO      %TestURL%
    ECHO   This should open a number of tabs in your browser. If you see a warning about
    ECHO   popups being blocked, please ALWAY allow them and refresh the page to
    ECHO   make sure the popups are opened. Next, find the tab that points to the Adobe
    ECHO   Flash website; it may ask for you permission to run Flash. Please ALWAY allow
    ECHO   this too. Once you have made sure that pop-ups are allowed and that WebGl,
    ECHO   Flash and PDF files are shown correctly, you can close the browser to
    ECHO   continue with the tests. Note that Microsoft Internet Explorer does not show
    ECHO   PDF files; this is expected.
    ECHO - You will need to install at least one extension in Edge in order to have the
    ECHO   AppContainer that hosts extensions analyzed.
    ECHO.
    ECHO Notes:
    ECHO - Tests results are generated only once; if a test result file exists, that
    ECHO   test is not run again. If you make changes to the test and want to make
    ECHO   sure it gets run again, please delete or rename the "Results" folder.
    ECHO - You should run these tests as a normal user to make sure the browser is not
    ECHO   started with elevated privileges, which can result in artificially high
    ECHO   integrity levels for certain processes in Chrome and Internet Explorer.
    ECHO   If you do run these tests as an administrator, none of the Internet Explorer
    ECHO   processes will run with low integrity, and none of them will therefore be
    ECHO   considered sandboxed or subjected to any sandboxing tests.
    ECHO.
    ECHO Once you have made sure the PDF is shown in Chrome and Edge, and Flash and WebGL
    ECHO are shown in all three browsers, and that all other prerequisites are met,
    ECHO PRESS ENTER TO CONTINUE.
    ECHO ^(You may disable this warning using the "--i-know" command-line argument^).
    PAUSE >nul
  )
  CALL :TEST_CHROME
  IF ERRORLEVEL 1 GOTO :ERROR
  CALL :TEST_EDGE
  IF ERRORLEVEL 1 GOTO :ERROR
  CALL :TEST_MSIE
  IF ERRORLEVEL 1 GOTO :ERROR
)

ECHO Tests completed.
ENDLOCAL
EXIT /B 0

:TEST_CHROME
  ECHO Chrome tests ###############################################################
  CALL BugId\BugId.cmd %BugIdArguments% %ChromePath% -- %TestURL% --disable-popup-blocking
  EXIT /B %ERRORLEVEL%

:TEST_EDGE
  ECHO Edge tests #################################################################
  %Kill% MicrosoftEdge.exe MicrosoftEdgeCP.exe RuntimeBroker.exe browser_broker.exe ApplicationFrameHost.exe 
  IF ERRORLEVEL 1 EXIT /B %ERRORLEVEL%
  CALL CleanupEdgeRecoveryData.cmd
  IF ERRORLEVEL 1 EXIT /B %ERRORLEVEL%

  ECHO BugId: load the new tab page, which should have a special AppContainer.
  CALL BugId\BugId.cmd %BugIdArguments% edge --
  IF ERRORLEVEL 1 EXIT /B %ERRORLEVEL%

  ECHO BugId: Load the rest of the tests
  %Kill% MicrosoftEdge.exe MicrosoftEdgeCP.exe RuntimeBroker.exe browser_broker.exe ApplicationFrameHost.exe 
  CALL CleanupEdgeRecoveryData.cmd
  IF ERRORLEVEL 1 EXIT /B %ERRORLEVEL%
  CALL BugId\BugId.cmd %BugIdArguments% edge -- %TestURL%
  IF ERRORLEVEL 1 EXIT /B %ERRORLEVEL%
  EXIT /B %ERRORLEVEL%

:TEST_MSIE
  REM Internet Explorer tests ##################################################
  CALL BugId\BugId.cmd %BugIdArguments% msie_%OSISA% -- %TestURL%
  EXIT /B %ERRORLEVEL%

:TEST_PID
  REM Arbitrary process ID tests ###############################################
  CALL BugId\BugId.cmd %BugIdArguments% --pid=%~1
  EXIT /B %ERRORLEVEL%

:ERROR
  ECHO Tests abort because of an error.
  EXIT /B 1

:SET_CDB_IF_EXISTS
  IF NOT DEFINED cdb (
    IF EXIST "%~1" (
      SET CDB="%~1"
    )
  )
  EXIT /B 0
