#!/usr/bin/env python3
#  -*- coding: utf-8 -*-
__author__ = "Ivo Woltring"
__revised__ = "$revised: 07/03/2021 19:02$"
__copyright__ = "Copyright (c) 2021 Ivo Woltring"
__license__ = "Apache 2.0"
__doc__ = """

"""

import os
import pickle

import wx

import ivonet
from ivonet.events import log
from ivonet.events.custom import ProjectHistoryEvent


def save_project(window, project):
    filename = project.title or "Untitled"
    if project.disc_total > 1:
        filename += f".Part {project.disc}"
    filename += ivonet.FILE_EXTENSION

    base_dir = None
    if project.name:
        base_dir, filename = os.path.split(project.name)
    elif project.tracks:
        base_dir = os.path.split(project.tracks[0])[0]

    default_dir = os.environ["HOME"] or os.getcwd()

    with wx.FileDialog(window,
                       message="Save file as ...",
                       defaultDir=default_dir,
                       defaultFile=f"{filename}",
                       wildcard=ivonet.FILE_WILDCARD_PROJECT,
                       style=wx.FD_SAVE
                       ) as save_dlg:

        save_dlg.SetFilterIndex(0)
        if base_dir:
            save_dlg.SetDirectory(base_dir)

        if save_dlg.ShowModal() == wx.ID_OK:
            path = save_dlg.GetPath()
            if not path.endswith(ivonet.FILE_EXTENSION):
                path += ivonet.FILE_EXTENSION
            with open(path, 'wb') as fo:
                project.name = path
                pickle.dump(project, fo)
            wx.PostEvent(window, ProjectHistoryEvent(path=path))
            log(f'Saved to: {path}')
