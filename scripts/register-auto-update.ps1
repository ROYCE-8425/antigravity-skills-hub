# ==============================================================================
# Dang ky Windows Task Scheduler tu dong cap nhat Antigravity Agent Skills
# ==============================================================================

[Console]::OutputEncoding = [System.Text.Encoding]::UTF8
$TaskName = "AntigravitySkillsAutoUpdate"
$HomeDir = [System.Environment]::GetFolderPath([System.Environment+SpecialFolder]::UserProfile)
$ScriptPath = Join-Path $HomeDir ".gemini\config\scripts\update-skills.ps1"

Write-Host "--- Thiet lap tu dong cap nhat Antigravity Skills (Windows Task Scheduler) ---" -ForegroundColor Cyan

# Kiem tra xem Task da ton tai chua
$ExistingTask = Get-ScheduledTask -TaskName $TaskName -ErrorAction SilentlyContinue

if ($null -ne $ExistingTask) {
    Write-Host "Task '$TaskName' da ton tai. Dang cap nhat lai..." -ForegroundColor Yellow
    Unregister-ScheduledTask -TaskName $TaskName -Confirm:$false
}

$Arguments = '-NoProfile -ExecutionPolicy Bypass -WindowStyle Hidden -File "' + $ScriptPath + '" -Quiet'
$Action = New-ScheduledTaskAction -Execute "powershell.exe" -Argument $Arguments

# Kich hoat moi tuan mot lan vao Thu Hai luc 09:00 sang
$TriggerWeekly = New-ScheduledTaskTrigger -Weekly -DaysOfWeek Monday -At 9:00am

# Kich hoat bo sung khi nguoi dung dang nhap Windows
$TriggerLogon = New-ScheduledTaskTrigger -AtLogOn

$Settings = New-ScheduledTaskSettingsSet -AllowStartIfOnBatteries -DontStopIfGoingOnBatteries -StartWhenAvailable -RunOnlyIfNetworkAvailable

try {
    Register-ScheduledTask -TaskName $TaskName -Action $Action -Trigger @($TriggerWeekly, $TriggerLogon) -Settings $Settings -Description "Tu dong cap nhat Agent Skills va Plugins cho Antigravity IDE va CLI" | Out-Null
    Write-Host "Da dang ky thanh cong Windows Scheduled Task: '$TaskName'!" -ForegroundColor Green
    Write-Host "Lich chay: Moi Thu Hai luc 09:00 AM va moi khi dang nhap Windows." -ForegroundColor Green
    Write-Host "Che do: Chay ngam (Hidden background), khong lam phien nguoi dung." -ForegroundColor Green
} catch {
    $ErrMsg = $_.Exception.Message
    Write-Host "Loi khi dang ky Scheduled Task: $ErrMsg" -ForegroundColor Red
}
