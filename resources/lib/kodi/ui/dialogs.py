# -*- coding: utf-8 -*-
"""
    Copyright (C) 2017 Sebastian Golasch (plugin.video.netflix)
    Copyright (C) 2018 Caphm (original implementation module)
    Various simple dialogs

    SPDX-License-Identifier: MIT
    See LICENSES/MIT.md for more information.
"""
# pylint: disable=wildcard-import
from __future__ import absolute_import, division, unicode_literals

import xbmc
import xbmcgui

from resources.lib.globals import g
import resources.lib.common as common

try:  # Python 2
    unicode
except NameError:  # Python 3
    unicode = str  # pylint: disable=redefined-builtin


def show_notification(msg, title='Netflix', time=3000):
    """Show a notification"""
    xbmc.executebuiltin(g.py2_encode('Notification({}, {}, {}, {})'
                                     .format(title, msg, time, g.ICON)))


def ask_credentials():
    """
    Show some dialogs and ask the user for account credentials
    """
    email = g.py2_decode(xbmcgui.Dialog().input(
        heading=common.get_local_string(30005),
        type=xbmcgui.INPUT_ALPHANUM)) or None
    common.verify_credentials(email)
    password = ask_for_password()
    common.verify_credentials(password)
    common.set_credentials(email, password)
    return {
        'email': email,
        'password': password
    }


def ask_for_password():
    """Ask the user for the password"""
    return g.py2_decode(xbmcgui.Dialog().input(
        heading=common.get_local_string(30004),
        type=xbmcgui.INPUT_ALPHANUM,
        option=xbmcgui.ALPHANUM_HIDE_INPUT)) or None


def ask_for_rating():
    """Ask the user for a rating"""
    heading = '{} {}'.format(common.get_local_string(30019),
                             common.get_local_string(30022))
    try:
        return int(xbmcgui.Dialog().numeric(heading=heading, type=0,
                                            defaultt=''))
    except ValueError:
        return None


def ask_for_pin():
    """Ask the user for the adult pin"""
    return xbmcgui.Dialog().numeric(
        heading=common.get_local_string(30002),
        type=0,
        defaultt='') or None


def ask_for_search_term():
    """Ask the user for a search term"""
    return _ask_for_input(common.get_local_string(30003))


def _ask_for_input(heading):
    return g.py2_decode(xbmcgui.Dialog().input(
        heading=heading,
        type=xbmcgui.INPUT_ALPHANUM)) or None


def ask_for_removal_confirmation():
    """Ask the user to finally remove title from the Kodi library"""
    return ask_for_confirmation(
        common.get_local_string(30047),
        common.get_local_string(30124))


def ask_for_confirmation(title, message):
    """Ask the user to confirm an operation"""
    return xbmcgui.Dialog().yesno(heading=title, line1=message)


def ask_for_resume(resume_position):
    """Ask the user for resuming a video"""
    return xbmcgui.Dialog().contextmenu(
        [
            common.get_local_string(12022).format(common.convert_seconds_to_hms_str(resume_position)),
            common.get_local_string(12023)
        ])


def show_backend_not_ready():
    return xbmcgui.Dialog().ok(common.get_local_string(30105),
                               line1=common.get_local_string(30138))


def show_ok_dialog(title, message):
    return xbmcgui.Dialog().ok(title, message)


def show_yesno_dialog(title, message, yeslabel=None, nolabel=None):
    return xbmcgui.Dialog().yesno(title, message, yeslabel=yeslabel, nolabel=nolabel)


def show_error_info(title, message, unknown_error=False, netflix_error=False):
    """Show a dialog that displays the error message"""
    prefix = (30104, 30102, 30101)[unknown_error + netflix_error]
    return xbmcgui.Dialog().ok(title,
                               line1=common.get_local_string(prefix),
                               line2=message,
                               line3=common.get_local_string(30103))


def show_addon_error_info(exc):
    """Show a dialog to notify of an addon internal error"""
    if g.ADDON.getSettingBool('disable_modal_error_display'):
        show_notification(title=common.get_local_string(30105),
                          msg=common.get_local_string(30131))
    else:
        show_error_info(title=common.get_local_string(30105),
                        message=': '.join((exc.__class__.__name__, unicode(exc))),
                        netflix_error=False)


def show_library_task_errors(notify_errors, errors):
    if notify_errors and errors:
        xbmcgui.Dialog().ok(common.get_local_string(0),
                            '\n'.join(['{} ({})'.format(err['task_title'], err['error'])
                                       for err in errors]))
