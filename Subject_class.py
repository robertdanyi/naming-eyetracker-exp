# -*- coding: utf-8 -*-
"""
Created on Fri Sep 21 16:37:11 2018

@author: robertdanyi
"""

import os
import datetime
import Tkinter as tk
import tkMessageBox as mbox

import constants as c
from demo_playStimuli import demoPlayStimuli


class Subject(object):

    subjectsLog = os.path.join(c.LOGDIR, "subjects_log.txt")
    if not os.path.exists(subjectsLog):
        with open(subjectsLog, "w") as slog:
            slog.write("\n")

    def __init__(self):

        self.datetime_of_exp = datetime.datetime.now().strftime("%Y-%m-%d_%H-%M")

    # create GUI
    def showGui(self):

        tobii_disp = c.TOBII_DISPSIZE
        font = ("Helvetica", 16)
        gui = tk.Tk()
        gui.title("Experiment and Subject data")
        gui.geometry("600x500")
        gui.grid_rowconfigure(0, weight=1)
        gui.grid_rowconfigure(11, weight=1)
        gui.grid_columnconfigure(0, weight=1)

        # frames
        fsettings = tk.Frame(gui, width=600)
        fdata = tk.Frame(gui)
        fExitbutton = tk.Frame(gui, width=600)

        # layout
        fsettings.grid(sticky="ew", columnspan=2)
        fdata.grid(sticky="w")
        fExitbutton.grid(row=13, column=1, sticky="nsew")

        # widgets
        tk.Label(fsettings, text="Welcome to ScopeNames experiment.", font=("Helvetica", 18), fg="blue").grid(row=1, sticky="w")
        tk.Label(fsettings, text="Date and time: {}".format(datetime.datetime.now().strftime("%Y-%m-%d  %I:%M %p")), font=font).grid(row=2, sticky="w")
        tk.Label(fsettings, text="Display resolution of Tobii monitor: {}".format(tobii_disp), font=font).grid(row=3, sticky="w") # change to date

        tk.Label(fsettings, text="").grid(row=4, sticky="w")

        tk.Label(fdata, text="Condition:", anchor="nw", font=font).grid(row=5, sticky=tk.W)
        tk.Label(fdata, text=" ([i]nspection / [n]o inspection): ", anchor="nw", font=font).grid(row=6, sticky=tk.W)
        condition = tk.Entry(fdata,width=4, font=font)
        condition.grid(row=6, column = 1, sticky=tk.W)

        tk.Label(fdata, text="Order number (1-24): ", anchor="nw", font=font).grid(row=7, sticky=tk.W)
        order = tk.Entry(fdata,width=4, font=font)
        order.grid(row=7, column = 1, sticky=tk.W)

        tk.Label(fdata, text="Age of subject (MMDD): ", anchor="nw", font=font).grid(row=8, sticky=tk.W)
        age = tk.Entry(fdata,width=4, font=font)
        age.grid(column=1, row=8, sticky=tk.W)

        tk.Label(fdata, text="Gender of subject (f or m): ", anchor="nw", font=font).grid(row=9, sticky=tk.W)
        gender = tk.Entry(fdata,width=4, font=font)
        gender.grid(column=1, row=9, sticky=tk.W)

        tk.Label(fdata, text="Initials of subject: ", anchor="nw", font=font).grid(row=10, sticky=tk.W)
        initials = tk.Entry(fdata,width=4, font=font)
        initials.grid(column=1, row=10, sticky=tk.W)

        # gap column
        tk.Label(fdata, text="", anchor="nw", font=font).grid(row=5, column=2, rowspan=4, sticky=tk.W)

        # invalidity message
        validityline = tk.Label(gui, text="", anchor="nw", font=font, fg="red")
        validityline.grid(row=12, sticky=tk.W)

        # demo button
        tk.Button(fdata, font=("Helvetica", 14), bg='blue', text = "Run DEMO",
                  command = lambda: self._onDemoButton(condition, order, validityline)).grid(row=7, column=3, pady=5,sticky="w")
        # submit button
        tk.Button(fdata, font=font, bg='green', text = "SUBMIT",
                  command = lambda: self._onSubmitButton(gui, condition, order, age, gender, initials, validityline)).grid(row=9, column=3, rowspan=3, pady=5,sticky="w")
        # exit button
        tk.Button(fExitbutton, font=font, bg='red', text = "EXIT",
                  command = lambda: self._onExitButton(gui)).grid(sticky="s")

        gui.mainloop()


    def _onDemoButton(self, condition, order, validityline):

        ### validation ###
        # condition
        if condition.get() not in ["i", "n"]:
            validityline.config(text = "Invalid condition. Please enter 'i' or 'n'.")

        # order
        elif self._checkIfInputIsInt(order.get()) == False:
            validityline.config(text = "Invalid order. Please enter a number from 1 to 24.")
        elif 0 > int(order.get()) or int(order.get()) > 25:
            validityline.config(text = "Invalid order. Please enter a number from 1 to 24.")

        else:
            validityline.config(text = "")

            result = mbox.askokcancel("DEMO MODE", "Are you sure you want to run the experiment in DEMO MODE?")
            if result:
                self.order_code = str(condition.get()) + str(order.get())
                stimuliSetList = c.STIMULIdict[self.order_code]
                demoPlayStimuli(stimuliSetList)
            else:
                return

    def _onSubmitButton(self, gui, condition, order, age, gender, initials, validityline):

        ### validation ###
        # condition
        if condition.get() not in ["i", "n"]:
            validityline.config(text = "Invalid condition. Please enter 'i' or 'n'.")
        # order
        elif self._checkIfInputIsInt(order.get()) == False:
            validityline.config(text = "Invalid order. Please enter a number from 1 to 24.")
        elif 0 > int(order.get()) or int(order.get()) > 25:
            validityline.config(text = "Invalid order. Please enter a number from 1 to 24.")
        # age
        elif self._checkIfInputIsInt(age.get()) == False:
            validityline.config(text = "Age > Please enter two digits for months, two for days.")
        elif len(str(age.get())) < 3:
            validityline.config(text = "Age > Please enter two digits for months, two for days.")
        # gender
        elif gender.get() not in ["f", "m"]:
            validityline.config(text = "Invalid gender. Please enter 'f' for female, or 'm' for male.")
        # initials
        elif len(str(initials.get())) < 2:
            validityline.config(text = "Please enter initials of subject (2-4 letters).")

        else:
            self.order_code = str(condition.get()) + str(order.get())
            order = "0" + str(order.get()) if len(str(order.get())) == 1 else str(order.get())
            self.subject_code = str(condition.get()) + order + str(initials.get()) + str(gender.get())
            self.subject_age = age.get()
            self._writeSubjectLog()
            gui.destroy()


    def _onExitButton(self, gui):
        gui.destroy()


    def _writeSubjectLog(self):
        with open(Subject.subjectsLog, "a+") as slog:
            data = slog.readlines()
            if len(data) > 1:
                self.subject_number = int(data[-1]) + 1
                print "subject nr: ", self.subject_number
            else:
                self.subject_number = 1

            slog.write("\n\nTime of experiment: {0}\nSubject nr: {1}\nSubject code: {2}\nSubject age: {3}\n{1}"
                       .format(self.datetime_of_exp, self.subject_number, self.subject_code, self.subject_age))


    def _checkIfInputIsInt(self, number):
        try:
            int(number)
        except ValueError:
            return False
        return True



