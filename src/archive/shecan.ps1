# Auto-elevate if not running as administrator
if (-not ([Security.Principal.WindowsPrincipal] [Security.Principal.WindowsIdentity]::GetCurrent()).IsInRole(
    [Security.Principal.WindowsBuiltInRole] "Administrator"))
{
    Start-Process powershell "-ExecutionPolicy Bypass -File `"$PSCommandPath`"" -Verb RunAs
    exit
}

# Define your custom DNS addresses
$preferredDNS = $args[0]
$alternateDNS = if ($args.Count -ge 2) { $args[1] } else { "" }

# Get the active network adapter
$adapter = Get-NetAdapter |
    Where-Object { $_.Status -eq "Up" -and $_.Name -notmatch "vEthernet|Virtual" } |
    Select-Object -First 1


if ($adapter) {
    Write-Host "Setting DNS for adapter: $($adapter.Name)"
    try {
        Set-DnsClientServerAddress -InterfaceAlias $adapter.Name -ServerAddresses ($preferredDNS, $alternateDNS)
        Write-Host "DNS successfully set to: $preferredDNS and $alternateDNS"
    } catch {
        Write-Error "Failed to set DNS: $_"
    }
} else {
    Write-Host "No active network adapter found."
}

