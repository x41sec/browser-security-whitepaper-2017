---
external help file: ProcessMitigations.dll-Help.xml
online version: 
schema: 2.0.0
---

# Get-ProcessMitigation

## SYNOPSIS
Gets the current process mitigation settings, either from the registry, from a running process, or saves all to a XML.

## SYNTAX

### NameMode
```
Get-ProcessMitigation [-Name] <String> [-RunningProcesses]
```

### IdMode
```
Get-ProcessMitigation [-Id] <Int32[]>
```

### SaveMode
```
Get-ProcessMitigation [-RegistryConfigFilePath <String>]
```

### SystemMode
```
Get-ProcessMitigation [-System]
```

### FullPolicy
```
Get-ProcessMitigation [-FullPolicy]
```

## DESCRIPTION
Gets all process mitigation settings either by process name (either running or from -Registry), or by process ID.
Can also save all settings to an XML file.

## EXAMPLES

### Example 1
```
PS C:\> Get-ProcessMitigation -Name notepad.exe -RunningProcess
```

Gets the current settings on all running instances of notepad.exe

### Example 2
```
PS C:\> Get-ProcessMitigation -Name notepad.exe
```

Gets the current settings in the registry for notepad.exe

### Example 3
```
PS C:\> Get-ProcessMitigation -Id 1304
```

Gets the current settings for the running process with pid 1304

### Example 4
```
PS C:\> Get-ProcessMitigation -RegistryConfigFilePath settings.xml
```

Gets the all process mitigation settings from the registry and saves them to the xml file settings.xml

### Example 5
```
PS C:\> Get-ProcessMitigation -FullPolicy
```

Gets all policies for all processes set in the registry.

### Example 6
```
PS C:\> Get-ProcessMitigation -System
```

Gets the current system process mitigation defaults stored in the registry.

### Example 7
```
PS C:\> Get-Process notepad | Get-ProcessMitigation 
```

Gets the current process mitigation settings for all running instances of notepad.exe

## PARAMETERS

### -Id
Process Id to retrieve current running process mitigation settings from

```yaml
Type: Int32[]
Parameter Sets: IdMode
Aliases: 

Required: True
Position: 0
Default value: None
Accept pipeline input: True (ByPropertyName, ByValue)
Accept wildcard characters: False
```

### -Name
Current process name to get current running (Or from registry) process mitigation settings from one (Can be more than one instance)

```yaml
Type: String
Parameter Sets: NameMode
Aliases: n

Required: True
Position: 0
Default value: None
Accept pipeline input: False
Accept wildcard characters: False
```

### -FullPolicy
Returns every processes' current mitigation settings in the registry

```yaml
Type: SwitchParameter
Parameter Sets: FullPolicy
Aliases: f

Required: False
Position: Named
Default value: None
Accept pipeline input: False
Accept wildcard characters: False
```

### -RegistryConfigFilePath
File to save the current registry process mitigation configuration to

```yaml
Type: String
Parameter Sets: SaveMode
Aliases: o

Required: False
Position: Named
Default value: None
Accept pipeline input: False
Accept wildcard characters: False
```

### -RunningProcesses
Pull the current process mitigation settings from a running instance instead of the registry.

```yaml
Type: SwitchParameter
Parameter Sets: NameMode
Aliases: r

Required: False
Position: Named
Default value: None
Accept pipeline input: False
Accept wildcard characters: False
```

### -System
Pulls the current system defaults for process mitigations.

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
System.Int32\[\]

## OUTPUTS

### System.Object

## NOTES

## RELATED LINKS

