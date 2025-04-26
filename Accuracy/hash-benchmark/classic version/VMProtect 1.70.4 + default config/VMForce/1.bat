Get-ChildItem -recurse | ForEach-Object{
    $_.CreationTime = Get-Date
    $_.LastWriteTime = Get-Date
    $_.LastAccessTime = Get-Date
}