import subprocess;
from Results import fbHaveResults, fWriteResults;
from oConsole import oConsole;
# Colors used in output for various types of information:
NORMAL = -1;  # Console default color
INFO = 10;    # Light green
HILITE = 15;  # White
ERROR = 12;   # Light red

def fTestFileAccess(oProcess, sProcessType, sTestPath, sSandBoxToolsPath):
  sTestType = "file access";
  if fbHaveResults(sProcessType, sTestType):
    oConsole.fPrint("Testing %s already completed" % sTestType);
    return;
  oConsole.fPrint("Testing ", INFO, "file access", NORMAL, " for process ", INFO, str(oProcess.uId), NORMAL, " running ", INFO, oProcess.sBinaryName);
  oTestProcess = subprocess.Popen(
    "\"%s\\CheckFileAccess\\bin\\Debug\\CheckFileAccess.exe\" -q -r -w --pid=%d %s" % (sSandBoxToolsPath, oProcess.uId, sTestPath),
    stdout = subprocess.PIPE,
    stderr = subprocess.PIPE,
  );
  (sStdOut, sStdErr) = oTestProcess.communicate();
  assert not sStdErr, "Failed:\r\n%s" % sStdErr;
  if sStdOut == "":
    fWriteResults(sProcessType, sTestType, True);
  else:
    fWriteResults(sProcessType, sTestType, False, "This process is able to access the following files:\r\n%s" % sStdOut);
