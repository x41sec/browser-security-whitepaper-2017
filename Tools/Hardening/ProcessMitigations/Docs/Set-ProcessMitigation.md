---
external help file: ProcessMitigations.dll-Help.xml
online version: 
schema: 2.0.0
---

# Set-ProcessMitigation

## SYNOPSIS
Commands to enable and disable process mitigations or set them in bulk from an XML file.

## SYNTAX

### ProcessPolicy
```
Set-ProcessMitigation [[-Name] <String>] [-Disable <String[]>] [-Enable <String[]>]
```

### FullPolicy
```
Set-ProcessMitigation -PolicyFilePath <String>
```

### SystemMode
```
Set-ProcessMitigation [-Disable <String[]>] [-Enable <String[]>] [-System]
```

## DESCRIPTION
Used to turn on and off various process mitigation settings.
Can also apply an XML file to apply settings for many processes at once.

## EXAMPLES

### Example 1
```
PS C:\>  set-ProcessMitigation -Name Notepad.exe -Enable MicrosoftSignedOnly -Disable MandatoryASLR
```

Gets the current process mitigation for "notepad.exe" from the registry and then enables MicrosoftSignedOnly, and disables MandatoryASLR.

### Example 2
```
PS C:\> set-ProcessMitigation -PolicyFilePath settings.xml
```

Sets the process mitigations from an XML file. Can be generated from get-ProcessMitigation -RegistryConfigFilePath settings.xml

### Example 3
```
PS C:\>  set-ProcessMitigation -System -Enable MicrosoftSignedOnly
```

Sets the system default to be MicrosoftSignedOnly.

Applies all settings inside settings.xml

## PARAMETERS

### -Disable
Comma separated list of mitigations to disable.
Disable list takes priority over enable list.
If specified in both, it will be disabled.

```yaml
Type: String[]
Parameter Sets: ProcessPolicy, SystemMode
Aliases: d
Accepted values: DEP, DisableATL, SEHOP, ForceRelocate, BottomUpASLR, CFG, HighEntropyASLR, StrictHandleCheck, AllowThreadOptOut, SystemCallDisable, ExtensionPointDisable, ProhibitDynamicCode, MicrosoftSignedOnly, StoreSignOnly, FontDisable, AuditNonSystemFonts, NoRemoteImages, NoLowLabel, PreferSystem32

Required: False
Position: Named
Default value: None
Accept pipeline input: False
Accept wildcard characters: False
```

### -Enable
Comma separated list of mitigations to enable.
Disable list takes priority over enable list.
If specified in both, it will be disabled.

```yaml
Type: String[]
Parameter Sets: ProcessPolicy, SystemMode
Aliases: e
Accepted values: DEP, DisableATL, SEHOP, MandatoryASLR, BottomUpASLR, CFG, HighEntropyASLR, StrictHandleCheck, AllowThreadOptOut, SystemCallDisable, ExtensionPointDisable, ProhibitDynamicCode, MicrosoftSignedOnly, StoreSignOnly, FontDisable, AuditNonSystemFonts, NoRemoteImages, NoLowLabel, PreferSystem32

Required: False
Position: Named
Default value: None
Accept pipeline input: False
Accept wildcard characters: False
```

### -Name
Name of the process to apply mitigation settings to.
Can be in the format "notepad" or "notepad.exe"

```yaml
Type: String
Parameter Sets: ProcessPolicy
Aliases: 

Required: False
Position: 0
Default value: None
Accept pipeline input: True (ByPropertyName, ByValue)
Accept wildcard characters: False
```

### -PolicyFilePath
File that contains a process mitigation policy that is to be set in the registry.

```yaml
Type: String
Parameter Sets: FullPolicy
Aliases: x

Required: True
Position: Named
Default value: None
Accept pipeline input: False
Accept wildcard characters: False
```

### -System
Sets the system process mitigation defaults.

```yaml
Type: SwitchParameter
Parameter Sets: SystemMode
Aliases: s

Required: False
Position: Named
Default value: None
Accept pipeline input: False
Accept wildcard characters: False
```

## INPUTS

### System.String

## OUTPUTS

### System.Object

## NOTES

## RELATED LINKS

