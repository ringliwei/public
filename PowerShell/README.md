# PowerShell

[GitHub](https://github.com/PowerShell/PowerShell)

[PowerShell about](https://docs.microsoft.com/en-us/powershell/module/microsoft.powershell.core/about/?view=powershell-6)

## PSTip

[A Better Way to Generate HTTP Query Strings in PowerShell](https://www.powershellmagazine.com/2019/06/14/pstip-a-better-way-to-generate-http-query-strings-in-powershell/)

```powershell
function New-HttpQueryString
{
    [CmdletBinding()]
    param
    (
        [Parameter(Mandatory = $true)]
        [String]
        $Uri,

        [Parameter(Mandatory = $true)]
        [Hashtable]
        $QueryParameter
    )

    # Add System.Web
    Add-Type -AssemblyName System.Web

    # Create a http name value collection from an empty string
    $nvCollection = [System.Web.HttpUtility]::ParseQueryString([String]::Empty)

    foreach ($key in $QueryParameter.Keys)
    {
        $nvCollection.Add($key, $QueryParameter.$key)
    }

    # Build the uri
    $uriRequest = [System.UriBuilder]$uri
    $uriRequest.Query = $nvCollection.ToString()

    return $uriRequest.Uri.OriginalString
}
```

[Force-remove files and directories in PowerShell fails sometimes, but not always](https://serverfault.com/questions/199921/force-remove-files-and-directories-in-powershell-fails-sometimes-but-not-always/942429#942429)

[Cannot remove item, The Directory is not empty](https://stackoverflow.com/questions/53553729/cannot-remove-item-the-directory-is-not-empty/)

``` powershell


function Remove-FileSystemItem {
    <#
    .SYNOPSIS
      Removes files or directories reliably and synchronously.
  
    .DESCRIPTION
      Removes files and directories, ensuring reliable and synchronous
      behavior across all supported platforms.
  
      The syntax is a subset of what Remove-Item supports; notably,
      -Include / -Exclude and -Force are NOT supported; -Force is implied.
  
      As with Remove-Item, passing -Recurse is required to avoid a prompt when
      deleting a non-empty directory.
  
      IMPORTANT:
        * On Unix platforms, this function is merely a wrapper for Remove-Item,
          where the latter works reliably and synchronously, but on Windows a
          custom implementation must be used to ensure reliable and synchronous
          behavior. See https://github.com/PowerShell/PowerShell/issues/8211
  
      * On Windows:
        * The *parent directory* of a directory being removed must be
          *writable* for the synchronous custom implementation to work.
        * The custom implementation is also applied when deleting
           directories on *network drives*.
  
      * If an indefinitely *locked* file or directory is encountered, removal is aborted.
        By contrast, files opened with FILE_SHARE_DELETE /
        [System.IO.FileShare]::Delete on Windows do NOT prevent removal,
        though they do live on under a temporary name in the parent directory
        until the last handle to them is closed.
  
      * Hidden files and files with the read-only attribute:
        * These are *quietly removed*; in other words: this function invariably
          behaves like `Remove-Item -Force`.
        * Note, however, that in order to target hidden files / directories
          as *input*, you must specify them as a *literal* path, because they
          won't be found via a wildcard expression.
  
      * The reliable custom implementation on Windows comes at the cost of
        decreased performance.
  
    .EXAMPLE
      Remove-FileSystemItem C:\tmp -Recurse
  
      Synchronously removes directory C:\tmp and all its content.
    #>
    [CmdletBinding(SupportsShouldProcess, ConfirmImpact = 'Medium', DefaultParameterSetName = 'Path', PositionalBinding = $false)]
    param(
        [Parameter(ParameterSetName = 'Path', Mandatory, Position = 0, ValueFromPipeline, ValueFromPipelineByPropertyName)]
        [string[]] $Path
        ,
        [Parameter(ParameterSetName = 'Literalpath', ValueFromPipelineByPropertyName)]
        [Alias('PSPath')]
        [string[]] $LiteralPath
        ,
        [switch] $Recurse
    )
    begin {
        # !! Workaround for https://github.com/PowerShell/PowerShell/issues/1759
        if ($ErrorActionPreference -eq [System.Management.Automation.ActionPreference]::Ignore) { $ErrorActionPreference = 'Ignore' }
        $targetPath = ''
        $yesToAll = $noToAll = $false
        function trimTrailingPathSep([string] $itemPath) {
            if ($itemPath[-1] -in '\', '/') {
                # Trim the trailing separator, unless the path is a root path such as '/' or 'c:\'
                if ($itemPath.Length -gt 1 -and $itemPath -notmatch '^[^:\\/]+:.$') {
                    $itemPath = $itemPath.Substring(0, $itemPath.Length - 1)
                }
            }
            $itemPath
        }
        function getTempPathOnSameVolume([string] $itemPath, [string] $tempDir) {
            if (-not $tempDir) { $tempDir = [IO.Path]::GetDirectoryName($itemPath) }
            [IO.Path]::Combine($tempDir, [IO.Path]::GetRandomFileName())
        }
        function syncRemoveFile([string] $filePath, [string] $tempDir) {
            # Clear the ReadOnly attribute, if present.
            if (($attribs = [IO.File]::GetAttributes($filePath)) -band [System.IO.FileAttributes]::ReadOnly) {
                [IO.File]::SetAttributes($filePath, $attribs -band -bnot [System.IO.FileAttributes]::ReadOnly)
            }
            $tempPath = getTempPathOnSameVolume $filePath $tempDir
            [IO.File]::Move($filePath, $tempPath)
            [IO.File]::Delete($tempPath)
        }
        function syncRemoveDir([string] $dirPath, [switch] $recursing) {
            if (-not $recursing) { $dirPathParent = [IO.Path]::GetDirectoryName($dirPath) }
            # Clear the ReadOnly attribute, if present.
            # Note: [IO.File]::*Attributes() is also used for *directories*; [IO.Directory] doesn't have attribute-related methods.
            if (($attribs = [IO.File]::GetAttributes($dirPath)) -band [System.IO.FileAttributes]::ReadOnly) {
                [IO.File]::SetAttributes($dirPath, $attribs -band -bnot [System.IO.FileAttributes]::ReadOnly)
            }
            # Remove all children synchronously.
            $isFirstChild = $true
            foreach ($item in [IO.directory]::EnumerateFileSystemEntries($dirPath)) {
                if (-not $recursing -and -not $Recurse -and $isFirstChild) {
                    # If -Recurse wasn't specified, prompt for nonempty dirs.
                    $isFirstChild = $false
                    # Note: If -Confirm was also passed, this prompt is displayed *in addition*, after the standard $PSCmdlet.ShouldProcess() prompt.
                    #       While Remove-Item also prompts twice in this scenario, it shows the has-children prompt *first*.
                    if (-not $PSCmdlet.ShouldContinue("The item at '$dirPath' has children and the -Recurse switch was not specified. If you continue, all children will be removed with the item. Are you sure you want to continue?", 'Confirm', ([ref] $yesToAll), ([ref] $noToAll))) { return }
                }
                $itemPath = [IO.Path]::Combine($dirPath, $item)
                ([ref] $targetPath).Value = $itemPath
                if ([IO.Directory]::Exists($itemPath)) {
                    syncremoveDir $itemPath -recursing
                }
                else {
                    syncremoveFile $itemPath $dirPathParent
                }
            }
            # Finally, remove the directory itself synchronously.
            ([ref] $targetPath).Value = $dirPath
            $tempPath = getTempPathOnSameVolume $dirPath $dirPathParent
            [IO.Directory]::Move($dirPath, $tempPath)
            [IO.Directory]::Delete($tempPath)
        }
    }
  
    process {
        $isLiteral = $PSCmdlet.ParameterSetName -eq 'LiteralPath'
        if ($env:OS -ne 'Windows_NT') {
            # Unix: simply pass through to Remove-Item, which on Unix works reliably and synchronously
            Remove-Item @PSBoundParameters
        }
        else {
            # Windows: use synchronous custom implementation
            foreach ($rawPath in ($Path, $LiteralPath)[$isLiteral]) {
                # Resolve the paths to full, filesystem-native paths.
                try {
                    # !! Convert-Path does find hidden items via *literal* paths, but not via *wildcards* - and it has no -Force switch (yet)
                    # !! See https://github.com/PowerShell/PowerShell/issues/6501
                    $resolvedPaths = if ($isLiteral) { Convert-Path -ErrorAction Stop -LiteralPath $rawPath } else { Convert-Path -ErrorAction Stop -path $rawPath }
                }
                catch {
                    Write-Error $_ # relay error, but in the name of this function
                    continue
                }
                try {
                    $isDir = $false
                    foreach ($resolvedPath in $resolvedPaths) {
                        # -WhatIf and -Confirm support.
                        if (-not $PSCmdlet.ShouldProcess($resolvedPath)) { continue }
                        if ($isDir = [IO.Directory]::Exists($resolvedPath)) {
                            # dir.
                            # !! A trailing '\' or '/' causes directory removal to fail ("in use"), so we trim it first.
                            syncRemoveDir (trimTrailingPathSep $resolvedPath)
                        }
                        elseif ([IO.File]::Exists($resolvedPath)) {
                            # file
                            syncRemoveFile $resolvedPath
                        }
                        else {
                            Throw "Not a file-system path or no longer extant: $resolvedPath"
                        }
                    }
                }
                catch {
                    if ($isDir) {
                        $exc = $_.Exception
                        if ($exc.InnerException) { $exc = $exc.InnerException }
                        if ($targetPath -eq $resolvedPath) {
                            Write-Error "Removal of directory '$resolvedPath' failed: $exc"
                        }
                        else {
                            Write-Error "Removal of directory '$resolvedPath' failed, because its content could not be (fully) removed: $targetPath`: $exc"
                        }
                    }
                    else {
                        Write-Error $_  # relay error, but in the name of this function
                    }
                    continue
                }
            }
        }
    }
}
```
