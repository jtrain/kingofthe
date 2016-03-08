from __future__ import unicode_literals

from django.db import models

class CheckinHit(models.Model):
    """
    One of these is created every time client pings
    back to us via the JS script.

    The "monarch" is the one with most overall pings.

    However, there is some smarts server side 
    in place to prevent people just pinging whenever they
    feel like it via automated scripts and such.
    """
    user = models.ForeignKey('auth.User')

    created_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(auto_now=True)

