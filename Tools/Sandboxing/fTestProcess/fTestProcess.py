import os, re, socket, subprocess, threading;

from Results import fbHaveResults, fWriteResults;
from oConsole import oConsole;
# Colors used in output for various types of information:
NORMAL =  0x0F07;  # Console default color
INFO =    0x0F0A;  # Light green (foreground only)
HILITE =  0x0F0F;  # White (foreground only)
ERROR =   0x0F0C;  # Light red (foreground only)

sSandBoxToolsPath = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "sandbox-attacksurface-analysis-tools"));
sHardeningToolsPath = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", "Hardening"));
sTestPath = os.environ.get("SystemDrive") + "\\";
sAdditionalIntranetIPAddress = os.getenv("INTRANET_IP_ADDRESS");
assert sAdditionalIntranetIPAddress, \
    "You have to set the INTRANET_IP_ADDRESS environment variable to an IP address of a machine that accepts connections on at least one port, "\
    "and the INTRANET_PORT environment variable to a port number on which it accepts such connections.";
if sAdditionalIntranetIPAddress == "-":
  sAdditionalIntranetIPAddress = None;
else:
  uAdditionalIntranetConnectPort = long(os.getenv("INTRANET_PORT"));
sLoopbackIPAddress = "127.0.0.1";
uLoopbackConnectPort = 28876;
uLoopbackListenPort = 28888;
sIntranetIPAddress = socket.gethostbyname_ex(socket.gethostname())[2][0];
uIntranetConnectPort = 445;
uIntranetListenPort = 28888;
sInternetIPAddress = socket.gethostbyname_ex("example.com")[2][0];
uInternetConnectPort = 80;

# You can disable individual tests here to speed up testing.
bTestAppContainer = True;
bTestProcessMitigations = True;
bTestBinaryHardening = True;
bTestFileAccess = True;
bTestNetworkAccess = True;
bTestProcessAccess = True;
bTestRegistryAccess = True;

def fTestProcess(oBugId, oProcess):
  # Let the process run for 20 seconds to initialize stuff and load things.
  oBugId.foSetTimeout(
    sDescription = "Browser Security Process Tests timeout",
    nTimeout = 20.0,
    fCallback = lambda oBugId: fRunProcessTestsAfterTimeout(oProcess),
  );

def fRunProcessTestsAfterTimeout(oProcess):
  if oProcess.bTerminated:
    oConsole.fPrint(ERROR, "- Process ", str(oProcess.uId), " was terminated before tests could start...");
    return;
  sSandboxType = None;
  oConsole.fPrint("* Testing process ", INFO, str(oProcess.uId), NORMAL, " running ", INFO, oProcess.sBinaryName, NORMAL, "...");
  if oProcess.sBinaryName.lower() in [
    "applicationframehost.exe", "browser_broker.exe", "runtimebroker.exe", # Edge
    "software_reporter_tool.exe", # Chrome
  ]:
    sSandboxType = "not sandboxed";
#    oConsole.fPrint("* Process ", INFO, str(oProcess.uId), NORMAL, " is running ", INFO, oProcess.sBinaryName, NORMAL, ", which is not sandboxed.");
#    return;
  elif oProcess.sBinaryName.lower() == "microsoftedge.exe":
    sSandboxType = "Master AppContainer";
  elif oProcess.sBinaryName.lower() == "microsoftedgecp.exe":
    sSandboxType = "Internet or Intranet AppContainer pid=%d" % oProcess.uId;
    for oModule in oProcess.aoModules:
      if oModule.sBinaryName.lower() == "flash.ocx":
        sSandboxType = "Flash AppContainer";
        break;
      elif oModule.sBinaryName.lower() == "windows.data.pdf.dll":
        sSandboxType = "Internet or Intranet AppContainer (hosting PDF reader)";
        break;
      elif re.match(r"^d3dcompiler_\d+\.dll$", oModule.sBinaryName, re.I):
        sSandboxType = "Internet or Intranet AppContainer (hosting WebGL)";
        break;
  elif oProcess.sBinaryName.lower() == "iexplore.exe":
    if oProcess in oProcess.oCdbWrapper.aoMainProcesses:
      sSandboxType = "Main process";
    else:
      sSandboxType = "Content process pid=%d" % oProcess.uId;
      for oModule in oProcess.aoModules:
        if oModule.sBinaryName.lower() == "flash.ocx":
          sSandboxType = "Flash content process";
          break;
  elif oProcess.sBinaryName.lower() == "chrome.exe":
    oTypeMatch = re.search(r"\s\-\-type=(\S+)", oProcess.sCommandLine);
    if not oTypeMatch:
      sSandboxType = "main process";
#      oConsole.fPrint("* Process ", INFO, str(oProcess.uId), NORMAL, " is the main chrome process, which is not sandboxed.");
#      return;
    else:
      sSandboxType = oTypeMatch.group(1);
#      if sSandboxType in ["crashpad-handler", "watcher"]:
#        oConsole.fPrint("* Process ", INFO, str(oProcess.uId), NORMAL, " is a ", INFO, sSandboxType, NORMAL, " process, which is not sandboxed.");
#        return;
  elif oProcess.sBinaryName.lower() == "iexplore.exe":
    sSandboxType = "iexplore unknown pid=%d" % oProcess.uId;
  else:
    sSandboxType = "UNKNOWN pid=%d" % oProcess.uId;
  assert sSandboxType, \
      "Cannot determine process type based on binary name:\r\n%s" % oProcess.sBinaryName;
  # sProcessType = "<binary>.exe <version> [x86|x64] pid=<pid> <sandbox>"
  sProcessType = " ".join([oProcess.sBinaryName, oProcess.oMainModule.sFileVersion, oProcess.sISA, sSandboxType]);
  
  if not os.path.isdir(r"Results\%s" % sProcessType):
    os.mkdir(r"Results\%s" % sProcessType);
  if not os.path.isfile(r"Results\%s\Process details.txt" % sProcessType):
    uProcessIntegrityLevel = oProcess.uIntegrityLevel;
    sProcessIntegrityLevel = " ".join([s for s in [
      {0: "Untrusted", 1: "Low", 2: "Medium", 3: "High", 4: "System"}.get(uProcessIntegrityLevel >> 12, "Unknown"),
      "Integrity",
      uProcessIntegrityLevel & 0x100 and "Plus" or None,
    ] if s]);
    asProcessDetails = [
      "Command Line: %s" % oProcess.sCommandLine,
      "Process type: %s" % sProcessType,
      "Integrity level: 0x%X (%s)" % (uProcessIntegrityLevel, sProcessIntegrityLevel),
    ];
    if bTestAppContainer:
      asCapabilities = fasTestAppContainerCapabilities(oProcess, sHardeningToolsPath);
      if asCapabilities:
        asProcessDetails.extend([
          "",
          "AppContainer Capabilities:",
        ] + [
          "  %s" % s for s in asCapabilities
        ]);
      else:
        asProcessDetails.append("The process is not running in an AppContainer");
    if bTestProcessMitigations:
      asProcessDetails.extend([
        "",
        "Process mitigations:",
      ]);
      dsProcessMitigations = fdsTestProcessMitigations(oProcess, sProcessType, sHardeningToolsPath);
      for sName in sorted(dsProcessMitigations.keys()):
        sValue = dsProcessMitigations[sName];
        asProcessDetails.append("    %40s: %s" % (sName, sValue));
    # We need to sort the modules by binary name for this to be somewhat readable.
    asProcessDetails.extend([
      "",
      "Loaded modules",
    ]);
    dsModuleList = {};
    for oModule in oProcess.aoModules:
      dsModuleList[oModule.sBinaryName] = oModule;
    for sBinaryName in sorted(dsModuleList.keys()):
      # Dump module name and version
      oModule = dsModuleList[sBinaryName];
      asProcessDetails.append("  %s %s" % (oModule.sBinaryPath, oModule.sFileVersion));
    open(r"Results\%s\Process details.txt" % sProcessType, "wb").write("\r\n".join(asProcessDetails) + "\r\n");
    if bTestBinaryHardening:
      asBinaryDetails = [];
      # Get hardening information for each module
      for sBinaryName in sorted(dsModuleList.keys()):
        # Dump module name and version
        oModule = dsModuleList[sBinaryName];
        asBinaryDetails.append("  %s %s" % (oModule.sBinaryPath, oModule.sFileVersion));
        dsHardeningInfo = fdsTestBinaryHardening(oProcess, sProcessType, oModule, sHardeningToolsPath);
        if dsHardeningInfo is None:
          asBinaryDetails.append("    The file could not be found on the system!");
        else:
          for sFeature in sorted(dsHardeningInfo.keys()):
            asBinaryDetails.append("    %40s: %s" % (sFeature, dsHardeningInfo[sFeature]));
      open(r"Results\%s\Binary details.txt" % sProcessType, "wb").write("\r\n".join(asBinaryDetails) + "\r\n");
  
  if oProcess.uIntegrityLevel >= 0x2000:
    oConsole.fPrint("- Process ", INFO, str(oProcess.uId), NORMAL, " is running at integrity level ", INFO, \
        "0x%X" % oProcess.uIntegrityLevel, NORMAL, ": ", INFO, "no sandboxing tests will be run", NORMAL, ".");
  else:
    # Test file access
    if bTestFileAccess:
      fTestFileAccess(oProcess, sProcessType, sTestPath, sSandBoxToolsPath);
    
    # Test network access
    if bTestNetworkAccess:
      fTestNetworkConnect(oProcess, sProcessType, "loopback device", sLoopbackIPAddress, uLoopbackConnectPort, sSandBoxToolsPath);
      fTestNetworkConnect(oProcess, sProcessType, "intranet", sIntranetIPAddress, uIntranetConnectPort, sSandBoxToolsPath);
      if sAdditionalIntranetIPAddress:
        fTestNetworkConnect(oProcess, sProcessType, "intranet %s" % sAdditionalIntranetIPAddress, sAdditionalIntranetIPAddress, uAdditionalIntranetConnectPort, sSandBoxToolsPath);
      fTestNetworkConnect(oProcess, sProcessType, "internet", sInternetIPAddress, uInternetConnectPort, sSandBoxToolsPath);
      fTestNetworkListen(oProcess, sProcessType, "loopback device", sLoopbackIPAddress, uLoopbackListenPort, sSandBoxToolsPath);
      fTestNetworkListen(oProcess, sProcessType, "intranet", sIntranetIPAddress, uIntranetListenPort, sSandBoxToolsPath);
    
    # Test process access
    if bTestProcessAccess:
      fTestProcessAccess(oProcess, sProcessType, sSandBoxToolsPath);
    
    # Test registry access
    if bTestRegistryAccess:
      fTestRegistry(oProcess, sProcessType, "hkey_current_user", sSandBoxToolsPath);
      fTestRegistry(oProcess, sProcessType, "hkey_local_machine", sSandBoxToolsPath);

from fTestFileAccess import fTestFileAccess;
from fTestNetworkConnect import fTestNetworkConnect;
from fTestNetworkListen import fTestNetworkListen;
from fTestProcessAccess import fTestProcessAccess;
from fTestRegistry import fTestRegistry;
from fdsTestBinaryHardening import fdsTestBinaryHardening;
from fdsTestProcessMitigations import fdsTestProcessMitigations;
from fasTestAppContainerCapabilities import fasTestAppContainerCapabilities;
