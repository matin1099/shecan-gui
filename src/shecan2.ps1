# Auto-elevate if not running as administrator
if (-not ([Security.Principal.WindowsPrincipal] [Security.Principal.WindowsIdentity]::GetCurrent()).IsInRole(
    [Security.Principal.WindowsBuiltInRole] "Administrator")) {
    Start-Process powershell "-ExecutionPolicy Bypass -File `"$PSCommandPath`" $args" -Verb RunAs
    exit
}

# Check if user provided at least one DNS address
if ($args.Count -lt 1) {
    Write-Host "Usage: powershell -File shecan.ps1 <PreferredDNS> [AlternateDNS]"
    exit
}

# Read DNS addresses from arguments
$preferredDNS = $args[0]
$alternateDNS = if ($args.Count -ge 2) { $args[1] } else { "" }

# Get active non-virtual network adapter
$adapter = Get-NetAdapter |
    Where-Object { $_.Status -eq "Up" -and $_.Name -notmatch "vEthernet|Virtual" } |
    Select-Object -First 1

if ($adapter) {
    Write-Host "Setting DNS for adapter: $($adapter.Name)"
    try {
        $dnsList = if ($alternateDNS) { @($preferredDNS, $alternateDNS) } else { @($preferredDNS) }
        Set-DnsClientServerAddress -InterfaceAlias $adapter.Name -ServerAddresses $dnsList
        Write-Host "DNS successfully set to: $($dnsList -join ', ')"
    } catch {
        Write-Error "Failed to set DNS: $_"
    }
} else {
    Write-Host "No suitable network adapter found."
}
