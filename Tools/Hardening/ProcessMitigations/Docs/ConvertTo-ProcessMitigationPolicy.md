---
external help file: processmitigations.dll-Help.xml
online version: 
schema: 2.0.0
---

# ConvertTo-ProcessMitigationPolicy

## SYNOPSIS
Converts an mitigation policy file formats.

## SYNTAX

```
ConvertTo-ProcessMitigationPolicy -EMETFilePath <String> -OutputFilePath <String>
```

## DESCRIPTION
Converts an EMET policy file or pinning rule file to a new Windows 10 format.

## EXAMPLES

### Example 1
```
PS C:\> ConvertTo-ProcessMitigationPolicy -EMETFilePath policy.xml -OutputFilePath result.xml
```

Converts EMET file policy.xml to result.xml, may also generate a CI file CI-result.xml if necessary.

## PARAMETERS

### -EMETFilePath
File that either contains cert pinning rules or an existing EMET process mitigation configuration file.

```yaml
Type: String
Parameter Sets: (All)
Aliases: f

Required: True
Position: Named
Default value: None
Accept pipeline input: True (ByPropertyName, ByValue)
Accept wildcard characters: False
```

### -OutputFilePath
Resulting new Windows10 process mitigation/pinning rules format.

```yaml
Type: String
Parameter Sets: (All)
Aliases: o

Required: True
Position: Named
Default value: None
Accept pipeline input: True (ByPropertyName, ByValue)
Accept wildcard characters: False
```

## INPUTS

### None

## OUTPUTS

### System.Object

## NOTES

## RELATED LINKS

