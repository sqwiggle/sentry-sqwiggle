from django import forms
from django.conf import settings

from sentry.plugins.bases import notify
from sentry.utils import json

import sentry_sqwiggle
import logging
import urllib
import urllib2
from cgi import escape

class SqwiggleOptionsForm(notify.NotificationConfigurationForm):
    webhook_url = forms.CharField(
        help_text='Your Sqwiggle webhook URL.',
        label='Webhook URL',
        widget=forms.TextInput(
        attrs={'class': 'span12'}
    )
  )

class SqwiggleMessage(notify.NotificationPlugin):
    title = 'Sqwiggle'
    slug = 'sqwiggle'
    description = 'Event notifications for Sqwiggle.'

    author = 'Your Name'
    author_url = 'https://github.com/yourname/sentry_pluginname'

    resource_links = [
        ('Bug Tracker', 'https://github.com/sqwiggle/sentry-sqwiggle/issues'),
        ('Source', 'https://github.com/sqwiggle/sentry-sqwiggle'),
    ]

    version = sentry_sqwiggle.VERSION

    conf_title = title
    conf_key = 'sqwiggle'

    project_conf_form = SqwiggleOptionsForm
    logger = logging.getLogger('sentry.errors')

    def is_configured(self, project):
        return all((self.get_option(k, project) for k in ('webhook_url',)))

    def notify_users(self, group, event, fail_silently=False):
        webhook = self.get_option('webhook_url', event.project)

        project_name = escape(event.project.name.encode('utf-8'))
        project_url = group.get_absolute_url()

        team_name = escape(event.team.name.encode('utf-8'))
        event_type = 'New event' if group.times_seen == 1 else 'Regression'

        message = getattr(group, 'message_short', group.message).encode('utf-8')
        culprit = getattr(group, 'title', group.culprit).encode('utf-8')

        if message == culprit:
            culprit = ''

        payload = {
            'project_name': project_name,
            'project_url': project_url,
            'team_name': team_name,
            'event_type': event_type,
            'error_message': message,
            'error_culprit': culprit,
        }

        request = urllib2.Request(webhook)

        request.add_header('Content-Type', 'application/json')
        request.add_header('User-Agent', 'sentry-sqwiggle/%s' % (self.version))

        try:
            return urllib2.urlopen(request, json.dumps({'payload': payload})).read() 
        except urllib2.URLError:
            self.logger.error('Error connecting to Sqwiggle.', exc_info=True)
            raise
        except urllib2.HTTPError as e:
            self.logger.error('Error posting to Sqwiggle: %s', e.read(), exc_info=True)
            raise
