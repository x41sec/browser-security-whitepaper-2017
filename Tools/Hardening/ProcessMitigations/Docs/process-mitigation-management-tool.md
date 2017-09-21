# Process Mitigation Management Tool

The Process Mitigation Management Tool provides functionalities to allow users to configure and audit exploit mitigations for increased process security or for continued enforcement of EMET policy settings.

## Exploit Mitigations

The Process Mitigation Management Tool offers six new functionalities (Enumerate, Enable, Disable, Save, Apply, Convert) to cover basic settings configuration for the following Windows 10 exploit mitigations: 

1.	DEP (configurable via EMET)
2.	DEPATL
3.	SEHOP (configurable via EMET)
4.	MandatoryASLR (configurable via EMET)
5.	BottomUpASLR (configurable via EMET)
6.	HighEntropyASLR
7.	CFG
8.	NoRemoteImages
9.	NoLowLabel
10.	PreferSystem32
11.	FontDisable (configurable via EMET)
12.	AuditNonSysFonts
13.	MicrosoftSignedOnly
14.	StoreSignOnly
15.	ExtensionPointDisable
16.	SystemCallDisable
17.	StrictHandleCheck
18.	ProhibitDynamicCode
19.	AllowThreadOptOut

## Functionalities

The **Enumerate** functionality generates a list of running process mitigation settings or a list of registry mitigation settings for a particular process, which the user specifies by process name or process ID. 
The **Enable** and **Disable** functionalities respectively enable and disable registry settings for a process mitigation.

### Examples

| Sample usage |  Sample PowerShell |
|--------------|--------------------|
| **Enumerate** running process settings for a Notepad instance based on process name. |  Get-ProcessMitigation -Name notepad.exe |
| **Enumerate** registry settings for Notepad based on process name. | Get-ProcessMitigation -Name notepad.exe -Registry |
| **Enumerate** running process settings for a Notepad instance based on process ID. | Get-ProcessMitigation -Id 1304 |
| **Enable** SEHOP and **disable** MandatoryASLR and DEPATL registry settings for Notepad. | Set-ProcessMitigation -Name notepad.exe -Enable SEHOP -Disable MandatoryASLR,DEPATL |
| **Save** registry settings (process mitigation policy) for all supported process mitigations. | Get-ProcessMitigation -Save settings.xml |
| **Apply** registry settings (process mitigation policy) for all supported process mitigations. | Set-ProcessMitigation -File settings.xml |
| **Convert** from EMET policy settings to registry settings (process mitigation policy) for relevant process mitigations.| ConvertTo-ProcessMitigationPolicy -EMETfile emetpolicy.xml -output newconfiguration.xml |

## Caveats

- Windows 10 systems will still enforce certain high-value protections (DEP, CFG, etc.) for most/all processes, even if these mitigations have been disabled in registry settings (process mitigation policy) by the user.
- The **Enumerate** functionality’s result for the SEHOP mitigation setting is unreliable.
- The **Convert** functionality, when given an EMET policy file as input, ignores any ASR rules in the EMET policy that contain module wildcards, as well as any mitigation settings in the EMET policy for which there is no Windows 10 counterpart.
