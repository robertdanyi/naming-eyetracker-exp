# -*- coding: utf-8 -*-
"""
@author: robertdanyi
showing stimuli for the infant study
"""

import os
import time

from psychopy import visual, event, core
from psychopy import prefs
prefs.general['audioLib'] = ['pygame']
from psychopy import sound

import constants as c


"""
    !!!psychopy pixel screen coordinates (top left: (-dispsize[0]/2, dispsize[1]/2), center: (0,0))
"""

def playStimuli(tracker, stimuliSetList):

#    print "----------> stimuliSetList: ", stimuliSetList

    winStim = visual.Window(size=c.TOBII_DISPSIZE, fullscr=True, winType='pyglet', screen=0, units='pix', color='black', allowGUI=False)
#    winStim.mouseVisible=False

    # showing attention getter while loading other stuff
    attGetter = visual.ImageStim(winStim, image=c.ATT_IMG, size=(200,200))
    attGetter.draw()
    winStim.flip()

    # permanent stimuli
    sizerange = range(200, 80, -2) + range(80, 200, 2) # 120 frames
    sizerangeTest = range(200, 80, -4) + range(80, 200, 4) + range(200, 80, -4) + range(80, 200, 4) # 120 frames

    att_snd = sound.Sound(value=c.ATTSOUNDFILE)
    att_snd.setVolume(0.5)

    print "\n----------> Showing stimuli."

    ########################
    ##### play stimuli #####
    tracker.start_recording()  # subscribes to tobii gaze data stream, and writes the .tsv file header
    for i in range(2): # REPEATING the whole stimuli setlist
        # prepare the files
        for stimuliSet in stimuliSetList:
            folderPath = os.path.join(c.STIMULIDIR, stimuliSet)
            files = os.listdir(folderPath)

            for file in files:
                if file.endswith(".mp4"):
                    videoFile = os.path.join(folderPath, file)
                elif file.endswith(".png"):
                    testImageFile = os.path.join(folderPath, file)
                elif file.endswith(".wav"):
                    testAudioFile = os.path.join(folderPath, file)

            # stimuli
            movStim = visual.MovieStim3(winStim, videoFile, size=c.STIM_DISPSIZE, flipVert=False)
            testImage = visual.ImageStim(winStim, testImageFile, size=c.STIM_DISPSIZE)
            snd = sound.Sound(value=testAudioFile)

            tracker.log("Stimuli '{0}' started. Attention Getter on".format(stimuliSet)) # CHANGED LINE

            ##### attention_getter animation #####
            attGetter.setPos((0,0))
            att_snd.play()
            for frameN in range(120):

                attGetter.setSize((sizerange[frameN], sizerange[frameN]))
                attGetter.draw()

                winStim.flip()

            ##### video #####
            tracker.log("Video stim '{0}' started".format(stimuliSet)) # CHANGED LINE

            event.clearEvents()
            tV0 = time.clock()
            while movStim.status != visual.FINISHED:

                movStim.draw()
                winStim.flip()

                key = _getKeypress(tracker, winStim) # CHANGED LINE
                if key == 'space':
                    break

            tV1 = time.clock()
            print "----------> Duration of video stimulus: ", tV1-tV0
            if movStim.status != visual.FINISHED:
            # stop and clear video (".stop" cannot be used because of pyglet version)
                movStim.pause()
                del movStim


            ##### test image with attention getter and sound #####
            tracker.log("Test phase start - {0}".format(stimuliSet)) # CHANGED LINE
            attGetter.setPos((0,200))
            event.clearEvents()
            t0 = time.clock()
            for frameN in range(480):

                testImage.draw()

                # att getter for 2 s
                if 120 <= frameN < 240:
                    i = frameN%120
                    attGetter.setSize((sizerangeTest[i], sizerangeTest[i]))
                    attGetter.setOri(12*i)
                    attGetter.draw()

                # sound starts after 2 seconds
                if frameN == 120:
                    snd.play()

                winStim.flip()

                key = _getKeypress(tracker, winStim) # CHANGED LINE
                if key == 'space':
                    snd.stop()
                    break

            tracker.log("Test phase end - {0}".format(stimuliSet)) # CHANGED LINE
            t1 = time.clock()
            attGetter.setPos((0,0))
            attGetter.draw()
            winStim.flip()
            print "----------> Duration of 'test phase': ", t1-t0
            del snd

    tracker.stop_recording()
    winStim.close()


def _getKeypress(tracker, winStim): # CHANGED LINE
    keys = event.getKeys(keyList=['escape', 'space'])
    if keys and keys[0]=='escape':
        tracker.log("Experiment was stopped") # CHANGED LINE
        print "Experiment was stopped"
        winStim.close()
        core.quit()
    elif keys:
        return keys[0]
    else:
        return None


