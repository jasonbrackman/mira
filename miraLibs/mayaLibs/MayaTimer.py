# -*- coding: utf-8 -*-
import logging
import PySide.QtCore as QtCore
import maya.OpenMaya as OpenMaya


SecPerMin = 60
MsecPerSec = 1000


class MayaTimer(object):
    def __init__(self, event=None, duration=20, slot=None):
        """

        Args:
            duration: during time, in minutes.
            slot: a function which will be executed when time up

        Returns:

        """
        self.__duration_msec = duration*SecPerMin*MsecPerSec
        self.__slot = slot
        self.__timer = None

        if event:
            self.event_message = OpenMaya.MEventMessage()
            self.event_message.addEventCallback(event, self.restart)

    @property
    def duration(self):
        minutes = self.__duration_msec/SecPerMin/MsecPerSec
        return minutes

    @duration.setter
    def duration(self, value):
        if not isinstance(value, int) or isinstance(value, float):
            logging.error("valueError: must be a number...")
            return
        self.__duration_msec = value*SecPerMin*MsecPerSec

    @property
    def slot(self):
        return self.__slot

    @slot.setter
    def slot(self, func):
        if not callable(func):
            logging.error("valueError: must be a function...")
            return
        self.__slot = func

    def restart(self, *args, **kwargs):
        self.stop()
        self.start()

    def start(self):
        self.__timer = QtCore.QTimer()
        self.__timer.setSingleShot(True)
        self.__timer.timeout.connect(self.__trigger)
        self.__timer.start(self.__duration_msec)

    def stop(self):
        if self.__timer:
            self.__timer.stop()
            self.__timer.deleteLater()
            self.__timer = None

    def __trigger(self):
        if not self.slot:
            logging.warning("no slot function. nothing will happen.")
            return
        self.__slot()


if __name__ == "__main__":
    pass
