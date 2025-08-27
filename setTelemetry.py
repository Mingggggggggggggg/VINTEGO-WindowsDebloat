import subprocess
import winreg
import logger as log

#Global Variables
hklm = winreg.HKEY_LOCAL_MACHINE
hkcu = winreg.HKEY_CURRENT_USER


def setRegistry(root, path, name, valueType, setValue):
    try:
        print(f"Setze Registryeintrg {path}\\{name} auf {setValue}")
        log.logMessage(f"Setze Registryeintrg {path}\\{name} auf {setValue}")
        key = winreg.CreateKey(root, path)
        winreg.SetValueEx(key, name, 0, valueType, setValue)
        winreg.CloseKey(key)
        print(f"{path}\\{name} gesetzt auf {setValue}")
        log.logMessage(f"{path}\\{name} gesetzt auf {setValue}")
    except Exception as e:
        print(f"Fehler beim Setzen des Registry Keys {path}\\{name}: {e}")
        log.logMessage(f"Fehler beim Setzen des Registry Keys {path}\\{name}: {e}")

def setTask(taskPath, setting):
    if setting:
        try:
            print(f"Setze Scheduled Task {taskPath} auf ENABLE")
            log.logMessage(f"Setze Scheduled Task {taskPath} auf ENABLE")

            subprocess.run(
                ["schtasks", "/Change", "/TN", taskPath, "/ENABLE"],
                check=True,
                capture_output=True,
                text=True
            )

            print(f"Task aktiviert: {taskPath}")
            log.logMessage(f"Task aktiviert: {taskPath}")
        except subprocess.CalledProcessError as e:
            print(f"Fehler beim Aktivieren von {taskPath}: {e.stderr.strip()}")
            log.logMessage(f"Fehler beim Aktivieren von {taskPath}: {e.stderr.strip()}")
    else:
        try:
            print(f"Setze Scheduled Task {taskPath} auf DISABLE")
            log.logMessage(f"Setze Scheduled Task {taskPath} auf DISABLE")

            subprocess.run(
                ["schtasks", "/Change", "/TN", taskPath, "/DISABLE"],
                check=True,
                capture_output=True,
                text=True
            )

            print(f"Task deaktiviert: {taskPath}")
            log.logMessage(f"Task deaktiviert: {taskPath}")
        except subprocess.CalledProcessError as e:
            print(f"Fehler beim Deaktivieren von {taskPath}: {e.stderr.strip()}")
            log.logMessage(f"Fehler beim Deaktivieren von {taskPath}: {e.stderr.strip()}")



def initTelemetry(data, settings : bool = False):
    for i in data:
        match i:
            case "Location Tracking":
                configureLocationTracking(settings)
            case "Telemetry":
                configureTelemetry(settings)
            case "GameDVR":
                configureGameDVR(settings)
            case "WiFi Sense":
                configureWiFiSense(settings)
            case "Recall":
                configureRecall(settings)
            case "Background Apps":
                configureMicrosoftBackgroundApps(settings)
            case  _:
                print(f"Datenschutzliste Leer oder ungueltige Werte gefunden: {i}")



def configureLocationTracking(settings: bool):
    keys = [
        {
            "root" : hklm, 
            "path" : "SOFTWARE\\Microsoft\\Windows\\CurrentVersion\\CapabilityAccessManager\\ConsentStore\\location", 
            "name" : "Value", 
            "valType" : winreg.REG_SZ
        },
        {
            "root" : hklm, 
            "path" : "SOFTWARE\\Microsoft\\Windows NT\\CurrentVersion\\Sensor\\Overrides\\{BFA794E4-F964-4FDB-90F6-51056BFE4B44}", 
            "name" : "SensorPermissionState", 
            "valType" : winreg.REG_DWORD
        },
        {
            "root" : hklm, 
            "path" : "SYSTEM\\CurrentControlSet\\Services\\lfsvc\\Service\\Configuration", 
            "name" : "Status", 
            "valType" : winreg.REG_DWORD
        },
        {
            "root" : hklm,
            "path" : "SYSTEM\\Maps", 
            "name" : "AutoUpdateEnabled", 
            "valType" : winreg.REG_DWORD
        }
    ]

    if settings:
        values = {"Value": "Allow", "SensorPermissionState": 1, "Status": 1, "AutoUpdateEnabled": 1}
    else:
        values = {"Value": "Deny", "SensorPermissionState": 0, "Status": 0, "AutoUpdateEnabled": 0}

    for key in keys:
        value = values[key["name"]]
        setRegistry(key["root"], key["path"], key["name"], key["valType"], value)


def configureTelemetry(settings : bool):
    schedulePaths = [
       "Microsoft\\Windows\\Application Experience\\Microsoft Compatibility Appraiser",
       "Microsoft\\Windows\\Application Experience\\ProgramDataUpdater",
       "Microsoft\\Windows\\Autochk\\Proxy",
       "Microsoft\\Windows\\Customer Experience Improvement Program\\Consolidator",
       "Microsoft\\Windows\\Customer Experience Improvement Program\\UsbCeip",
       "Microsoft\\Windows\\DiskDiagnostic\\Microsoft-Windows-DiskDiagnosticDataCollector",
       "Microsoft\\Windows\\Feedback\\Siuf\\DmClient",
       "Microsoft\\Windows\\Feedback\\Siuf\\DmClientOnScenarioDownload",
       "Microsoft\\Windows\\Windows Error Reporting\\QueueReporting",
       "Microsoft\\Windows\\Application Experience\\MareBackup",
       "Microsoft\\Windows\\Application Experience\\StartupAppTask",
       "Microsoft\\Windows\\Application Experience\\PcaPatchDbTask",
       "Microsoft\\Windows\\Maps\\MapsUpdateTask",
    ]

    for path in schedulePaths:
        setTask(path, settings)

    keys = [
        {
            "root" : hklm,
            "path" : "SOFTWARE\\Microsoft\\Windows\\CurrentVersion\\Policies\\DataCollection",
            "name" : "AllowTelemetry", 
            "valType" : winreg.REG_DWORD
        },
        {
            "root" : hklm,
            "path" : "SOFTWARE\\Policies\\Microsoft\\Windows\\DataCollection", 
            "name" : "AllowTelemetry", 
            "valType" : winreg.REG_DWORD
        },
        {
            "root" : hkcu,
            "path" : "SOFTWARE\\Microsoft\\Windows\\CurrentVersion\\ContentDeliveryManager", 
            "name" : "ContentDeliveryAllowed", 
            "valType" : winreg.REG_DWORD
        },
        {
            "root" : hkcu,
            "path" : "SOFTWARE\\Microsoft\\Windows\\CurrentVersion\\ContentDeliveryManager", 
            "name" : "OemPreInstalledAppsEnabled", 
            "valType" : winreg.REG_DWORD
        },
        {
            "root" : hkcu,
            "path" : "SOFTWARE\\Microsoft\\Windows\\CurrentVersion\\ContentDeliveryManager", 
            "name" : "PreInstalledAppsEnabled", 
            "valType" : winreg.REG_DWORD
        },
        {
            "root" : hkcu,
            "path" : "SOFTWARE\\Microsoft\\Windows\\CurrentVersion\\ContentDeliveryManager", 
            "name" : "PreInstalledAppsEverEnabled", 
            "valType" : winreg.REG_DWORD
        },
        {
            "root" : hkcu,
            "path" : "SOFTWARE\\Microsoft\\Windows\\CurrentVersion\\ContentDeliveryManager", 
            "name" : "SilentInstalledAppsEnabled", 
            "valType" : winreg.REG_DWORD
        },
        {
            "root" : hkcu,
            "path" : "Software\\Microsoft\\Windows\\CurrentVersion\\ContentDeliveryManager", 
            "name" : "SubscribedContent-338387Enabled", 
            "valType" : winreg.REG_DWORD
        },
        {
            "root" : hkcu,
            "path" : "SOFTWARE\\Microsoft\\Windows\\CurrentVersion\\ContentDeliveryManager", 
            "name" : "SubscribedContent-338388Enabled", 
            "valType" : winreg.REG_DWORD
        },
        {
            "root" : hkcu,
            "path" : "SOFTWARE\\Microsoft\\Windows\\CurrentVersion\\ContentDeliveryManager", 
            "name" : "SubscribedContent-338389Enabled", 
            "valType" : winreg.REG_DWORD
        },
        {
            "root" : hkcu,
            "path" : "SOFTWARE\\Microsoft\\Windows\\CurrentVersion\\ContentDeliveryManager", 
            "name" : "SubscribedContent-353698Enabled",
            "valType" : winreg.REG_DWORD
        },
        {
            "root" : hkcu,
            "path" : "SOFTWARE\\Microsoft\\Windows\\CurrentVersion\\ContentDeliveryManager", 
            "name" : "SystemPaneSuggestionsEnabled", 
            "valType" : winreg.REG_DWORD
        },
        {
            "root" : hkcu,
            "path" : "SOFTWARE\\Microsoft\\Siuf\\Rules", 
            "name" : "NumberOfSIUFInPeriod", 
            "valType" : winreg.REG_DWORD
        },
        {
            "root" : hklm,
            "path" : "SOFTWARE\\Policies\\Microsoft\\Windows\\DataCollection", 
            "name" : "DoNotShowFeedbackNotifications", 
            "valType" : winreg.REG_DWORD
        },
        {
            "root" : hkcu,
            "path" : "SOFTWARE\\Policies\\Microsoft\\Windows\\CloudContent", 
            "name" : "DisableTailoredExperiencesWithDiagnosticData", 
            "valType" : winreg.REG_DWORD
        },
        {
            "root" : hklm,
            "path" : "SOFTWARE\\Policies\\Microsoft\\Windows\\AdvertisingInfo", 
            "name" : "DisabledByGroupPolicy", 
            "valType" : winreg.REG_DWORD
        },
        {
            "root" : hklm,
            "path" : "SOFTWARE\\Microsoft\\Windows\\Windows Error Reporting", 
            "name" : "Disabled", 
            "valType" : winreg.REG_DWORD
        },
        {
            "root" : hklm,
            "path" : "SOFTWARE\\Microsoft\\Windows\\CurrentVersion\\DeliveryOptimization\\Config", 
            "name" : "DODownloadMode", 
            "valType" : winreg.REG_DWORD
        },
        {
            "root" : hklm,
            "path" : "SYSTEM\\CurrentControlSet\\Control\\Remote Assistance", 
            "name" : "fAllowToGetHelp", 
            "valType" : winreg.REG_DWORD
        },
        {
            "root" : hkcu,
            "path" : "SOFTWARE\\Microsoft\\Windows\\CurrentVersion\\Explorer\\OperationStatusManager", 
            "name" : "EnthusiastMode", 
            "valType" : winreg.REG_DWORD
        },
        {
            "root" : hkcu,
            "path" : "SOFTWARE\\Microsoft\\Windows\\CurrentVersion\\Explorer\\Advanced", 
            "name" : "ShowTaskViewButton", 
            "valType" : winreg.REG_DWORD
        },
        {
            "root" : hkcu,
            "path" : "SOFTWARE\\Microsoft\\Windows\\CurrentVersion\\Explorer\\Advanced\\People", 
            "name" : "PeopleBand", 
            "valType" : winreg.REG_DWORD
        },
        {
            "root" : hkcu,
            "path" : "SOFTWARE\\Microsoft\\Windows\\CurrentVersion\\Explorer\\Advanced", 
            "name" : "LaunchTo", 
            "valType" : winreg.REG_DWORD
        },
        {
            "root" : hklm,
            "path" : "SYSTEM\\CurrentControlSet\\Control\\FileSystem", 
            "name" : "LongPathsEnabled", 
            "valType" : winreg.REG_DWORD
        },
        {
            "root" : hklm,
            "path" : "SOFTWARE\\Microsoft\\Windows\\CurrentVersion\\DriverSearching", 
            "name" : "SearchOrderConfig", 
            "valType" : winreg.REG_DWORD
        },
        {
            "root" : hklm,
            "path" : "SOFTWARE\\Microsoft\\Windows NT\\CurrentVersion\\Multimedia\\SystemProfile", 
            "name" : "SystemResponsiveness", 
            "valType" : winreg.REG_DWORD
        },
        {
            "root" : hklm,
            "path" : "SOFTWARE\\Microsoft\\Windows NT\\CurrentVersion\\Multimedia\\SystemProfile", 
            "name" : "NetworkThrottlingIndex", 
            "valType" : winreg.REG_DWORD
        },
        {
            "root" : hkcu,
            "path" : "Control Panel\\Desktop", 
            "name" : "MenuShowDelay", 
            "valType" : winreg.REG_DWORD
        },
        {
            "root" : hkcu,
            "path" : "Control Panel\\Desktop", 
            "name" : "AutoEndTasks", 
            "valType" : winreg.REG_DWORD
        },
        {
            "root" : hklm,
            "path" : "SYSTEM\\CurrentControlSet\\Control\\Session Manager\\Memory Management", 
            "name" : "ClearPageFileAtShutdown", 
            "valType" : winreg.REG_DWORD
        },
        {
            "root" : hklm,
            "path" : "SYSTEM\\ControlSet001\\Services\\Ndu", 
            "name" : "Start", 
            "valType" : winreg.REG_DWORD
        },
        {
            "root" : hkcu,
            "path" : "Control Panel\\Mouse", 
            "name" : "MouseHoverTime", 
            "valType" : winreg.REG_SZ
        },
        {
            "root" : hklm,
            "path" : "SYSTEM\\CurrentControlSet\\Services\\LanmanServer\\Parameters", 
            "name" : "IRPStackSize", 
            "valType" : winreg.REG_DWORD
        },
        {
            "root" : hkcu,
            "path" : "SOFTWARE\\Policies\\Microsoft\\Windows\\Windows Feeds", 
            "name" : "EnableFeeds", 
            "valType" : winreg.REG_DWORD
        },
        {
            "root" : hkcu,
            "path" : "Software\\Microsoft\\Windows\\CurrentVersion\\Feeds", 
            "name" : "ShellFeedsTaskbarViewMode", 
            "valType" : winreg.REG_DWORD
        },
        {
            "root" : hkcu,
            "path" : "Software\\Microsoft\\Windows\\CurrentVersion\\Policies\\Explorer", 
            "name" : "HideSCAMeetNow", 
            "valType" : winreg.REG_DWORD
        },
        {
            "root" : hkcu,
            "path" : "Software\\Microsoft\\Windows\\CurrentVersion\\UserProfileEngagement", 
            "name" : "ScoobeSystemSettingEnabled", 
            "valType" : winreg.REG_DWORD
        }
    ]
    if settings:
        values = {"AllowTelemetry": 1, "AllowTelemetry": 1, "ContentDeliveryAllowed": 1, "OemPreInstalledAppsEnabled": 1, "PreInstalledAppsEnabled": 1, "PreInstalledAppsEverEnabled": 1, "SilentInstalledAppsEnabled": 1, "SubscribedContent-338387Enabled": 1, "SubscribedContent-338388Enabled": 1, "SubscribedContent-338389Enabled": 1, "SubscribedContent-353698Enabled": 1, "SystemPaneSuggestionsEnabled": 1, "NumberOfSIUFInPeriod": 0, "DoNotShowFeedbackNotifications": 0, "DisableTailoredExperiencesWithDiagnosticData": 0, "DisabledByGroupPolicy": 0, "Disabled": 0, "DODownloadMode": 1, "fAllowToGetHelp": 1, "EnthusiastMode": 0, "ShowTaskViewButton": 1, "PeopleBand": 1, "LaunchTo": 1, "LongPathsEnabled": 0, "SearchOrderConfig": 1, "SystemResponsiveness": 1, "NetworkThrottlingIndex": 1, "MenuShowDelay": 1, "AutoEndTasks": 1, "ClearPageFileAtShutdown": 0, "Start": 1, "MouseHoverTime": 400, "IRPStackSize": 20, "EnableFeeds": 1, "ShellFeedsTaskbarViewMode": 1, "HideSCAMeetNow": 1, "ScoobeSystemSettingEnabled": 1}
    else:
        values = {"AllowTelemetry": 0, "AllowTelemetry": 0, "ContentDeliveryAllowed": 0, "OemPreInstalledAppsEnabled": 0, "PreInstalledAppsEnabled": 0, "PreInstalledAppsEverEnabled": 0, "SilentInstalledAppsEnabled": 0, "SubscribedContent-338387Enabled": 0, "SubscribedContent-338388Enabled": 0, "SubscribedContent-338389Enabled": 0, "SubscribedContent-353698Enabled": 0, "SystemPaneSuggestionsEnabled": 0, "NumberOfSIUFInPeriod": 0, "DoNotShowFeedbackNotifications": 1, "DisableTailoredExperiencesWithDiagnosticData": 1, "DisabledByGroupPolicy": 1, "Disabled": 1, "DODownloadMode": 1, "fAllowToGetHelp": 0, "EnthusiastMode": 1, "ShowTaskViewButton": 0, "PeopleBand": 0, "LaunchTo": 1, "LongPathsEnabled": 1, "SearchOrderConfig": 1, "SystemResponsiveness": 0, "NetworkThrottlingIndex": 4294967295, "MenuShowDelay": 1, "AutoEndTasks": 1, "ClearPageFileAtShutdown": 0, "Start": 2, "MouseHoverTime": 400, "IRPStackSize": 30, "EnableFeeds": 0, "ShellFeedsTaskbarViewMode": 2, "HideSCAMeetNow": 1, "ScoobeSystemSettingEnabled": 0}

    for key in keys:
        value = values[key["name"]]
        setRegistry(key["root"], key["path"], key["name"], key["valType"], value)

def configureGameDVR(settings : bool):
    keys = [
        {
            "root" : hkcu,
            "path" : "System\\GameConfigStore", 
            "name" : "GameDVR_FSEBehavior", 
            "valType" : winreg.REG_DWORD
        },
        {
            "root" : hkcu,
            "path" : "System\\GameConfigStore", 
            "name" : "GameDVR_Enabled", 
            "valType" : winreg.REG_DWORD
        },
        {
            "root" : hkcu,
            "path" : "System\\GameConfigStore", 
            "name" : "GameDVR_HonorUserFSEBehaviorMode", 
            "valType" : winreg.REG_DWORD
        },
        {
            "root" : hkcu,
            "path" : "System\\GameConfigStore", 
            "name" : "GameDVR_EFSEFeatureFlags", 
            "valType" : winreg.REG_DWORD
        },
        {
            "root" : hklm,
            "path" : "SOFTWARE\\Policies\\Microsoft\\Windows\\GameDVR", 
            "name" : "AllowGameDVR", 
            "valType" : winreg.REG_DWORD
        }
    ]
    if settings:
        values = {"GameDVR_FSEBehavior" : 1, "GameDVR_Enabled" : 1, "GameDVR_HonorUserFSEBehaviorMode" : 0, "GameDVR_EFSEFeatureFlags" : 1, "AllowGameDVR" : 1}
    else:
        values = {"GameDVR_FSEBehavior" : 2, "GameDVR_Enabled" : 0, "GameDVR_HonorUserFSEBehaviorMode" : 1, "GameDVR_EFSEFeatureFlags" : 0, "AllowGameDVR" : 0}

    for key in keys:
        value = values[key["name"]]
        setRegistry(key["root"], key["path"], key["name"], key["valType"], value)

def configureWiFiSense(settings : bool):
    keys = [
        {
            "root" : hklm,
            "path" : "Software\\Microsoft\\PolicyManager\\default\\WiFi\\AllowWiFiHotSpotReporting", 
            "name" : "Value", 
            "valType" : winreg.REG_DWORD
        },
        {
            "root" : hklm,
            "path" : "Software\\Microsoft\\PolicyManager\\default\\WiFi\\AllowAutoConnectToWiFiSenseHotspots", 
            "name" : "Value", 
            "valType" : winreg.REG_DWORD
        }
    ]

    if settings:
        values = {"Value" : 1, "Value" : 1}
    else:
        values = {"Value" : 0, "Value" : 0}
    for key in keys:
        value = values[key["name"]]
        setRegistry(key["root"], key["path"], key["name"], key["valType"], value)

def configureRecall(settings: bool):
    if settings:
        cmd = "DISM /Online /Enable-Feature /FeatureName:Recall /NoRestart"
    else:
        cmd = "DISM /Online /Disable-Feature /FeatureName:Recall /NoRestart"

    try:
        print(f"Konfiguriere Recall auf {settings}")
        log.logMessage(f"Konfiguriere Recall auf {settings}")
        rs = subprocess.run(
            ["powershell", "-Command", cmd],
            check=True,
            capture_output=True,
            text=True
        )
        print(rs)
        log.logMessage(rs)
    except subprocess.CalledProcessError as e:
        print(f"Fehler beim Deaktivieren von Recall: {e.stderr.strip()}")
        log.logMessage(f"Fehler beim Deaktivieren von Recall: {e.stderr.strip()}")


def configureMicrosoftBackgroundApps(settings : bool):

    keys = [
        {
            "root" : hkcu,
            "path" : "Software\\Microsoft\\Windows\\CurrentVersion\\BackgroundAccessApplications", 
            "name" : "GlobalUserDisabled", 
            "valType" : winreg.REG_DWORD
        }
    ]
    if settings:
        values = {"GlobalUserDisabled" : 0}
    else:
        values = {"GlobalUserDisabled" : 1}
    for key in keys:
        value = values[key["name"]]
        setRegistry(key["root"], key["path"], key["name"], key["valType"], value)
