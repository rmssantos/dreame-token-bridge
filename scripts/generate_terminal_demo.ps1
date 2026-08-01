param(
    [string]$OutputPath = (Join-Path $PSScriptRoot "..\assets\terminal-demo.gif"),
    [string]$FontFile = "C:\Windows\Fonts\consola.ttf"
)

$duration = 12
$draws = [System.Collections.Generic.List[string]]::new()
$fontForFfmpeg = $FontFile.Replace("\", "/").Replace(":", "\:")

function Add-TerminalText {
    param(
        [string]$Text,
        [int]$Y,
        [double]$Start,
        [double]$End = $duration
    )

    $safeText = $Text.Replace("'", "\\'")
    $enable = "between(t\,$Start\,$End)"
    $draws.Add("drawtext=fontfile='$fontForFfmpeg':text='$safeText':fontcolor=0xD1FAE5:fontsize=24:x=52:y=${Y}:enable='$enable'")
}

Add-TerminalText "============================================================" 44 0
Add-TerminalText "  Dreame Token Bridge - Xiaomi Account session refresh" 80 0
Add-TerminalText "============================================================" 116 0
Add-TerminalText "Xiaomi Account - d" 184 1.0 1.2
Add-TerminalText "Xiaomi Account - demo" 184 1.2 1.4
Add-TerminalText "Xiaomi Account - demo@example" 184 1.4 1.6
Add-TerminalText "Xiaomi Account - demo@example.com" 184 1.6
Add-TerminalText "Password - *" 220 2.0 2.15
Add-TerminalText "Password - *****" 220 2.15 2.3
Add-TerminalText "Password - ************" 220 2.3
Add-TerminalText "[1/3] Logging in to Xiaomi Account" 288 2.8
Add-TerminalText "CAPTCHA verification required" 324 3.4
Add-TerminalText "Enter CAPTCHA - D" 360 3.8 3.95
Add-TerminalText "Enter CAPTCHA - DEMO" 360 3.95 4.1
Add-TerminalText "Enter CAPTCHA - DEMO-42" 360 4.1
Add-TerminalText "Two-factor authentication required" 432 4.8
Add-TerminalText "Enter 2FA code - 0" 468 5.2 5.35
Add-TerminalText "Enter 2FA code - 000" 468 5.35 5.5
Add-TerminalText "Enter 2FA code - 000000" 468 5.5
Add-TerminalText "[2/3] Xiaomi Account session refreshed" 540 6.2
Add-TerminalText "serviceToken - [REDACTED]" 576 6.6
Add-TerminalText "ssecurity - [REDACTED]" 612 6.9
Add-TerminalText "Cache written and protocol.py.bak created" 648 7.3
Add-TerminalText "[3/3] Reload Dreame Vacuum in Home Assistant" 684 8.0

$filter = $draws -join ","
& ffmpeg -hide_banner -loglevel error `
    -f lavfi -i "color=c=0x0b1020:s=1280x720:d=${duration}:r=8" `
    -vf $filter -loop 0 -y $OutputPath

if ($LASTEXITCODE -ne 0) {
    throw "FFmpeg failed to generate the terminal demonstration."
}
