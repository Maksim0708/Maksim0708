[Setup]
AppName=AlphaTast Clone
AppVersion=1.0
DefaultDirName={pf}\AlphaTastClone
DefaultGroupName=AlphaTastClone
OutputDir=dist
OutputBaseFilename=setup

[Files]
; expects alphatast_clone.exe built via PyInstaller in dist folder
Source: "dist\alphatast_clone\alphatast_clone.exe"; DestDir: "{app}"; Flags: ignoreversion

[Icons]
Name: "{group}\AlphaTast Clone"; Filename: "{app}\alphatast_clone.exe"
