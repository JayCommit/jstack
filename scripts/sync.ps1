#Requires -Version 7
<#
.SYNOPSIS
    Copy jstack skills into a target repo. Does not run git.
#>
[CmdletBinding()]
param(
    [Parameter(Mandatory = $true, Position = 0)]
    [string]$Target,

    [Parameter()]
    [string]$TargetDir = '.github/skills',

    [Parameter()]
    [string[]]$Skill,

    [Parameter()]
    [switch]$All,

    [Parameter()]
    [switch]$DryRun
)

Set-StrictMode -Version Latest
$ErrorActionPreference = 'Stop'

function Write-SyncFailure {
    param(
        [Parameter(Mandatory = $true)]
        [string]$Message
    )
    [Console]::Error.WriteLine("sync: $Message")
    exit 1
}

function Get-TreeSignature {
    param(
        [Parameter(Mandatory = $true)]
        [string]$Root
    )
    $entries = New-Object System.Collections.Generic.List[string]
    if (-not (Test-Path -LiteralPath $Root)) {
        return $entries
    }
    $fullRoot = [System.IO.Path]::GetFullPath($Root)
    $separator = [System.IO.Path]::DirectorySeparatorChar
    if (-not $fullRoot.EndsWith($separator)) {
        $fullRoot = $fullRoot + $separator
    }
    $items = @(Get-ChildItem -LiteralPath $fullRoot -Recurse -Force)
    foreach ($item in $items) {
        $relative = $item.FullName.Substring($fullRoot.Length).Replace('\', '/')
        if ($item.PSIsContainer) {
            $entries.Add("dir:$relative")
        }
        else {
            $hash = (Get-FileHash -LiteralPath $item.FullName -Algorithm SHA256).Hash
            $entries.Add("file:${relative}:$hash")
        }
    }
    return $entries
}

$RepoRoot = Split-Path -Parent $PSScriptRoot
$SkillsRoot = Join-Path $RepoRoot 'skills'

if (-not (Test-Path -LiteralPath $Target -PathType Container)) {
    Write-SyncFailure "not a directory: $Target"
}
if (-not (Test-Path -LiteralPath $SkillsRoot -PathType Container)) {
    Write-SyncFailure "skills directory not found: $SkillsRoot"
}
if ([string]::IsNullOrWhiteSpace($TargetDir) -or [System.IO.Path]::IsPathRooted($TargetDir)) {
    Write-SyncFailure '--target dir must be a relative path'
}

$skillPassed = $null -ne $Skill -and $Skill.Count -gt 0
if ($All -and $skillPassed) {
    Write-SyncFailure 'do not pass -Skill with -All'
}
if (-not $All -and -not $skillPassed) {
    Write-SyncFailure 'specify -All or at least one skill'
}

$allNames = @(
    Get-ChildItem -LiteralPath $SkillsRoot -Directory |
        Select-Object -ExpandProperty Name |
        Sort-Object
)

$selected = New-Object System.Collections.Generic.List[string]
if ($All) {
    foreach ($name in $allNames) {
        $selected.Add($name)
    }
}
else {
    foreach ($pattern in $Skill) {
        $matched = @($allNames | Where-Object { $_ -clike $pattern })
        if ($matched.Count -eq 0) {
            Write-SyncFailure "skill not found: $pattern"
        }
        foreach ($name in $matched) {
            if (-not $selected.Contains($name)) {
                $selected.Add($name)
            }
        }
    }
}

foreach ($name in $selected) {
    $source = Join-Path $SkillsRoot $name
    $skillFile = Join-Path $source 'SKILL.md'
    if (-not (Test-Path -LiteralPath $skillFile -PathType Leaf)) {
        Write-SyncFailure "skill not found: $name"
    }

    $destination = Join-Path (Join-Path $Target $TargetDir) $name
    $destinationExists = Test-Path -LiteralPath $destination
    $destinationIsDir = Test-Path -LiteralPath $destination -PathType Container
    if ($destinationExists -and -not $destinationIsDir) {
        $status = 'update'
    }
    elseif (-not $destinationExists) {
        $status = 'create'
    }
    else {
        $sourceSignature = (@(Get-TreeSignature -Root $source) | Sort-Object) -join "`n"
        $destinationSignature = (@(Get-TreeSignature -Root $destination) | Sort-Object) -join "`n"
        if ($sourceSignature -eq $destinationSignature) {
            $status = 'unchanged'
        }
        else {
            $status = 'update'
        }
    }

    if (-not $DryRun -and $status -ne 'unchanged') {
        if ($destinationExists) {
            Remove-Item -LiteralPath $destination -Recurse -Force
        }
        $parent = Split-Path -Parent $destination
        if (-not (Test-Path -LiteralPath $parent)) {
            New-Item -ItemType Directory -Path $parent -Force | Out-Null
        }
        New-Item -ItemType Directory -Path $destination -Force | Out-Null
        $children = @(Get-ChildItem -LiteralPath $source -Force)
        foreach ($child in $children) {
            Copy-Item -LiteralPath $child.FullName -Destination (Join-Path $destination $child.Name) -Recurse -Force
        }
    }

    Write-Output "$status $name"
}
