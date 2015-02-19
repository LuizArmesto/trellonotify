# -*- coding: utf-8 -*-

import json

from gi.repository import Notify

from lib.common import APP_NAME


Notify.init(APP_NAME)


class NotificationManager(object):
    def __init__(self, member):
        self.member = member
        self.notified = []

        notifications = iter(member.get_notifications())
        self.notify(next(notifications))
        self.notify(next(notifications))

    def notify(self, notification):
        if notification.id in self.notified:
            return

        gnotification = Notify.Notification()
        gnotification.update('Trello Notification',
                json.dumps(notification.data),
                '')
        gnotification.show()

        self.notified.append(notification.id)
