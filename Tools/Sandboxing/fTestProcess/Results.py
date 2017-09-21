import os;

def fbHaveResults(sProcessType, sTestType):
  # Returns true if we have already got results for this process and test type.
  return (
    os.path.isfile(r"Results\%s\%s test.txt" % (sProcessType, sTestType))
    or os.path.isfile(r"Results\%s\Passed %s test.txt" % (sProcessType, sTestType))
    or os.path.isfile(r"Results\%s\Failed %s test.txt" % (sProcessType, sTestType))
  );

def fWriteResults(sProcessType, sTestType, bSuccess, sMessage = ""):
  # Save results for this process and test type.
  if bSuccess is None:
    sFilePath = r"Results\%s\%s test.txt" % (sProcessType, sTestType);
  elif bSuccess is True:
    sFilePath = r"Results\%s\Passed %s test.txt" % (sProcessType, sTestType);
  else:
    sFilePath = r"Results\%s\Failed %s test.txt" % (sProcessType, sTestType);
  open(sFilePath, "wb").write(sMessage);
