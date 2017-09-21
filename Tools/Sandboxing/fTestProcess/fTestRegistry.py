import subprocess;
from Results import fbHaveResults, fWriteResults;
from oConsole import oConsole;
# Colors used in output for various types of information:
NORMAL = -1;  # Console default color
INFO = 10;    # Light green
HILITE = 15;  # White
ERROR = 12;   # Light red

def fTestRegistry(oProcess, sProcessType, sHiveName, sSandBoxToolsPath):
  sTestType = "registry %s" % sHiveName;
  if fbHaveResults(sProcessType, sTestType):
    oConsole.fPrint("Testing %s already completed" % sTestType);
    return;
  oConsole.fPrint("Testing registry access to ", INFO, sHiveName, NORMAL, " for process ", INFO, str(oProcess.uId), NORMAL, " running ", INFO, oProcess.sBinaryName);
  oTestProcess = subprocess.Popen(
    "\"%s\\CheckRegistryAccess\\bin\\Debug\\CheckRegistryAccess.exe\" -w -r -p %d %s\\" % (sSandBoxToolsPath, oProcess.uId, sHiveName),
    stdout = subprocess.PIPE,
    stderr = subprocess.PIPE,
  );
  (sStdOut, sStdErr) = oTestProcess.communicate();
  assert not sStdErr, "Failed:\r\n%s" % sStdErr;
  if sStdOut == "":
    fWriteResults(sProcessType, sTestType, True);
  else:
    fWriteResults(sProcessType, sTestType, False, "This process is able to access the following registry keys in %s:\r\n%s" % (sHiveName, sStdOut));
