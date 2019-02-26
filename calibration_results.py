
from psychopy import visual
from psychopy.event import Mouse
from pygaze.keyboard import Keyboard

import tobii_research as tr

from coordinates_converters import tobii_norm_2_psy_px
from constants import CONTROL_DISPSIZE


"""NOTES:
   1. If points < 3, Tobii's calibration status is unsuccesful, and no calibration_result data is generated
   2. psychopy pixel screen coordinates are: top left = (-dispsize[0]/2, dispsize[1]/2), center = (0,0))
"""

def showCalibrationResults(logfiledir, calibration_result):
    """shows calibration results on control monitor (screen 0)"""

    DS=CONTROL_DISPSIZE #(2048, 1152)

    win = visual.Window(size=DS, fullscr=True, winType='pyglet', screen=1, units='pix', color='black')

    kb = Keyboard(keylist=['space', 'r'],timeout=0.1)

    # target points (calibration points) to draw clickable circles
    targetPoints = [tobii_norm_2_psy_px(p) for p in [(0.5, 0.5), (0.1, 0.9), (0.1, 0.1), (0.9, 0.9), (0.9, 0.1)]]

    clickable_circles = []
    for i in range(len(targetPoints)):
        clickable_circles.append(visual.Circle(win, lineColor='red', pos=targetPoints[i], radius=DS[0]/120, fillColor='green'))

    mouse = Mouse(visible=True,win=win)

    mousePressed = []
    for i in range(len(targetPoints)):
        mousePressed.append(False)

    # texts on screen
    infoText = visual.TextStim(win, text="Press the \'r\' key to recalibrate or \'space\' to continue and start showing stimuli",
                              pos=(0, -0.4 * DS[1]), color="white")
    infoText.autoDraw = True

    leftEyeText = visual.TextStim(win, "Left Eye", pos=(0, 0.45 * DS[1]), color="red")
    leftEyeText.autoDraw = True

    rightEyeText = visual.TextStim(win, "Right Eye", pos=(0, 0.47 * DS[1]), color="blue")
    rightEyeText.autoDraw = True

    recalibration_points = []

    # target calibration points and gaze sample points
    for point in calibration_result.calibration_points:

        target = visual.Circle(win, lineColor='green', pos=tobii_norm_2_psy_px(point.position_on_display_area), radius=DS[0]/200,
                      fillColor=None)
        target.autoDraw = True

        for sample in point.calibration_samples:
            if sample.left_eye.validity == tr.VALIDITY_VALID_AND_USED:
                leftGazePoint = visual.Circle(win, lineColor="red",
                                        pos=tobii_norm_2_psy_px(sample.left_eye.position_on_display_area),
                                        radius=DS[0]/450, lineWidth=DS[0]/450, fillColor="red")
                leftGazePoint.autoDraw = True

            if sample.right_eye.validity == tr.VALIDITY_VALID_AND_USED:
                rightGazePoint = visual.Circle(win, lineColor="blue",
                                        pos=tobii_norm_2_psy_px(sample.right_eye.position_on_display_area),
                                        radius=DS[0]/450, lineWidth=DS[0]/450, fillColor="blue")
                rightGazePoint.autoDraw = True


    key = kb.get_key()[0]
    k = 0
    while (not (key == 'space' or key == 'r')):

        key = kb.get_key()[0]

        for i in range(len(targetPoints)):
            if (mouse.isPressedIn(clickable_circles[i], buttons=[0])):
                if not mousePressed[i] and k == 0:
                    clickable_circles[i].autoDraw = True
                    mousePressed[i] = True
                    recalibration_points.append(calibration_result.calibration_points[i].position_on_display_area)
                    k = 20

                if mousePressed[i] and k == 0:
                    clickable_circles[i].autoDraw = False
                    mousePressed[i] = False
                    recalibration_points.remove(calibration_result.calibration_points[i].position_on_display_area)
                    k = 20

        win.flip()
        if k > 0:
            k -= 1

    if (key == 'space'):
        win.getMovieFrame()   # Defaults to front buffer, I.e. what's on screen now.
        win.saveMovieFrames("{0}\{1}".format(logfiledir, "calibration_results.png"))
        win.close()
        return []

    elif (key == 'r'):
        win.close()
        if len(recalibration_points) == 0:
            return [1]
        else:
            return recalibration_points






