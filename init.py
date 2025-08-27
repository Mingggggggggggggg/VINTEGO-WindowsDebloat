import argparse
import os
import sys
import debloat as db
import dataManager as dM
import setTelemetry as sT
import logger as log


dataPath = f"C:\\VINTEGO-Technik\\Data"
dataFile = "debloatList.json"
fullDataPath = os.path.join(dataPath, dataFile)

def getArgs():
    parser = argparse.ArgumentParser(
        prog=r"""
 __     _____ _   _ _____ _____ ____  ___                     
 \ \   / /_ _| \ | |_   _| ____/ ___|/ _ \                    
  \ \ / / | ||  \| | | | |  _|| |  _| | | |                   
   \ V /  | || |\  | | | | |__| |_| | |_| |                   
  __\_/ _|___|_|_\_|_|_| |_____\____|\___/  _____           _ 
 |  _ \| ____| __ )| |   / _ \  / \|_   _| |_   _|__   ___ | |
 | | | |  _| |  _ \| |  | | | |/ _ \ | |     | |/ _ \ / _ \| |
 | |_| | |___| |_) | |__| |_| / ___ \| |     | | (_) | (_) | |
 |____/|_____|____/|_____\___/_/   \_\_|     |_|\___/ \___/|_|
                                                              
""",
        description=(
            "VINTEGO Debloat Tool"
            "Tool zum Entfernen von Bloatware und Deaktivieren von Telemetrieeinstellungen in Windows über Ninja"
        ),
    add_help=True
    )
    
    mode_group = parser.add_mutually_exclusive_group()
    mode_group.add_argument(
        "-d", "--debloat",
        action="store_true",
        help="Deinstalliere Bloatware aus einer Liste"
    )
    mode_group.add_argument(
        "-t", "--telemetry",
        action="store_true",
        help="Deaktiviere Telemetrieeinstellungen aus einer Liste"
    )


    parser.add_argument(
        "-e", "--exclude",
        type=str,
        help="Ausnahmen eingeben, die nicht deinstalliert werden sollen. Mehrere Ausnahmen koennen mit Kommata voneinander getrennt werden"
    )

    parser.add_argument(
        "-i", "--include",
        type=str,
        help="Weitere Programme, zur Deinstallation eingeben. [Nur bei --debloat]"
    )

    return parser.parse_args()

def main():
    args = getArgs()
    log.cleanLog()
    print(r"""
------------------------------------------------------------------
 __     _____ _   _ _____ _____ ____  ___                     
 \ \   / /_ _| \ | |_   _| ____/ ___|/ _ \                    
  \ \ / / | ||  \| | | | |  _|| |  _| | | |                   
   \ V /  | || |\  | | | | |__| |_| | |_| |                   
  __\_/ _|___|_|_\_|_|_| |_____\____|\___/  _____           _ 
 |  _ \| ____| __ )| |   / _ \  / \|_   _| |_   _|__   ___ | |
 | | | |  _| |  _ \| |  | | | |/ _ \ | |     | |/ _ \ / _ \| |
 | |_| | |___| |_) | |__| |_| / ___ \| |     | | (_) | (_) | |
 |____/|_____|____/|_____\___/_/   \_\_|     |_|\___/ \___/|_|
-------------------------------------------------------------------                                                              
"""
    )

    if args.debloat:
        data = dM.processData(fullDataPath, "debloat", args.exlude, args.include)
        db.uninstall(data)
        pass
    
    if args.telemetry:
        data = dM.processData(fullDataPath, "telemetry", args.exlude)
        sT.initTelemetry(data, False)
        pass


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("Anwendung durch Nutzer beendet")