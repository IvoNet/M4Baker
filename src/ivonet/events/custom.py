#!/usr/bin/env python3
#  -*- coding: utf-8 -*-
__author__ = "Ivo Woltring"
__revised__ = "$revised: 07/03/2021 09:36$"
__copyright__ = "Copyright (c) 2021 Ivo Woltring"
__license__ = "Apache 2.0"
__doc__ = """

"""

import wx.lib.newevent

# New Event type
(ProcessDoneEvent, EVT_PROCESS_DONE) = wx.lib.newevent.NewEvent()
