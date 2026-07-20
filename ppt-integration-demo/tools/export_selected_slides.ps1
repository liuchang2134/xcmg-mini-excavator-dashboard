param(
  [Parameter(Mandatory = $true)][string]$Source,
  [Parameter(Mandatory = $true)][string]$OutputDirectory,
  [int[]]$Slides = @(3..15)
)

$ErrorActionPreference = 'Stop'
$sourcePath = (Resolve-Path -LiteralPath $Source).Path
New-Item -ItemType Directory -Path $OutputDirectory -Force | Out-Null
$outputPath = (Resolve-Path -LiteralPath $OutputDirectory).Path

$powerPoint = $null
$presentation = $null
try {
  $powerPoint = New-Object -ComObject PowerPoint.Application
  $presentation = $powerPoint.Presentations.Open($sourcePath, $true, $true, $false)
  foreach ($slideNumber in $Slides) {
    if ($slideNumber -lt 1 -or $slideNumber -gt $presentation.Slides.Count) {
      throw "Slide $slideNumber is outside the presentation range."
    }
    $target = Join-Path $outputPath "slide-$slideNumber.png"
    $presentation.Slides.Item($slideNumber).Export($target, 'PNG', 1600, 900)
  }
  Write-Output "Exported $($Slides.Count) slides to $outputPath"
}
finally {
  if ($presentation) {
    $presentation.Close()
    [System.Runtime.InteropServices.Marshal]::ReleaseComObject($presentation) | Out-Null
  }
  if ($powerPoint) {
    $powerPoint.Quit()
    [System.Runtime.InteropServices.Marshal]::ReleaseComObject($powerPoint) | Out-Null
  }
  [GC]::Collect()
  [GC]::WaitForPendingFinalizers()
}
