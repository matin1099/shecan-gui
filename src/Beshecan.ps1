# Auto-elevate if not running as administrator
if (-not ([Security.Principal.WindowsPrincipal] [Security.Principal.WindowsIdentity]::GetCurrent()).IsInRole(
    [Security.Principal.WindowsBuiltInRole] "Administrator"))
{
    Start-Process powershell "-ExecutionPolicy Bypass -File `"$PSCommandPath`"" -Verb RunAs
    exit
}

# Get the active network adapter
$adapter = Get-NetAdapter | Where-Object { $_.Status -eq "Up" } | Select-Object -First 1

if ($adapter) {
    Write-Host "Reverting DNS settings to automatic for: $($adapter.Name)"
    try {
        Set-DnsClientServerAddress -InterfaceAlias $adapter.Name -ResetServerAddresses
        Write-Host "DNS settings reverted to automatic (via DHCP)."
    } catch {
        Write-Error "Failed to revert DNS: $_"
    }
} else {
    Write-Host "No active network adapter found."
}
