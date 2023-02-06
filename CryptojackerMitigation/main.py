import subprocess
import time
from Parser import Parser


def mitigateCryptojacker():
    # We need to update the db to locate the actual target file
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

                # Write all corresponding files to a log, that could be manually deleted if necessary
                subprocess.Popen("locate "+ maliciousPrograms[i] + " >> cjlog.txt", shell=True, stdin=subprocess.PIPE)
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
    timerOfCollectingData = 60
    subprocess.Popen("nethogs -t -v 2 > " + outputFileName, shell=True, stdin=subprocess.PIPE)
    time.sleep(timerOfCollectingData)
    subprocess.Popen("pkill -f nethogs", shell=True, stdin=subprocess.PIPE)
    print("output saved in " + outputFileName)


if __name__ == '__main__':
    mitigateCryptojacker()
