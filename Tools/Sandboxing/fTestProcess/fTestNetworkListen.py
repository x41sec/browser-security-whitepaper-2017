import socket, subprocess, threading;
from Results import fbHaveResults, fWriteResults;
from oConsole import oConsole;
# Colors used in output for various types of information:
NORMAL = -1;  # Console default color
INFO = 10;    # Light green
HILITE = 15;  # White
ERROR = 12;   # Light red

def fTestNetworkListen(oProcess, sProcessType, sNetworkType, sIPAddress, uPort, sSandBoxToolsPath):
  sTestType = "network %s listen" % sNetworkType;
  if fbHaveResults(sProcessType, sTestType):
    oConsole.fPrint("Testing %s already completed" % sTestType);
    return;
  oConsole.fPrint("Testing ", sNetworkType, " network listen for process ", INFO, str(oProcess.uId), NORMAL, " running ", INFO, oProcess.sBinaryName);
  oTestProcess = subprocess.Popen(
    "\"%s\\CheckNetworkAccess\\bin\\Debug\\CheckNetworkAccess.exe\" -p %d -l %s %d" % (sSandBoxToolsPath, oProcess.uId, sIPAddress, uPort),
    stdout = subprocess.PIPE,
    stderr = subprocess.PIPE,
  );
  # The process is currently suspended, so it can't actually accept a connection.
  # This means the test will hang if it can listen on a port, even if we try to
  # connect to the port. Instead, we will use a timer to terminate the test
  # after five seconds and see if it outputs an error or not.
  abConnectionAccepted = []; # Weird hack to be able to export info from another thread.
  def fConnect():
    oConsole.fStatus("fConnect: Attempting to connect to ", INFO, sIPAddress, NORMAL, ":", INFO, str(uPort), NORMAL, "...");
    try:
      socket.create_connection((sIPAddress, uPort), 5);
    except socket.error as oException:
      abConnectionAccepted.append(False);
    else:
      abConnectionAccepted.append(True);
    oTestProcess.terminate();
  oConnectThread = threading.Thread(target=fConnect);
  oConnectThread.start();
  (sStdOut, sStdErr) = oTestProcess.communicate();
  assert not sStdErr, "Failed:\r\n%s" % sStdErr;
  oConnectThread.join();
  bConnectionAccepted = abConnectionAccepted[0];
  if bConnectionAccepted:
    fWriteResults(sProcessType, sTestType, False, "+ This process is able to listen for connections on the %s at %s:%d.\r\n%s" % (sNetworkType, sIPAddress, uPort, sStdOut));
  elif sStdOut in [
    "Make a connection to %s:%d\r\n" % (sIPAddress, uPort), # It thinks it can accept connections, but it never will.
    "Unknown error (0x271d)\r\n",
    "An attempt was made to access a socket in a way forbidden by its access permissions\r\n",
    "An attempt was made to access a socket in a way that was forbidden by its access permissions\r\n",
    "(0xC0000022) - {Access Denied}\r\nA process has requested access to an object, but has not been granted those access rights.\r\n",
  ]:
    fWriteResults(sProcessType, sTestType, True);
  else:
    raise AssertionError("Unknown test output: %s" % sStdOut);
