#!/usr/bin/env bash
git submodule init
git submodule update --remote --force
chmod a+x Kill/bin/Kill_x86.exe
chmod a+x Kill/bin/Kill_x64.exe
cat <<EOF
--------------------------------------------------------------------------------
You will need to patch BugId/BugId.py to hook our checks. This is done by
adding two lines to the fNewProcessHandler function:

def fNewProcessHandler(oBugId, oProcess):
  [...old code, leave in place...]
  from fTestProcess import fTestProcess;
  fTestProcess(oBugId, oProcess);
--------------------------------------------------------------------------------
EOF