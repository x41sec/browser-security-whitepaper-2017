import re, subprocess;
from Results import fbHaveResults, fWriteResults;
from oConsole import oConsole;
# Colors used in output for various types of information:
NORMAL = -1;  # Console default color
INFO = 10;    # Light green
HILITE = 15;  # White
ERROR = 12;   # Light red

def fdsTestProcessMitigations(oProcess, sProcessType, sHardeningToolsPath):
  sTestType = "process mitigations %s" % oProcess.sBinaryName;
  if fbHaveResults(sProcessType, sTestType):
    oConsole.fPrint("Testing %s already completed" % sTestType);
    return;
  oConsole.fPrint("Testing ", INFO, sTestType, NORMAL, " for process ", INFO, str(oProcess.uId), NORMAL, \
      " running ", INFO, oProcess.sBinaryName);
  
  # Child Process Policy
  oTestProcess = subprocess.Popen(
    "POWERSHELL \"Import-Module '%s\\NtObjectManager\\NtObjectManager.psd1'; Use-NtObject($p = Get-NtProcess -ProcessId %d) { Write-Output $p.IsChildProcessRestricted };\"" % \
        (sHardeningToolsPath, oProcess.uId),
    stdout = subprocess.PIPE,
    stderr = subprocess.PIPE,
  );
  (sStdOut, sStdErr) = oTestProcess.communicate();
  assert not sStdErr, \
      "Failed:\r\n%s" % sStdErr;
  bChildProcessPolicy = None;
  for sLine in sStdOut.split("\r\n"):
    sLine = sLine.rstrip("\r").strip();
    if sLine == "": continue;
    bChildProcessPolicy = {"True": True, "False": False}.get(sLine);
    assert bChildProcessPolicy is not None, \
        "Unexpected IsChildProcessRestricted value %s" % repr(sLine);
  assert bChildProcessPolicy is not None, \
      "missing IsChildProcessRestricted value:\r\n%s" % sStdOut;
  
  # Process mitigations
  oTestProcess = subprocess.Popen(
    "POWERSHELL \"Import-Module '%s\\ProcessMitigations\\ProcessMitigations.psd1'; Get-ProcessMitigation -Id %d;\"" % \
        (sHardeningToolsPath, oProcess.uId),
    stdout = subprocess.PIPE,
    stderr = subprocess.PIPE,
  );
  (sStdOut, sStdErr) = oTestProcess.communicate();
  assert not sStdErr, \
      "Failed:\r\n%s" % sStdErr;
  dsTestResults = {
    "Child Process Policy": bChildProcessPolicy and "true" or "FALSE; CHILD PROCESSES CAN BE CREATED AT WILL",
  };
  sSubject = None;
  for sLine in sStdOut.split("\r\n"):
    sLine = sLine.rstrip("\r").strip();
    if sLine == "": continue;
    if sLine[-1] == ":":
      sSubject = sLine[:-1];
    else:
      oNameValueMatch = re.match(r"(.*?)\s*: (.+)$", sLine);
      assert oNameValueMatch, \
          "Unexpected name value pair: %s\r\n%s" % (repr(sLine), sStdOut);
      sName, sValue = oNameValueMatch.groups();
      if sSubject == "DEP":
        if sName == "Enable":
          dsTestResults["DEP enabled"] = sValue == "on" and "true" or "FALSE!";
        elif sName == "Disable ATL":
          # Take into account on x64 (https://twitter.com/epakskape/status/851783906688876544):
          if sValue == "off" and oProcess.sISA != "x64":
            dsTestResults["Disable ATL Thunk Emulation"] = "FALSE; ATL THUNKS CAN BE EXECUTED IN NON-EXECUTABLE MEMORY!";
        else:
          raise AssertionError("Unknown %s name: value pair: %s" % (sSubject, repr(sLine)));
      elif sSubject == "ASLR":
        # https://msdn.microsoft.com/en-us/library/windows/desktop/hh769086(v=vs.85).aspx
        if sName == "BottomUp":
          dsTestResults["ASLR enabled for stack & heap"] = sValue == "on" and "true" or "FALSE; STACK AND HEAP ADDRESSES ARE NOT RANDOMIZED!";
        elif sName == "HighEntropy":
          if oProcess.sISA == "x86": 
            dsTestResults["ASLR high entropy"] = "not available on x86";
          else:
            dsTestResults["ASLR high entropy"] = sValue == "on" and "true" or "FALSE; RANDOMIZATION IS LOWER THAN IT COULD BE!";
        elif sName == "ForceRelocate":
          dsTestResults["ASLR forced"] = sValue == "on" and "true; even binaries that do not opt-in are randomized" or "FALSE; BINARIES CAN OPT-OUT AND BE LOADED AT PREDICTABLE ADDRESSES!";
        elif sName == "DisallowStripped":
          dsTestResults["ASLR disallow stripped relocation"] = sValue == "on" and "true; binaries without relocation information will fail to load" or "FALSE; BINARIES WITHOUT RELOCATION INFORMATION CAN BE LOADED AT PREDICTABLE ADDRESSES!";
        else:
          raise AssertionError("Unknown %s name: value pair: %s" % (sSubject, repr(sLine)));
      elif sSubject == "StrictHandle":
        # https://msdn.microsoft.com/en-us/library/windows/desktop/hh871471(v=vs.85).aspx
        if sName == "RaiseExceptionOnInvalid":
          if "Invalid handle exceptions" not in dsTestResults:
            # This may be overwritten later when we parse "HandleExceptionsPermanently"
            dsTestResults["Invalid handle exceptions"] = sValue == "on" and "TRUE; BUT CAN BE DISABLED!" or "FALSE; INVALID HANDLES WILL NOT TERMINATE THE APPLICATION!";
        elif sName == "HandleExceptionsPermanently":
          if sValue == "on":
            dsTestResults["Invalid handle exceptions"] = "true (permanently enabled)";
        else:
          raise AssertionError("Unknown %s name: value pair: %s" % (sSubject, repr(sLine)));
      elif sSubject == "System Call":
        # https://msdn.microsoft.com/en-us/library/windows/desktop/hh871472(v=vs.85).aspx
        if sName == "DisallowWin32kSysCalls":
          dsTestResults["Disallow win32k system calls"] = sValue == "on" and "true" or "FALSE; WIN32K SYSTEM CALLS CAN BE MADE!";
        else:
          raise AssertionError("Unknown %s name: value pair: %s" % (sSubject, repr(sLine)));
      elif sSubject == "ExtensionPoint":
        # https://msdn.microsoft.com/en-us/library/windows/desktop/jj200586(v=vs.85).aspx
        if sName == "DisableExtensionPoints":
          # TODO: What does this do?
          dsTestResults["Disable Legacy Extension Point DLLs"] = sValue == "on" and "true" or "FALSE; LEGACY EXTENSION POINT DLLS CAN BE LOADED!";
        else:
          raise AssertionError("Unknown %s name: value pair: %s" % (sSubject, repr(sLine)));
      elif sSubject == "DynamicCode":
        # https://msdn.microsoft.com/en-us/library/windows/desktop/mt706243(v=vs.85).aspx
        if sName == "ProhibitDynamicCode":
          dsTestResults["ACG enabled"] = sValue == "on" and "true" or "FALSE; CODE CAN BE CREATED DYNAMICALLY!";
        elif sName == "AllowThreadOpt":
          dsTestResults["ACG: disallow thread opt-out"] = sValue == "off" and "true" or "FALSE; THREADS ARE ALLOWED TO DISABLE ACG!";
        elif sName == "AllowRemoteDowngrade":
          dsTestResults["ACG: disallow remote downgrade"] = sValue == "off" and "true" or "FALSE; ANOTHER PROCESS COULD INSERT ARBITRARY CODE!";
        else:
          raise AssertionError("Unknown %s name: value pair: %s" % (sSubject, repr(sLine)));
      elif sSubject == "CFG":
        # https://msdn.microsoft.com/en-us/library/windows/desktop/mt654121(v=vs.85).aspx
        if sName == "EnableCFG":
          dsTestResults["CFG enabled"] = sValue == "on" and "true" or "FALSE; CODE DOES NOT CHECK IF INDIRECT CALL TARGETS ARE VALID!";
        elif sName == "EnableExportSuppression":
          dsTestResults["CFG: exports are not valid CFG targets"] = sValue == "off" and "true" or "FALSE; EXPORTED FUNCTIONS ARE VALID INDIRECT CALL TARGETS!";
        elif sName == "StrictMode":
          dsTestResults["CFG forced"] = sValue == "on" and "true; binaries without CFG cannot be loaded" or "FALSE; BINARIES WITHOUT CFG CAN BE LOADED!";
        else:
          raise AssertionError("Unknown %s name: value pair: %s" % (sSubject, repr(sLine)));
      elif sSubject == "BinarySignature":
        # https://msdn.microsoft.com/en-us/library/windows/desktop/mt706242(v=vs.85).aspx
        # Note: a default value has been set above.
        if "Signature checks" not in dsTestResults:
          dsTestResults["Signature checks"] = "FALSE; ANY BINARY CAN BE LOADED INTO THE PROCESS";
        if sName == "MicrosoftSignedOnly":
          if sValue == "on":
            dsTestResults["Signature checks"] = "true (Microsoft only)";
        elif sName == "StoreSignedOnly":
          if sValue == "on":
            dsTestResults["Signature checks"] = "true (Microsoft Store only)";
        elif sName == "MitigationOptIn":
          if sValue == "on":
            dsTestResults["Signature checks"] = "true (Microsoft, Microsoft Store or WHQL only)";
        else:
          raise AssertionError("Unknown %s name: value pair: %s" % (sSubject, repr(sLine)));
      elif sSubject == "FontDisable":
        # https://msdn.microsoft.com/en-us/library/windows/desktop/mt706244(v=vs.85).aspx
        if sName == "DisableNonSystemFonts":
          dsTestResults["Disallow non-system fonts"] = sValue == "on" and "true" or "FALSE; THE PROCESS CAN ATTEMPT TO LOAD ANY FONT FILE!";
        elif sName == "AuditNonSystemFontLoading":
          # This flag just means stuff gets logged, not that it is mitigated.
          pass;
        else:
          raise AssertionError("Unknown %s name: value pair: %s" % (sSubject, repr(sLine)));
      elif sSubject == "ImageLoad":
        # https://msdn.microsoft.com/en-us/library/windows/desktop/mt706245(v=vs.85).aspx
        if sName == "NoRemoteImages":
          dsTestResults["Disallow loading remote images"] = sValue == "on" and "true" or "FALSE; THE PROCESS CAN LOAD BINARIES FROM NETWORK SHARES!";
        elif sName == "NoLowMandatoryLabelImages":
          dsTestResults["Disallow low-integrity images"] = sValue == "on" and "true" or "FALSE; THE PROCESS CAN LOAD BINARIES FROM LOW INTEGRITY FOLDERS";
        elif sName == "PreferSystem32Images":
          # This kinda protects against side-loading attacks, but I don't think it's relevant to the browser.
          pass;
        else:
          raise AssertionError("Unknown %s name: value pair: %s" % (sSubject, repr(sLine)));
  return dsTestResults;
  