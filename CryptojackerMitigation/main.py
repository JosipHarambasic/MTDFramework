import subprocess
import time
from Parser import Parser
from datetime import datetime

def mitigateCryptojacker():

    # We need to update the db to locate the actual target file
    subprocess.Popen("rm nethogs.txt", shell=True, stdout=subprocess.PIPE)
    subprocess.Popen("updatedb", shell=True, stdout=subprocess.PIPE)

    print("started network tracking")
    startNetworkTracking()
    print("finished network tracking")

    maliciousPrograms = Parser("whitelist.txt", "nethogs.txt").parse()
    if len(maliciousPrograms) > 0:
        for i in maliciousPrograms:
            try:
                subprocess.Popen("kill -9 " + i, shell=True, stdin=subprocess.PIPE)
                print("Killed process with PID: " + i)
            except:
                print("Process not found, must be already killed")
            try:
                subprocess.Popen("pkill " + maliciousPrograms[i], shell=True, stdin=subprocess.PIPE)
                print("Killing all remaining processes with the same process name: " + maliciousPrograms[i])
            except:
                print("No more processes with name '" + maliciousPrograms[i] + "'")
    else:
        print("no suspect task found")

def startNetworkTracking():
    outputFileName = "nethogs.txt"
    subprocess.Popen("nethogs -t -v 2 > " + outputFileName, shell=True, stdin=subprocess.PIPE)
    time.sleep(60)
    subprocess.Popen("pkill -f nethogs", shell=True, stdin=subprocess.PIPE)
    print("output saved in " + outputFileName)


if __name__ == '__main__':
    mitigateCryptojacker()