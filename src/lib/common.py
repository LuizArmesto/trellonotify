# -*- coding: utf-8 -*-

try:
    from defs import *
except:
    APP_VERSION = "0.0.1"
    data_dir = "/usr/share"

APP_SHORTNAME = 'TrelloNotify'
APP_NAME = 'Trello Notifier for GNOME'

COPYRIGHT_YEAR = '2012'
COPYRIGHTS = "{app_name} - Copyright (c) {year}\n" \
             "Luiz Armesto <luiz.armesto@gmail.com>".format(
        app_name=APP_NAME, year=COPYRIGHT_YEAR)
WEBSITE = ""
AUTHORS = [
    ('Developers:'),
    'Luiz Armesto <luiz.armesto@gmail.com>',
    '',
    ('Contributors:'),
    '',
]

ARTISTS = [
    'Luiz Armesto <luiz.armesto@gmail.com>',
]


LICENSE = """{app_name}
Copyright (C) {year} - Og Maciel <ogmaciel@gnome.org>.

BillReminder is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

BillReminder is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with BillReminder.  If not, see <http://www.gnu.org/licenses/>.
""".format(app_name=APP_NAME, year=COPYRIGHT_YEAR)

API_KEY = 'b2f2e732c26b7245655b3c6b157c8412'
OAUTH_SECRET = '07b18803182cb1542fffe26096f661f1d5242fe2dc17b225c2fa9edd3f256bb0'

# Database info
DB_NAME = 'trellonotify.db'
