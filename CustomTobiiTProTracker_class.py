"""
A subclass of the TobiiProTracker class from the Pygaze library by Edwin Dalmaijer.
Customised calibration for infant studies.

see:
Dalmaijer, E.S., Mathôt, S., & Van der Stigchel, S. (2014). PyGaze: an open-source, cross-platform toolbox for minimal-effort programming of eye tracking experiments.
Behavior Research Methods, 46, 913-921. doi:10.3758/s13428-013-0422-2
"""

import sys
import os
import copy
import pygaze
import tobii_research as tr

from calibration_results import showCalibrationResults
from draw_functions import drawCoreImage
import constants as c

from pygaze.libtime import clock
from pygaze.libscreen import Screen
#from pygaze.sound import Sound
from pygaze._eyetracker.libtobii import TobiiProTracker
from psychopy import prefs
prefs.general['audioLib'] = ['pygame']
from psychopy import visual, sound


class CustomTobiiProTracker(TobiiProTracker):

    """A customised class for Tobii Pro EyeTracker objects
        display	--	a pygaze.display.Display instance"""

    def __init__(self, display, logfile,
                 eventdetection=c.EVENTDETECTION,
                 saccade_velocity_threshold=35,
                 saccade_acceleration_threshold=9500,
                 blink_threshold=c.BLINKTHRESH, **args):

        TobiiProTracker.__init__(self, display, logfile,
                 eventdetection=c.EVENTDETECTION,
                 saccade_velocity_threshold=35,
                 saccade_acceleration_threshold=9500,
                 blink_threshold=c.BLINKTHRESH, **args)

        # initialize screens
        self.screen = Screen(dispsize=self.disp.dispsize)
        self.c_screen = Screen(dispsize=self.disp.dispsize)

        self.screen.set_background_colour(colour=(0, 0, 0))

        self.points_to_calibrate = [self._norm_2_px(p) for p in [(0.5, 0.5), (0.1, 0.9), (0.1, 0.1), (0.9, 0.9), (0.9, 0.1)]]

        self.datafilepath = "{0}_TOBII_output.tsv".format(logfile)
        self.datafile = open(self.datafilepath, 'w')

        # create handle for psychopy window for pre-calibration video
        self.video_win = pygaze.expdisplay
        self.video_win.mouseVisible = False
        self.video_win.size = self.disp.dispsize




    def preCalibrate(self):
        """Helps position the infant while playing a video.
        returns
            Boolean indicating whether the positioning is done (True: 'space' has been pressed)
        """
        self._write_enabled = False
        self.start_recording()

        origin = (int(self.disp.dispsize[0] / 4), int(self.disp.dispsize[1] / 4))
        size = (int(2 * self.disp.dispsize[0] / 4), int(2 * self.disp.dispsize[1] / 4))

        videoFile = os.path.join(c.CALIBVIDEODIR, "--- cal_movie_1.mov")

        # Initialise a PsychoPy MovieStim
        mov = visual.MovieStim3(self.video_win, videoFile, flipVert=False)

        print("------------> Pre-calibration process started.")
        print("------------> When correctly positioned press \'space\' to start the calibration.")

        while mov.status != visual.FINISHED:
            if not self.gaze:
                continue

            self.screen.clear()

            # Add the MovieStim to a PyGaze Screen instance.
            self.screen.screen.append(mov)

            gaze_sample = copy.copy(self.gaze[-1])

            validity_colour = (255, 0, 0)

            if gaze_sample['right_gaze_origin_validity'] and gaze_sample['left_gaze_origin_validity']:
                left_validity = 0.15 < gaze_sample['left_gaze_origin_in_trackbox_coordinate_system'][2] < 0.85
                right_validity = 0.15 < gaze_sample['right_gaze_origin_in_trackbox_coordinate_system'][2] < 0.85
                if left_validity and right_validity:
                    validity_colour = (0, 255, 0)

            self.screen.draw_line(colour=validity_colour, spos=origin, epos=(origin[0] + size[0], origin[1]), pw=1)
            self.screen.draw_line(colour=validity_colour, spos=origin, epos=(origin[0], origin[1] + size[1]), pw=1)
            self.screen.draw_line(colour=validity_colour,
                                  spos=(origin[0], origin[1] + size[1]),
                                  epos=(origin[0] + size[0], origin[1] + size[1]),
                                  pw=1)
            self.screen.draw_line(colour=validity_colour,
                                  spos=(origin[0] + size[0], origin[1] + size[1]),
                                  epos=(origin[0] + size[0], origin[1]),
                                  pw=1)

            right_eye, left_eye, distance = None, None, []
            if gaze_sample['right_gaze_origin_validity']:
                distance.append(round(gaze_sample['right_gaze_origin_in_user_coordinate_system'][2] / 10, 1))
                right_pos = gaze_sample['right_gaze_origin_in_trackbox_coordinate_system']
                right_eye = ((1 - right_pos[0]) * size[0] + origin[0], right_pos[1] * size[1] + origin[1])
                self.screen.draw_circle(colour=validity_colour,
                                        pos=right_eye,
                                        r=int(self.disp.dispsize[0] / 100),
                                        pw=5,
                                        fill=True)

            if gaze_sample['left_gaze_origin_validity']:
                distance.append(round(gaze_sample['left_gaze_origin_in_user_coordinate_system'][2] / 10, 1))
                left_pos = gaze_sample['left_gaze_origin_in_trackbox_coordinate_system']
                left_eye = ((1 - left_pos[0]) * size[0] + origin[0], left_pos[1] * size[1] + origin[1])
                self.screen.draw_circle(colour=validity_colour,
                                        pos=left_eye,
                                        r=int(self.disp.dispsize[0] / 100),
                                        pw=5,
                                        fill=True)

            self.screen.draw_text(text="Current distance to the eye tracker: {0} cm.".format(self._mean(distance)),
                                  pos=(int(self.disp.dispsize[0] / 2), int(self.disp.dispsize[1] * 0.9)),
                                  colour=(255, 255, 255),
                                  fontsize=20)

            self.disp.fill(self.screen)
            self.disp.show()

            key = self._getKeyPress()
            if key == "space":
                break



        if mov.status != visual.FINISHED:
            # pause and discard video for the audio to stop as well
            mov.pause()
            self.screen.screen.remove(mov)
            #video_win.close()
            del mov
            self.screen.clear()
            clock.pause(1000)
            return True
        else:
            return False


    def calibrate(self, eventlog, calibrate=True, validate=False):
        """Calibrates the eye tracker with custom child-friendly screens.
        arguments
            eventlog          --    logfile instance
        keyword arguments
            calibrate    --    Boolean indicating if calibration should be
                        performed (default = True).
            validate    --    Boolean indicating if validation should be performed
                        (default = True).
        returns
            success    --    returns True if calibration succeeded, or False if
                        not; in addition a calibration log is added to the
                        log file and some properties are updated (i.e. the
                        thresholds for detection algorithms)
        """


        # # # #calculate thresholds (degrees to pixels)
        self.pxfixtresh = self._deg2pix(self.screendist, self.fixtresh, self.pixpercm)
        # in pixels per millisecons
        self.pxspdtresh = self._deg2pix(self.screendist, self.spdtresh / 1000.0, self.pixpercm)
        # in pixels per millisecond**2
        self.pxacctresh = self._deg2pix(self.screendist, self.accthresh / 1000.0, self.pixpercm)

        # calibration image file
        calibImg = c.CALIBIMG

        # initialize a sound
        snd = sound.Sound(value=c.CALIBSOUNDFILE)
        snd.setVolume(0.5)

        # image scaling range
        bit = 0.02
        scaleRange = ([x / 100.0 for x in range(60, 30, -2)] + [x / 100.0 for x in range(30, 60, 2)])

        if calibrate:

            if not self.eyetracker:
                print("WARNING! libtobii.TobiiProTracker.calibrate: no eye trackers found for the calibration!")
                self.stop_recording()
                return False

            calibration = tr.ScreenBasedCalibration(self.eyetracker)

            calibrating = True
            calibration.enter_calibration_mode()

            while calibrating:

                eventlog.write(["Calibration started at ", clock.get_time()])
                print "----------> Starting calibration..."

                # original (normalised) points_to_calibrate = [(0.5, 0.5), (0.9, 0.1), (0.1, 0.1), (0.9, 0.9), (0.1, 0.9)]
                # pixel values are calculated based on the normalised points. With (1920,1200):
                # self.points_to_calibrate calculated values: [(960, 600), (192, 1080), (192, 120), (1728, 1080), (1728, 120)]

                # calibration for all calibration points
                for i in range(0,len(self.points_to_calibrate)):

                    point = self.points_to_calibrate[i]

                    eventlog.write(["\nCalibrating point {0} at: ".format(point), clock.get_time()])
                    print "----------> Calibrating at point ", point

                    # play the soundfile
                    snd.play()

                    # Shrink from big size to small
                    scale = 1
                    for frameN in range(20): # 20 frames -> 1/3 sec shrinking (180 to 108)

                        self.c_screen.clear()
                        self.c_screen.draw_image(calibImg, pos=point, scale=scale)
                        drawCoreImage(self.c_screen, point, i)
                        self.disp.fill(self.c_screen)
                        self.disp.show()
                        scale = scale - bit

                    # shrink and grow while 'space' is pressed
                    s = 0
                    for frameN in range(12000): # 108 -> 54, 15 frames (1/4 s) and backwards

                        s = frameN%30
                        scale = scaleRange[s]
                        self.c_screen.clear()
                        self.c_screen.draw_image(calibImg, pos=point, scale=scale)
                        drawCoreImage(self.c_screen, point, i)
                        self.disp.fill(self.c_screen)
                        self.disp.show()

                        if self.kb.get_key(keylist=['space'],timeout=10, flush=False)[0] == 'space':
                            break

                    # collect results for point
                    normalized_point = self._px_2_norm(point)
                    collect_result = calibration.collect_data(normalized_point[0], normalized_point[1])
                    print("----------> Collecting results for point ", point)
                    eventlog.write(["Collecting result for point {0} at: ".format(point), clock.get_time()])

                    if collect_result != tr.CALIBRATION_STATUS_SUCCESS:
                        eventlog.write(["Recollecting result for point {0} at: ".format(point), clock.get_time()])
                        # Try again if it didn't go well the first time.
                        # Not all eye tracker models will fail at this point, but instead fail on ComputeAndApply.
                        calibration.collect_data(normalized_point[0], normalized_point[1])

                    # Shrink back to big size
                    scaleUp = [x / 100.0 for x in range(int(scale*100), 100, 2)]
                    for scale in scaleUp:
                        self.c_screen.clear()
                        self.c_screen.draw_image(calibImg, pos=point, scale=scale)
                        drawCoreImage(self.c_screen, point, i)
                        self.disp.fill(self.c_screen)
                        self.disp.show()


                    # image rolling to next point
                    # pixelised self.points_to_calibrate = [(960, 600), (192, 1080), (192, 120), (1728, 1080), (1728, 120)]
                    if (i < len(self.points_to_calibrate)-1):

                        """
                        screen ratio: 16/10
                        The steps for moving the images should be 16, 10 or 8, 5
                        """
                        # center -> bottom left / (960, 600) -> (192, 1080) - 48 frames
                        while point[0] >= self.points_to_calibrate[i+1][0]:
                            self.c_screen.clear()
                            point = (point[0]-16, point[1]+10)
                            self.c_screen.draw_image(calibImg, pos=point)
                            self.disp.fill(self.c_screen)
                            self.disp.show()

                        # bottom-left -> top-left / (192, 1080) -> (192, 120)
                        # AND
                        # bottom-right -> top-right / (1728, 1080) -> (1728, 120) - 80 frames
                        while point[1] > self.points_to_calibrate[i+1][1]:
                            self.c_screen.clear()
                            point = (point[0], point[1]-12)
                            self.c_screen.draw_image(calibImg, pos=point)
                            self.disp.fill(self.c_screen)
                            self.disp.show()

                        # top-left -> bottom-right / (192, 120) -> (1728, 1080) - 96 frames
                        while point[0] < self.points_to_calibrate[i+1][0] and not point[1] == self.points_to_calibrate[i+1][1]:
                            self.c_screen.clear()
                            point = (point[0]+16, point[1]+10)
                            self.c_screen.draw_image(calibImg, pos=point)
                            self.disp.fill(self.c_screen)
                            self.disp.show()


                print("------------> Calculating calibration result....")

                calibration_result = calibration.compute_and_apply()

                eventlog.write(["\nCompute and apply returned {0} and collected at {1} points.\n".
                      format(calibration_result.status, len(calibration_result.calibration_points))])
                print("------------> Compute and apply returned {0} and collected at {1} points.".
                      format(calibration_result.status, len(calibration_result.calibration_points)))



                # Show image after calibration
                self.c_screen.clear()
                self.c_screen.draw_image(c.ATT_IMG)
                self.disp.fill(self.c_screen)
                self.disp.show()

                if calibration_result.status != tr.CALIBRATION_STATUS_SUCCESS:
                    eventlog.write(["\n\nWARNING! libtobii.TobiiProTracker.calibrate: Calibration was unsuccessful!\n\n"])
                    print "Calibration was unsuccessful.\nPress 'R' to recalibrate all points\nor 'SPACE' to continue without calibration"
                    key = self.kb.get_key(keylist=['space', 'r'], timeout=None)[0]
                    if key == 'r':
                        recalibration_points = [0]
                    elif key == 'space':
                        recalibration_points = []

                else:
                    # call showCalibrationResults function to present the results on screen 0. The function returns a list
                    logfiledir = os.path.dirname(os.path.abspath(self.datafilepath))
                    recalibration_points = showCalibrationResults(logfiledir, calibration_result)

                # if the list is empty, calibration is finished
                if len(recalibration_points) == 0:
                    eventlog.write(["\nCalibration finished at ", clock.get_time()])
                    calibrating = False

                # if the list contains only '0', the calibration was unsuccessful, recalibrate all points
                elif (recalibration_points[0] == 0):
                    eventlog.write(["\nRecalibrating all points..."])
                    calibrating = True
                # if the list contains only '1', recalibrate all points despite successful calibration
                elif (recalibration_points[0] == 1):
                    eventlog.write(["\nRecalibrating all points..."])
                    for point in self.points_to_calibrate:
                        calibration.discard_data(point[0], point[1])
                    calibrating = True
                # recalibrate the returned points
                else:
                    eventlog.write(["\nRecalibrating {0} points...".format(len(recalibration_points))])
                    self.points_to_calibrate = [self._norm_2_px(p) for p in recalibration_points]
                    for point in self.points_to_calibrate:
                        calibration.discard_data(point[0], point[1])
                    calibrating = True


        calibration.leave_calibration_mode()
        eventlog.write([" Leaving calibration mode...", clock.get_time()])
        self.stop_recording()
        self._write_enabled = True
        self.disp.close()


    def _getKeyPress(self):
        key = self.kb.get_key(keylist=['space', 'escape'], flush=False)[0]
        if key and key=='escape':
            self.disp.close()
            self.close()
            sys.exit()
        elif key:
            return key
        else:
            return None



