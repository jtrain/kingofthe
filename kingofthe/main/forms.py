from django import forms
from django.conf import settings
from django.utils import timezone as tz

from .models import CheckinHit

class CheckinForm(forms.Form):
    """
    Checks that the user hasn't PINGed  in the last
    settings.MINIMUM_CHECKIN_MICROSECONDS.

    Requires the self.user attribute to be set.
    """

    def clean(self):
        now = tz.now()
        delta = tz.timedelta(microseconds=settings.MINIMUM_CHECKIN_MICROSECONDS)
        if CheckinHit.objects.filter(
                                         user=self.user,
                                         created_at__gt=now - delta).exists():
            raise forms.ValidationError("User already checked in recently.")
