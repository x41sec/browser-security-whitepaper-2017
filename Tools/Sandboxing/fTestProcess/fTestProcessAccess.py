import subprocess;
from Results import fbHaveResults, fWriteResults;
from oConsole import oConsole;
# Colors used in output for various types of information:
NORMAL = -1;  # Console default color
INFO = 10;    # Light green
HILITE = 15;  # White
ERROR = 12;   # Light red

def fTestProcessAccess(oProcess, sProcessType, sSandBoxToolsPath):
  sTestType = "process access";
  if fbHaveResults(sProcessType, sTestType):
    oConsole.fPrint("Testing %s already completed" % sTestType);
    return;
  oConsole.fPrint("Testing process access for process ", INFO, str(oProcess.uId), NORMAL, " running ", INFO, oProcess.sBinaryName);
  oTestProcess = subprocess.Popen(
    "\"%s\\CheckProcessAccess\\bin\\Debug\\CheckProcessAccess.exe\" -p %d" % (sSandBoxToolsPath, oProcess.uId),
    stdout = subprocess.PIPE,
    stderr = subprocess.PIPE,
  );
  (sStdOut, sStdErr) = oTestProcess.communicate();
  assert not sStdErr, "Failed:\r\n%s" % sStdErr;
  if sStdOut == "":
    fWriteResults(sProcessType, sTestType, True);
  else:
    fWriteResults(sProcessType, sTestType, False, "This process is able to access the following processes:\r\n%s" % sStdOut);
