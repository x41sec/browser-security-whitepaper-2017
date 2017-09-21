import os, re, subprocess;
from Results import fbHaveResults, fWriteResults;
from oConsole import oConsole;
# Colors used in output for various types of information:
NORMAL = -1;  # Console default color
INFO = 10;    # Light green
HILITE = 15;  # White
ERROR = 12;   # Light red

gdsBinaryHardeningTestResultsCache_by_sPath = {};

def fdsTestBinaryHardening(oProcess, sProcessType, oModule, sHardeningToolsPath):
  if oModule.sBinaryPath in gdsBinaryHardeningTestResultsCache_by_sPath:
    return gdsBinaryHardeningTestResultsCache_by_sPath[oModule.sBinaryPath];
  sTestType = "binary hardening %s" % oModule.sBinaryName;
  oConsole.fPrint("Testing binary hardening for ", INFO, oModule.sBinaryName, NORMAL, " for process ", INFO, str(oProcess.uId), NORMAL, " running ", INFO, oProcess.sBinaryName);
  if oModule.sBinaryPath is None:
    fWriteResults(sProcessType, sTestType, False, "The file path could not be determined.");
    return
  if not os.path.isfile(oModule.sBinaryPath):
    oConsole.fPrint(ERROR, "ERROR: the file ", oModule.sBinaryPath, " was not found!");
    fWriteResults(sProcessType, sTestType, False, "The file %s was not found!?" % oModule.sBinaryPath);
    return;
  oTestProcess = subprocess.Popen(
    "POWERSHELL \"Import-Module '%s\\PESecurity\\Get-PESecurity.psm1'; Get-PESecurity -File '%s';\"" % (sHardeningToolsPath, oModule.sBinaryPath),
    stdout = subprocess.PIPE,
    stderr = subprocess.PIPE,
  );
  (sStdOut, sStdErr) = oTestProcess.communicate();
  assert not sStdErr, "Failed:\r\n%s" % sStdErr;
  dsPESecurityOutput = {};
  for sLine in sStdOut.split("\n"):
    oMatch = re.match(r"(\w+)\s*: (.+)", sLine.rstrip("\r"));
    if oMatch:
      sName, sValue = oMatch.groups();
      dsPESecurityOutput[sName] = sValue;
  dsTestResults = {};
  dsTestResults["ASLR enabled"] = dsPESecurityOutput["ASLR"] == "True" and "true" or "FALSE!";
  if dsPESecurityOutput["ARCH"] != "I386":
    dsTestResults["ASLR high entropy"] = dsPESecurityOutput["HighentropyVA"] == "True" and "true" or "FALSE!";
  dsTestResults["DEP enabled"] = {"True": "true", "False": "FALSE!", "N/A": "n/a"}[dsPESecurityOutput["DEP"]]
  dsTestResults["Authenticode enabled"] = {"True": "true", "False": "FALSE!", "N/A": "n/a"}[dsPESecurityOutput["Authenticode"]];
  dsTestResults["SafeSEH enabled"] = {"True": "true", "False": "FALSE!", "N/A": "n/a"}[dsPESecurityOutput["SafeSEH"]];
  dsTestResults["CFG enabled"] = {"True": "true", "False": "FALSE!", "N/A": "n/a"}[dsPESecurityOutput["CFG"]];
  oConsole.fStatus("Testing MemGC for ", INFO, oModule.sBinaryName, NORMAL, " for process ", INFO, str(oProcess.uId), NORMAL, " running ", INFO, oProcess.sBinaryName);
  # MemGC
  bMemGCEnabled = oModule.oProcess.fuGetValue("%s!MemoryProtection::HeapFree" % oModule.sCdbId, "Attempt to detect MemGC") is not None;
  dsTestResults["MemGC enabled"] = bMemGCEnabled and "true" or "FALSE!";
  oConsole.fStatus("Testing VTGuard for ", INFO, oModule.sBinaryName, NORMAL, " for process ", INFO, str(oProcess.uId), NORMAL, " running ", INFO, oProcess.sBinaryName);
  # VTGuard
  uVTGuardValue = (
    oModule.oProcess.fuGetValue("%s!_vtguard" % oModule.sCdbId, "Attempt to detect VTGuard")
    or oModule.oProcess.fuGetValue("%s!__vtguard" % oModule.sCdbId, "Attempt to detect VTGuard")
  );
  if uVTGuardValue is None:
    dsTestResults["VTGuard enabled"] = "FALSE!";
  else:
    asSearchResults = oModule.oProcess.fasExecuteCdbCommand(
      sCommand = "s -%s 0x%X 0x%X 0x%X" % (oModule.sISA == "x86" and "d" or "q", oModule.uStartAddress, oModule.uEndAddress, uVTGuardValue),
      sComment = "Look for references to %s!_vtguard" % oModule.sCdbId,
    );
    asProtectedClasses = set();
    for sLine in asSearchResults:
      oMatch = re.match(r"^([0-9`a-f]+)\s+([0-9`a-f]+)\s+.*", sLine, re.I);
      assert oMatch, \
          "Unexpected search output: %s\r\n%s" % (repr(sLine), "\r\n".join(asSearchResults));
      sVTGuardAddress, sVTGuardValueCheck = oMatch.groups();
      assert long(sVTGuardValueCheck.replace("`", ""), 16) == uVTGuardValue, \
          "Unexpected search output (value !=0x%X): %s\r\n%s" % (uVTGuardValue, repr(sLine), "\r\n".join(asSearchResults));
      uVTGuardAddress = long(sVTGuardAddress.replace("`", ""), 16);
      asSymbolResults = oModule.oProcess.fasExecuteCdbCommand(
        sCommand = "ln 0x%X" % uVTGuardAddress,
        sComment = "Try to detect VTGuard",
      );
      oSymbolMatch = re.match(r"^\(([0-9`a-f]+)\)\s+(\w+!.+?)(?:\+0x[0-9a-f]+)?\s+\|.*", asSymbolResults[0], re.I);
      assert oSymbolMatch, \
          "Unexpected symbol output:\r\n%s" % "\r\n".join(asSymbolResults);
      sSymbolAddress, sSymbol = oSymbolMatch.groups();
      if sSymbol.endswith("::`vftable'"):
        asProtectedClasses.add(sSymbol);
      if len(asSymbolResults) >= 2 and asSymbolResults[1] == "Exact matches:":
        uClassCount = 0;
        # exact match; multiple classes are possible
        for uIndex in xrange(2, len(asSymbolResults)):
          oSymbolMatch = re.match(r"^\s+(\w+!.+?) = .+", asSymbolResults[uIndex], re.I);
          assert oSymbolMatch, \
              "Unrecognized symbol output line %d: %s\r\n%s" % (uIndex + 1, repr(asSymbolResults[uIndex]), "\r\n".join(asSymbolResults));
          sSymbol = oSymbolMatch.group(1);
          if sSymbol.endswith("::`vftable'"):
            asProtectedClasses.add(sSymbol);
    asClassesResult = set(oModule.oProcess.fasExecuteCdbCommand(
      sCommand = "x %s!*::`vftable';" % oModule.sCdbId,
      sComment = "Enumerate classes",
    ));
    for sLine in asClassesResult:
      assert re.match(r"^[0-9`a-f]+\s+%s!.*" % oModule.sCdbId, sLine, re.I), \
          "Unrecognized classes output: %s\r\n%s" % (repr(sLine), "\r\n".join(asClassesResult));
    uTotalClassesCount = len(asClassesResult);
    dsTestResults["VTGuard enabled"] = "true (in %d/%d classes; %.1f%% coverage)" % \
        (len(asProtectedClasses), uTotalClassesCount, len(asProtectedClasses) * 100.0 / uTotalClassesCount);
  gdsBinaryHardeningTestResultsCache_by_sPath[oModule.sBinaryPath] = dsTestResults;
  return dsTestResults;