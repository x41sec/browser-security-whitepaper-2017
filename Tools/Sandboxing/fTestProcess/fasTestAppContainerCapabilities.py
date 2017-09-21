import re, subprocess;
from Results import fbHaveResults, fWriteResults;
# The following file should be in the root test directory and is automatically generated.
from ddsCapabilityDetails_by_sName import ddsCapabilityDetails_by_sName;
from oConsole import oConsole;
# Colors used in output for various types of information:
NORMAL = -1;  # Console default color
INFO = 10;    # Light green
HILITE = 15;  # White
ERROR = 12;   # Light red

# Create a reverse lookup table for Capablity SID -> Name
dsCapabilityName_by_sSID = {}
for (sName, dsCapabilityDetails) in ddsCapabilityDetails_by_sName.items():
  sSID = dsCapabilityDetails["sSID"];
  dsCapabilityName_by_sSID[sSID] = sName;

def fasTestAppContainerCapabilities(oProcess, sHardeningToolsPath):
  sCommand = "POWERSHELL \"Import-Module '%s\\NtObjectManager\\NtObjectManager.psd1'; Use-NtObject($token = Get-NtToken -Primary -ProcessId %d) { foreach ($cap in $token.Capabilities) { Write-Output ('{0} {1}' -f ($cap.Sid, $cap.Sid.Name)) } };\"" % \
        (sHardeningToolsPath, oProcess.uId);
  oTestProcess = subprocess.Popen(
    sCommand,
    stdout = subprocess.PIPE,
    stderr = subprocess.PIPE,
  );
  (sStdOut, sStdErr) = oTestProcess.communicate();
  assert not sStdErr, \
      "Failed:\r\n%s" % sStdErr;
  asKnownSIDs = [];
  asNamedSIDs = [];
  asRemainingSIDs = [];
  # Each line should contain a SID
  for sLine in sStdOut.split("\r\n"):
    sLine = sLine.rstrip("\r").strip();
    if sLine == "": continue; # empty lines are ignored.
    sSID, sQualifiedName = sLine.split(" ", 1);
    sName = dsCapabilityName_by_sSID.get(sSID);
    if sName:
      asKnownSIDs.append(sName);
      asKnownSIDs.append("  = %s" % sQualifiedName);
      asKnownSIDs.append("  = %s" % sSID);
    elif sSID != sQualifiedName:
      asNamedSIDs.append(sQualifiedName);
      asNamedSIDs.append("  = %s" % sSID);
    else:
      asRemainingSIDs.append(sSID);
  return asKnownSIDs + asNamedSIDs + asRemainingSIDs;
  