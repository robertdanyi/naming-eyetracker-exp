# -*- coding: utf-8 -*-
"""
Created on Thu Jun 28 18:16:09 2018
@author: robertdanyi
draws the core images of the calibration "stars"

"""

from pygaze._screen.basescreen import *
import constants as c

def drawCoreImage(screen, point, version):

    dispsize = c.TOBII_DISPSIZE # (2048, 1152)

    if (version == 0): # square
        screen.draw_rect(colour=(255, 0, 0), x=point[0]-dispsize[0]/200, y=point[1]-dispsize[1]/200, w=dispsize[0]/100, h=dispsize[0]/100, pw=1, fill=True)

    elif (version == 1):
        screen.draw_circle(colour=(0,255,0), pos=point, r=dispsize[0] / 200, pw=1, fill=True)

    elif (version == 2):
        screen.draw_polygon(pointlist=[(point[0]+dispsize[0]/160, point[1]+dispsize[1]/160),
                             (point[0]-dispsize[0]/200, point[1]+dispsize[1]/200),
                             (point[0]-dispsize[0]/150, point[1]-dispsize[1]/150),
                             (point[0]+dispsize[0]/200, point[1]-dispsize[1]/200),
                             (point[0]+dispsize[0]/120, point[1]-dispsize[1]/110)],
                             colour=(0,0,255), pw=1, fill=True)

    elif (version == 3):  # triangle
        screen.draw_polygon(pointlist=[(point[0], point[1]-dispsize[1]/120),
                             (point[0]+dispsize[0]/160, point[1]+dispsize[1]/120),
                             (point[0]-dispsize[0]/160, point[1]+dispsize[1]/120)], colour=(255, 0, 0), pw=1, fill=True)

    elif (version == 4):
        screen.draw_circle(colour=(255,0,255), pos=point, r=dispsize[0] / 200, pw=1, fill=True)


