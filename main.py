import datetime
import os
import sys

from pygaze.display import Display
from pygaze.keyboard import Keyboard
from pygaze.time import Time
from pygaze.logfile import Logfile

from Subject_class import Subject
from CustomTobiiTProTracker_class import CustomTobiiProTracker
from connection_check import check_connection
import constants as c
from playStimuli_psychopy import playStimuli



# check if tobii is connected
if not check_connection():
    sys.exit()

# # # # # # # # # #
# create instances

# new subject
newSubject = Subject()
newSubject.showGui()

# get the list of stimuli folders
stimuliSetList = c.STIMULIdict[newSubject.order_code]

# Tobii output logfile folder path and filename format
fulltimenow = datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
datenow = datetime.datetime.now().strftime("%Y-%m-%d")
subjectNumber = "0" + str(newSubject.subject_number) if len(str(newSubject.subject_number)) < 2 else str(newSubject.subject_number)

logfolderpath = os.path.join(c.LOGDIR, "{0}_{1}_{2}".format(subjectNumber, newSubject.subject_code, fulltimenow))
if not os.path.exists(logfolderpath):
    os.makedirs(logfolderpath)
logfilepath = os.path.join(logfolderpath, "subject{0}_{1}_{2}".format(subjectNumber, newSubject.subject_code, datenow))
logfile = logfilepath

# initialize a Timer
timer = Time()

# initialize the display for stimuli
disp = Display(disptype="psychopy", dispsize=c.TOBII_DISPSIZE, screennr=0, bgc = "grey")

# initialize the custom tobiitracker
tracker = CustomTobiiProTracker(disp, logfilepath)

# initialize a pygaze keyboard
kb = Keyboard(keylist=['space'],timeout=None)

# create a new logfile
eventlog = Logfile(filename="{0}\subj{1}_caliblog_{2}".format(logfolderpath, subjectNumber, datenow))
eventlog.write(["\nDate and time of experiment: {0}".format(datetime.datetime.now().strftime("%Y-%m-%d %H:%M"))])
eventlog.write(["Subject number: {0}".format(subjectNumber)])
eventlog.write(["Subject code: {0}".format(newSubject.subject_code)])
eventlog.write(["Stimuli setlist: {0}".format(stimuliSetList)])
eventlog.write(["Subject's age: {0} months and {1} days\n".format(newSubject.subject_age[:2], newSubject.subject_age[2:])])

eventlog.write(["\nEVENT", "TIME"])


# # # # # # # # # #
# calibration
print "------------> Infant calibration module.\n------------> Press Space to start!\n"

# wait for space pressed
kb.get_key(keylist=['space'], timeout=None, flush=True)

# call preCalibrate() function
while tracker.preCalibrate() != True:
    tracker.preCalibrate()

print("------------> Positioned. Starting calibration")
tracker.calibrate(eventlog)


# # # # # # #
# Play videos
playStimuli(tracker, stimuliSetList)


# # # # # # #
# close down experiment
print "------------> Experiment ended."
eventlog.write(["Experiment ended ", timer.get_time()])
tracker.close()
timer.expend()
