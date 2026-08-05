param(
    [int]$LongEdge = 1600
)

$ErrorActionPreference = "Stop"
Set-StrictMode -Version Latest

$root = Split-Path -Parent $PSScriptRoot
$sourcePresentation = Join-Path $root "data\source-presentations\XCMG_North_America_Crane_Market_Insight_2025-07-01_V13_source.pptx"
$slidesPath = Join-Path $root "data\crane-ppt-insights\slides.json"
$outputDirectory = Join-Path $root "assets\crane-ppt-display"
$manifestPath = Join-Path $root "data\crane-ppt-insights\image-display.json"
$optimizerPath = Join-Path $PSScriptRoot "optimize_crane_ppt_images.py"
$stagingDirectory = Join-Path ([IO.Path]::GetTempPath()) ("xcmg-crane-ppt-" + [Guid]::NewGuid().ToString("N"))

if (-not (Test-Path -LiteralPath $sourcePresentation)) {
    throw "Source presentation not found: $sourcePresentation"
}

New-Item -ItemType Directory -Force -Path $outputDirectory | Out-Null
New-Item -ItemType Directory -Force -Path $stagingDirectory | Out-Null
$slides = Get-Content -LiteralPath $slidesPath -Raw -Encoding UTF8 | ConvertFrom-Json
$sourceImages = @(
    $slides |
        ForEach-Object { $_.images } |
        Where-Object { $_ } |
        Sort-Object -Unique
)

$powerPoint = New-Object -ComObject PowerPoint.Application
$presentation = $null
$imageMap = [ordered]@{}
$rendered = 0

try {
    $presentation = $powerPoint.Presentations.Open($sourcePresentation, $true, $true, $false)
    $slideWidth = [double]$presentation.PageSetup.SlideWidth
    $slideHeight = [double]$presentation.PageSetup.SlideHeight
    foreach ($sourceImage in $sourceImages) {
        $match = [regex]::Match(
            [string]$sourceImage,
            "s(?<slide>\d{3})-image-(?<shape>\d{2})-[^.]+\.(?:png|jpg|jpeg|gif|webp)$",
            [Text.RegularExpressions.RegexOptions]::IgnoreCase
        )
        if (-not $match.Success) {
            Write-Warning "Unable to map image to a PowerPoint shape: $sourceImage"
            continue
        }

        $slideNumber = [int]$match.Groups["slide"].Value
        $shapeNumber = [int]$match.Groups["shape"].Value
        $shape = $presentation.Slides.Item($slideNumber).Shapes.Item($shapeNumber)
        $shapeLongEdge = [Math]::Max([double]$shape.Width, [double]$shape.Height)
        $scaleFactor = $LongEdge / [Math]::Max($shapeLongEdge, 1.0)

        # Shape.Export scales relative to the full slide, not the shape bounds.
        # Scale the virtual slide so the exported shape itself reaches LongEdge.
        $width = [Math]::Max(1, [int][Math]::Round($slideWidth * $scaleFactor))
        $height = [Math]::Max(1, [int][Math]::Round($slideHeight * $scaleFactor))

        $sourceName = [IO.Path]::GetFileNameWithoutExtension([string]$sourceImage)
        $outputName = "$sourceName.png"
        $outputPath = Join-Path $stagingDirectory $outputName
        $shape.Export($outputPath, 2, $width, $height, 1)

        $imageMap[[string]$sourceImage] = "assets/crane-ppt-display/$sourceName.webp"
        $rendered++
    }
}
finally {
    if ($null -ne $presentation) {
        $presentation.Close()
        [Runtime.InteropServices.Marshal]::ReleaseComObject($presentation) | Out-Null
    }
    $powerPoint.Quit()
    [Runtime.InteropServices.Marshal]::ReleaseComObject($powerPoint) | Out-Null
    [GC]::Collect()
    [GC]::WaitForPendingFinalizers()
}

$python = (Get-Command python -ErrorAction Stop).Source
& $python $optimizerPath --input-dir $stagingDirectory --output-dir $outputDirectory --quality 92
if ($LASTEXITCODE -ne 0) {
    throw "Image optimization failed with exit code $LASTEXITCODE"
}

Get-ChildItem -LiteralPath $stagingDirectory -File | Remove-Item -Force
Remove-Item -LiteralPath $stagingDirectory -Force

$manifest = [ordered]@{
    source_presentation = "data/source-presentations/$([IO.Path]::GetFileName($sourcePresentation))"
    render_method = "PowerPoint Shape.Export with source crop, then WebP quality 92"
    long_edge = $LongEdge
    image_count = $rendered
    images = $imageMap
}

$json = $manifest | ConvertTo-Json -Depth 5
[IO.File]::WriteAllText($manifestPath, $json, [Text.UTF8Encoding]::new($false))
Write-Output "Rendered $rendered PowerPoint images to $outputDirectory"
Write-Output "Manifest: $manifestPath"
