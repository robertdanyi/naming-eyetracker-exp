import os


# EYETRACKER settings
TRACKERTYPE = 'tobii'
DUMMYMODE = False
SACCVELTHRESH = 35 # degrees per second, saccade velocity threshold
SACCACCTHRESH = 9500 # degrees per second, saccade acceleration threshold
BLINKTHRESH = 150 # milliseconds, blink detection threshold used in PyGaze method
EVENTDETECTION = 'pygaze' # Tobii offers no native method


# DISPLAY keyword arguments
MOUSEVISIBLE = False
DISPTYPE = 'psychopy'
TOBII_DISPSIZE = (1920,1200) # Tobii t60xl: (1920 x 1200) screen ratio: 16/10
STIM_DISPSIZE = (1920, 1080)  #... but we use this size for the stimulus
CONTROL_DISPSIZE = (1024, 768) #(2048, 1152) #?
FULLSCREEN = True
SCREENSIZE = (51.7, 32.31) # physical screen size in cm. (52.7, 29.6) are for the Dell monitor
SCREENDIST = 60.0 # centimeters; distance between screen and participant's eyes

# Foreground colour set to white
FGC = (255, 255, 255)
# Background colour set to black
BGC = (0, 0, 0)


#############
### PATHS ###

"""
A 'Logfiles' folder
and a Stimuli folder (with subfolders A1 to D8) to be added to parent dir
"""

# Path to the current file's parent folder
DIR = os.path.dirname(os.path.abspath(__file__))

# folder for logfile # CHANGED LINE
LOGDIR = os.path.join(DIR, "Logfiles") # CHANGED LINE

# Path to parent calibration folder
CALIBDIR = os.path.join(DIR, "calibrationfiles")
# Path to calibration and attention getter sounds
CALIBSOUNDDIR = os.path.join(CALIBDIR, 'calibsound')
CALIBSOUNDFILE = os.path.join(CALIBSOUNDDIR, "cen_4.wav")
ATTSOUNDFILE = os.path.join(CALIBSOUNDDIR, "cen_4_short.wav")
# Path to the calibration image
CALIBIMGDIR = os.path.join(CALIBDIR, 'calibimages')
CALIBIMG = os.path.join(CALIBIMGDIR, "glowing-star-180x180.png")
# Path to calibration video
CALIBVIDEODIR = os.path.join(CALIBDIR, 'calibvideos')
CALIBVIDEO = os.path.join(CALIBDIR, '--- cal_movie_1.mov')
# Path to attention getter image
ATT_IMG_DIR = os.path.join(CALIBIMGDIR, 'post-calibration')
ATT_IMG = os.path.join(ATT_IMG_DIR, 'att_03.png')


# Path to stimuli folder containing ordered video, image and audio lists
STIMULIDIR = os.path.join(DIR, 'stimuli')
# list of folders, each containing a video, an image and an audio file
STIMULI = os.listdir(STIMULIDIR)
STIMULI.sort()


STIMULIdict = {
                'i1': ['A1', 'C5', 'B2', 'D1'],
                'i2': ['A1', 'C5', 'B2', 'D2'],
                'i3': ['A1', 'C6', 'B2', 'D1'],
                'i4': ['A1', 'C6', 'B2', 'D2'],
                'i5': ['A2', 'C1', 'B1', 'D5'],
                'i6': ['A2', 'C1', 'B1', 'D6'],
                'i7': ['A2', 'C2', 'B1', 'D5'],
                'i8': ['A2', 'C2', 'B1', 'D6'],
                'i9': ['C5', 'A1', 'D1', 'B2'],
                'i10': ['C5', 'A1', 'D2', 'B2'],
                'i11': ['C6', 'A1', 'D1', 'B2'],
                'i12': ['C6', 'A1', 'D2', 'B2'],
                'i13': ['C1', 'A2', 'D5', 'B1'],
                'i14': ['C1', 'A2', 'D6', 'B1'],
                'i15': ['C2', 'A2', 'D5', 'B1'],
                'i16': ['C2', 'A2', 'D6', 'B1'],
                'i17': ['B2', 'D1', 'A1', 'C5'],
                'i18': ['B2', 'D2', 'A1', 'C5'],
                'i19': ['B1', 'D5', 'A2', 'C1'],
                'i20': ['B1', 'D6', 'A2', 'C1'],
                'i21': ['D1', 'B2', 'C6', 'A1'],
                'i22': ['D2', 'B2', 'C6', 'A1'],
                'i23': ['D5', 'B1', 'C2', 'A2'],
                'i24': ['D6', 'B1', 'C2', 'A2'],
                'n1': ['A3', 'C7', 'B4', 'D3'],
                'n2': ['A3', 'C7', 'B4', 'D4'],
                'n3': ['A3', 'C8', 'B4', 'D3'],
                'n4': ['A3', 'C8', 'B4', 'D4'],
                'n5': ['A4', 'C3', 'B3', 'D7'],
                'n6': ['A4', 'C3', 'B3', 'D8'],
                'n7': ['A4', 'C4', 'B3', 'D7'],
                'n8': ['A4', 'C4', 'B3', 'D8'],
                'n9': ['C7', 'A3', 'D3', 'B4'],
                'n10': ['C7', 'A3', 'D4', 'B4'],
                'n11': ['C8', 'A3', 'D3', 'B4'],
                'n12': ['C8', 'A3', 'D4', 'B4'],
                'n13': ['C3', 'A4', 'D7', 'B3'],
                'n14': ['C3', 'A4', 'D8', 'B3'],
                'n15': ['C4', 'A4', 'D7', 'B3'],
                'n16': ['C4', 'A4', 'D8', 'B3'],
                'n17': ['B4', 'D3', 'A3', 'C7'],
                'n18': ['B4', 'D4', 'A3', 'C7'],
                'n19': ['B3', 'D7', 'A4', 'C3'],
                'n20': ['B3', 'D8', 'A4', 'C3'],
                'n21': ['D3', 'B4', 'C8', 'A3'],
                'n22': ['D4', 'B4', 'C8', 'A3'],
                'n23': ['D7', 'B3', 'C4', 'A4'],
                'n24': ['D8', 'B3', 'C4', 'A4']
                }


