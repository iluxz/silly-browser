; the silly browser - windows 3.1 flavoured installer
#define MyAppName "the silly browser"
#define MyAppVersion "0.1.0"
#define MyAppPublisher "lux"
#define MyAppExeName "silly-browser.exe"

[Setup]
AppId={{8E4C1A22-6C3F-4C6E-9E4B-1D2C3B4A5E6F}
AppName={#MyAppName}
AppVersion={#MyAppVersion}
AppVerName={#MyAppName} {#MyAppVersion}
AppPublisher={#MyAppPublisher}
DefaultDirName={autopf}\silly-browser
DefaultGroupName={#MyAppName}
DisableProgramGroupPage=yes
OutputDir=installer_output
OutputBaseFilename=silly-browser-setup
Compression=lzma2/max
SolidCompression=yes
WizardStyle=classic
WizardImageFile=setup_panel.bmp
SetupIconFile=silly.ico
UninstallDisplayIcon={app}\{#MyAppExeName}
UninstallDisplayName={#MyAppName}
ArchitecturesInstallIn64BitMode=x64compatible
MinVersion=10.0
PrivilegesRequired=lowest
ShowLanguageDialog=no

[Languages]
Name: "english"; MessagesFile: "compiler:Default.isl"

[Tasks]
Name: "desktopicon"; Description: "{cm:CreateDesktopIcon}"; GroupDescription: "{cm:AdditionalIcons}"; Flags: unchecked

[Files]
Source: "dist\{#MyAppExeName}"; DestDir: "{app}"; Flags: ignoreversion
Source: "logo.png"; DestDir: "{app}"; Flags: ignoreversion isreadme
Source: "README.md"; DestDir: "{app}"; Flags: ignoreversion isreadme
Source: "setup_bg.bmp"; DestDir: "{tmp}"; Flags: dontcopy

[Code]
procedure InitializeWizard();
var
  BgImage: TBitmapImage;
begin
  WizardForm.Color := clBlack;
  ExtractTemporaryFile('setup_bg.bmp');
  BgImage := TBitmapImage.Create(WizardForm);
  BgImage.Parent := WizardForm;
  BgImage.SetBounds(0, 0, WizardForm.ClientWidth, WizardForm.ClientHeight);
  BgImage.Bitmap.LoadFromFile(ExpandConstant('{tmp}\setup_bg.bmp'));
  BgImage.Stretch := True;
  BgImage.SendToBack;
end;

[Icons]
Name: "{group}\{#MyAppName}"; Filename: "{app}\{#MyAppExeName}"
Name: "{group}\uninstall {#MyAppName}"; Filename: "{uninstallexe}"
Name: "{autodesktop}\{#MyAppName}"; Filename: "{app}\{#MyAppExeName}"; Tasks: desktopicon

[Run]
Filename: "{app}\{#MyAppExeName}"; Description: "{cm:LaunchProgram,{#MyAppName}}"; Flags: nowait postinstall skipifsilent
