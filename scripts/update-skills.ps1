# ==============================================================================
# Antigravity Skills & Plugins Auto-Updater + Repo Sync Tool (Windows Local)
# ==============================================================================
# Usage:
#   update-skills                                   # Update all Git repos & optimize SKILL.md
#   update-skills -AddRepo https://github.com/u/r   # Add a new skill repo to manifest & install
#   update-skills -PushHub                          # Push local custom skills & manifest to GitHub Hub
#   update-skills -Status                           # Show repo status & skill counts
# ==============================================================================

[CmdletBinding()]
param (
    [string]$AddRepo = "",
    [string]$Name = "",
    [switch]$PushHub,
    [switch]$Status,
    [switch]$Force,
    [switch]$Quiet
)

[Console]::OutputEncoding = [System.Text.Encoding]::UTF8
$OutputEncoding = [System.Text.Encoding]::UTF8
$ErrorActionPreference = "Continue"
$env:GIT_TERMINAL_PROMPT = "0"

$Utf8NoBom = [System.Text.UTF8Encoding]::new($false)
$GlobalConfigDir = "$HOME\.gemini\config"
$PluginsDir = Join-Path $GlobalConfigDir "plugins"
$GlobalSkillsDir = Join-Path $GlobalConfigDir "skills"
$ManifestPath = Join-Path $GlobalConfigDir "import_manifest.json"
$ConfigJsonPath = Join-Path $GlobalConfigDir "config.json"
$StateFile = Join-Path $GlobalConfigDir "last_skills_update.json"
$LogsDir = Join-Path $GlobalConfigDir "logs"
$LogFile = Join-Path $LogsDir "skill-updates.log"
$Timestamp = (Get-Date).ToString("yyyy-MM-dd HH:mm:ss")

foreach ($d in @($PluginsDir, $GlobalSkillsDir, $LogsDir)) {
    if (-not (Test-Path $d)) { New-Item -ItemType Directory -Path $d -Force | Out-Null }
}

function Write-Utf8File {
    param([string]$Path, [string]$Content)
    [System.IO.File]::WriteAllText($Path, $Content, $Utf8NoBom)
}

function Write-Log {
    param([string]$Message, [string]$Level = "INFO")
    $LogLine = "[$Timestamp] [$Level] $Message"
    [System.IO.File]::AppendAllText($LogFile, "$LogLine`r`n", $Utf8NoBom)
    if (-not $Quiet) {
        switch ($Level) {
            "SUCCESS" { Write-Host $Message -ForegroundColor Green }
            "WARN"    { Write-Host $Message -ForegroundColor Yellow }
            "ERROR"   { Write-Host $Message -ForegroundColor Red }
            default   { Write-Host $Message -ForegroundColor Cyan }
        }
    }
}

# 0. Status view (-Status)
if ($Status) {
    if (Test-Path $StateFile) {
        $st = Get-Content $StateFile -Raw -Encoding UTF8 | ConvertFrom-Json
        Write-Host "=== ANTIGRAVITY SKILLS STATUS ===" -ForegroundColor Cyan
        Write-Host "Last Updated : $($st.last_updated)"
        Write-Host "Total Skills : $($st.valid_skills) / $($st.total_skills) valid"
        Write-Host "Health       : $($st.status)"
        Write-Host "`nGit Plugin Repositories:" -ForegroundColor Yellow
        $st.git_plugins | Format-Table name, branch, commit, remote -AutoSize
    } else {
        Write-Host "No update state found. Run: update-skills" -ForegroundColor Yellow
    }
    return
}

# Read import_manifest.json
$Manifest = if (Test-Path $ManifestPath) {
    Get-Content $ManifestPath -Raw -Encoding UTF8 | ConvertFrom-Json
} else {
    [PSCustomObject]@{ hubRepo = "https://github.com/ROYCE-8425/antigravity-skills-hub.git"; imports = @() }
}

# 0.5 Add new Repo (-AddRepo)
if ($AddRepo) {
    $CleanUrl = $AddRepo.Trim()
    if (-not $CleanUrl.EndsWith(".git")) { $CleanUrl = "$CleanUrl.git" }
    if (-not $Name) {
        $Name = ([System.IO.Path]::GetFileNameWithoutExtension($CleanUrl)).ToLower()
    }
    Write-Log "Adding new repository '$Name' ($CleanUrl) to import_manifest.json..." "INFO"
    $Existing = $Manifest.imports | Where-Object { $_.name -eq $Name }
    if (-not $Existing) {
        $NewEntry = [PSCustomObject]@{
            name       = $Name
            source     = $CleanUrl
            branch     = "main"
            components = @("skills")
            pluginJson = [PSCustomObject]@{
                name        = $Name
                displayName = $Name
                version     = "1.0.0"
                description = "Auto-synced skill plugin from $CleanUrl"
            }
        }
        $Manifest.imports += $NewEntry
        Write-Utf8File -Path $ManifestPath -Content ($Manifest | ConvertTo-Json -Depth 6)
        Write-Log "Added '$Name' to import_manifest.json!" "SUCCESS"
    }
}

Write-Log "========== STARTING ANTIGRAVITY AGENT SKILLS SYNC =========="

# 1. Ensure all repos in import_manifest.json are cloned in ~/.gemini/config/plugins/
if ($Manifest.imports) {
    foreach ($Item in $Manifest.imports) {
        $TargetDir = Join-Path $PluginsDir $Item.name
        $TargetGit = Join-Path $TargetDir ".git"
        if (-not (Test-Path $TargetGit)) {
            Write-Log "Cloning missing plugin from manifest: $($Item.name) ($($Item.source))..." "WARN"
            if (Test-Path $TargetDir) { Remove-Item -Path $TargetDir -Recurse -Force -ErrorAction SilentlyContinue }
            git clone --depth 1 $Item.source $TargetDir 2>&1 | Out-Null
            Write-Log "Cloned $($Item.name) successfully!" "SUCCESS"
        }
    }
}

# 2. Scan and update all Git-backed plugins in ~/.gemini/config/plugins/
$UpdatedPlugins = @()
if (Test-Path $PluginsDir) {
    $PluginDirs = Get-ChildItem -Path $PluginsDir -Directory
    foreach ($Plugin in $PluginDirs) {
        $GitDir = Join-Path $Plugin.FullName ".git"
        if (Test-Path $GitDir) {
            Write-Log "Checking Git plugin: $($Plugin.Name)..."
            try {
                $CurrentBranch = (git -C $Plugin.FullName rev-parse --abbrev-ref HEAD 2>$null).Trim()
                if (-not $CurrentBranch -or $CurrentBranch -eq "HEAD") { $CurrentBranch = "main" }

                # Save existing plugin.json before git reset
                $PluginJsonPath = Join-Path $Plugin.FullName "plugin.json"
                $SavedPluginJson = if (Test-Path $PluginJsonPath) { Get-Content $PluginJsonPath -Raw -Encoding UTF8 } else { $null }

                # Fetch latest commits from origin
                git -C $Plugin.FullName fetch origin $CurrentBranch 2>$null | Out-Null
                $LocalSha = (git -C $Plugin.FullName rev-parse HEAD 2>$null).Trim()
                $RemoteSha = (git -C $Plugin.FullName rev-parse "origin/$CurrentBranch" 2>$null).Trim()

                if ($LocalSha -and $RemoteSha -and ($LocalSha -ne $RemoteSha)) {
                    $DiffCount = (git -C $Plugin.FullName rev-list "HEAD..origin/$CurrentBranch" --count 2>$null)
                    Write-Log "Update found for $($Plugin.Name) ($DiffCount new commits). Syncing..." "WARN"
                    git -C $Plugin.FullName reset --hard "origin/$CurrentBranch" 2>$null | Out-Null
                    $NewSha = (git -C $Plugin.FullName rev-parse --short HEAD 2>$null).Trim()
                    Write-Log "Updated $($Plugin.Name) to latest commit ($NewSha)!" "SUCCESS"
                } else {
                    git -C $Plugin.FullName reset --hard HEAD 2>$null | Out-Null
                    $ShortSha = if ($LocalSha.Length -ge 7) { $LocalSha.Substring(0, 7) } else { $LocalSha }
                    Write-Log "$($Plugin.Name) is up to date ($CurrentBranch @ $ShortSha)." "INFO"
                }

                # Restore plugin.json from import_manifest.json or saved copy
                $ManifestEntry = $Manifest.imports | Where-Object { $_.name -eq $Plugin.Name } | Select-Object -First 1
                if ($ManifestEntry -and $ManifestEntry.pluginJson) {
                    Write-Utf8File -Path $PluginJsonPath -Content ($ManifestEntry.pluginJson | ConvertTo-Json -Depth 5)
                } elseif ($SavedPluginJson) {
                    Write-Utf8File -Path $PluginJsonPath -Content $SavedPluginJson
                } elseif (-not (Test-Path $PluginJsonPath)) {
                    $DefaultPj = @{ name = $Plugin.Name; displayName = $Plugin.Name; version = "1.0.0" } | ConvertTo-Json
                    Write-Utf8File -Path $PluginJsonPath -Content $DefaultPj
                }

                # Stage hooks/hooks.json -> hooks.json at plugin root if needed
                $SubHooks = Join-Path $Plugin.FullName "hooks\hooks.json"
                $RootHooks = Join-Path $Plugin.FullName "hooks.json"
                if ((Test-Path $SubHooks) -and -not (Test-Path $RootHooks)) {
                    Copy-Item -Path $SubHooks -Destination $RootHooks -Force
                }

                $FinalSha = (git -C $Plugin.FullName rev-parse --short HEAD 2>$null).Trim()
                $RemoteUrl = (git -C $Plugin.FullName config --get remote.origin.url 2>$null).Trim()
                $UpdatedPlugins += [PSCustomObject]@{
                    name   = $Plugin.Name
                    branch = $CurrentBranch
                    commit = $FinalSha
                    remote = $RemoteUrl
                }
            } catch {
                Write-Log "Error updating $($Plugin.Name): $_" "ERROR"
            }
        }
    }
}

# 3. Validate SKILL.md & optimize Context Budget (UTF-8 without BOM, description <= 160 chars)
Write-Log "Validating SKILL.md files and optimizing Context Budget..."
$TotalSkills = 0
$ValidSkills = 0

$SearchDirs = @($PluginsDir, $GlobalSkillsDir) | Where-Object { Test-Path $_ }
$AllSkills = Get-ChildItem -Path $SearchDirs -Recurse -Filter "SKILL.md" -ErrorAction SilentlyContinue
foreach ($SkillFile in $AllSkills) {
    $TotalSkills++
    $Content = [System.IO.File]::ReadAllText($SkillFile.FullName, [System.Text.Encoding]::UTF8).TrimStart([char]0xFEFF)
    if ($Content -match "(?s)^---\s*\r?\n(.*?)\r?\n---\s*\r?\n(.*)$") {
        $Frontmatter = $Matches[1]
        $Body = $Matches[2]
        if ($Frontmatter -match "description:" -and $Frontmatter -match "(?m)^name:\s*([^\r\n]+)") {
            $ValidSkills++
            $SkillName = ($Matches[1] -replace "^[`"']|[`"']$", "").Trim()
            $Desc = ""
            if ($Frontmatter -match "(?ms)^description:\s*[>|][-+]?\s*\r?\n((?:[ \t]+[^\r\n]+\r?\n?)+)") {
                $Desc = ($Matches[1] -replace "\r?\n\s*", " ").Trim(" `"'`r`n`t")
            } elseif ($Frontmatter -match "(?m)^description:\s*(.+)$") {
                $Desc = $Matches[1].Trim(" `"'`r`n`t")
            }
            if ($Frontmatter.Length -gt 240 -or $Desc.Length -gt 160) {
                if ($Desc.Length -gt 160) {
                    $Cut = $Desc.Substring(0, 155)
                    $LastDot = $Cut.LastIndexOf(". ")
                    if ($LastDot -gt 70) { $Desc = $Cut.Substring(0, $LastDot + 1) }
                    else {
                        $LastSpace = $Cut.LastIndexOf(" ")
                        if ($LastSpace -gt 70) { $Desc = $Cut.Substring(0, $LastSpace) + "..." }
                        else { $Desc = $Cut + "..." }
                    }
                }
                $DescSafe = ($Desc -replace '"', "'") -replace "\r?\n", " "
                $NewFm = "name: $SkillName`n" + "description: `"$DescSafe`""
                Write-Utf8File -Path $SkillFile.FullName -Content "---`n$NewFm`n---`n`n$Body"
            }
        }
    }
}
Write-Log "Validated: $ValidSkills/$TotalSkills SKILL.md files (Context Budget optimized)." "SUCCESS"

# 4. Sync to GitHub Hub (-PushHub) if requested
if ($PushHub -and $Manifest.hubRepo) {
    $HubDir = Join-Path $GlobalConfigDir "hub-sync"
    Write-Log "Syncing Custom Skills and Scripts to GitHub Hub ($($Manifest.hubRepo))..." "INFO"
    if (-not (Test-Path (Join-Path $HubDir ".git"))) {
        if (Test-Path $HubDir) { Remove-Item $HubDir -Recurse -Force }
        git clone $Manifest.hubRepo $HubDir 2>$null | Out-Null
    } else {
        git -C $HubDir pull --rebase origin main 2>$null | Out-Null
    }
    if (Test-Path $HubDir) {
        Copy-Item -Path $ManifestPath -Destination (Join-Path $HubDir "import_manifest.json") -Force
        Robocopy $GlobalSkillsDir (Join-Path $HubDir "skills") /MIR /XD ".git" "__pycache__" "node_modules" /NFL /NDL /NJH /NJS | Out-Null
        foreach ($CustomPlugin in @("custom-skills", "production-engineering-skills", "anthropic-agent-skills")) {
            $SrcP = Join-Path $PluginsDir $CustomPlugin
            if (Test-Path $SrcP) {
                Robocopy $SrcP (Join-Path $HubDir "plugins\$CustomPlugin") /MIR /XD ".git" "__pycache__" "node_modules" /NFL /NDL /NJH /NJS | Out-Null
            }
        }
        Robocopy (Join-Path $GlobalConfigDir "scripts") (Join-Path $HubDir "scripts") /MIR /NFL /NDL /NJH /NJS | Out-Null
        git -C $HubDir add -A
        $HasChanges = git -C $HubDir status --porcelain
        if ($HasChanges) {
            git -C $HubDir commit -m "chore(skills): auto-sync custom skills and manifest ($Timestamp)" | Out-Null
            git -C $HubDir push origin main | Out-Null
            Write-Log "Pushed latest custom skills & manifest to GitHub Hub!" "SUCCESS"
        } else {
            Write-Log "GitHub Hub is already up to date." "INFO"
        }
    }
}

# 5. Save completion state
$StateData = [ordered]@{
    last_updated = $Timestamp
    total_skills = $TotalSkills
    valid_skills = $ValidSkills
    git_plugins  = $UpdatedPlugins
    status       = "healthy"
} | ConvertTo-Json -Depth 4
Write-Utf8File -Path $StateFile -Content $StateData

Write-Log "========== COMPLETED SKILLS SYNC AT $Timestamp ==========" "SUCCESS"
