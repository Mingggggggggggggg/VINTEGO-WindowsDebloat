import subprocess
import logger as log

def uninstall(data):
    results = []
    for i in data:
        print(f"Deinstalliere {i}")
        log.logMessage(f"Deinstalliere {i}")
        try:
            rs = subprocess.run(
                ["winget", "uninstall", "--id", i, "--force", "-h"],
                text=True,
                capture_output=True
            )
            print(i, rs.returncode, rs.stdout)
            log.logMessage((i, rs.returncode, rs.stdout))
            if rs.returncode != 0:
                print(f"Fehler bei {i}:\n{rs.stderr}")
                log.logMessage(f"Fehler bei {i}:\n{rs.stderr}")
        except Exception as e:
            print(f"Exception bei {i}: {e}")
            log.logMessage((i, -1, str(e)))
    
    return results
