import subprocess;
from Results import fbHaveResults, fWriteResults;
from oConsole import oConsole;
# Colors used in output for various types of information:
NORMAL = -1;  # Console default color
INFO = 10;    # Light green
HILITE = 15;  # White
ERROR = 12;   # Light red

def fTestNetworkConnect(oProcess, sProcessType, sNetworkType, sIPAddress, uPort, sSandBoxToolsPath):
  sTestType = "network %s connect" % sNetworkType;
  if fbHaveResults(sProcessType, sTestType):
    oConsole.fPrint("Testing %s already completed" % sTestType);
    return;
  oConsole.fPrint("Testing ", sNetworkType, " network connection for process ", INFO, str(oProcess.uId), NORMAL, " running ", INFO, oProcess.sBinaryName);
  oTestProcess = subprocess.Popen(
    "\"%s\\CheckNetworkAccess\\bin\\Debug\\CheckNetworkAccess.exe\" -p %d %s %d" % (sSandBoxToolsPath, oProcess.uId, sIPAddress, uPort),
    stdout = subprocess.PIPE,
    stderr = subprocess.PIPE,
  );
  (sStdOut, sStdErr) = oTestProcess.communicate();
  assert not sStdErr, "Failed:\r\n%s" % sStdErr;
  if sStdOut in [
    "** Opened Connection **\r\n",
    "A connection attempt failed because the connected party did not properly respond after a period of time, or established connection failed because connected host has failed to respond %s:%d\r\n" % (sIPAddress, uPort),
    "No connection could be made because the target machine actively refused it %s:%d\r\n" % (sIPAddress, uPort),
  ]:
    # Connection was made
    fWriteResults(sProcessType, sTestType, False, "This process is able to open a connection on the %s to %s:%d." % (sNetworkType, sIPAddress, uPort));
  elif sStdOut in [
    "Unknown error (0x271d)\r\n",
    "(0xC0000022) - {Access Denied}\r\nA process has requested access to an object, but has not been granted those access rights.\r\n",
    "An attempt was made to access a socket in a way forbidden by its access permissions %s:%d\r\n" % (sIPAddress, uPort),
  ]:
    fWriteResults(sProcessType, sTestType, True);
  else:
    raise AssertionError("Unknown test output: %s" % sStdOut);
