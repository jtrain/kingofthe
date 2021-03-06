import time
import uuid

from django.conf import settings
from django.core.urlresolvers import reverse
from django.core.cache import cache
from django.db.models import Count
from django.http import JsonResponse
from django.shortcuts import redirect, render
from django.views.generic.list import ListView
from django.views.generic.edit import FormView
from django.views.generic import View
from django.template.defaultfilters import slugify

from django.contrib.auth.models import User

from .forms import CheckinForm
from .models import CheckinHit
from .tasks import maybe_increment_hit

class IndexView(ListView):

    queryset = User.objects.annotate(num_hits=Count('checkinhit')).order_by(
                '-num_hits')

    def get(self, request):
        if not self.request.user.is_authenticated():

            uname = slugify(request.META.get('HTTP_USER_AGENT'))[:110] # length 110
            unique = uuid.uuid4().hex[:30] # length 30
            # both less than 150 char max for username

            user = User.objects.create_user(
                username=uname+unique,
                last_name=unique,
                email='fake@example.com')

            login_user(self.request, user)

        return super(IndexView, self).get(request)

class ToggleCacheView(View):
    def get(self, request):
        cache.add('iscached', False)
        iscached = not cache.get('iscached')
        cache.set('iscached', iscached)
        return redirect('index')

class CheckinPingView(View):

    def post(self, request):
        """get
        Create the checkin model for this person.

        Return a render of the highscores table.
        """
        start = time.time()
        maybe_increment_hit.delay(self.request.user.id)
        html = self._render_template()
        end = time.time()
        return JsonResponse({
                             "html": html,
                             "time": round((end - start)*1000, 0)
                             }, status=201)

    def _render_template(self):
        hits = User.objects.annotate(num_hits=Count('checkinhit')
                                     ).order_by('-num_hits')

        iscached = cache.get('iscached', False)
        if iscached:
            template_name = '_cached_high_scores.html'
        else:
            template_name = '_high_scores.html'

        return render(self.request,
                      template_name,
                      {'object_list': hits, 'iscached': iscached}).content

def login_user(request, user):
    from django.contrib.auth import load_backend, login
    if not hasattr(user, 'backend'):
        for backend in settings.AUTHENTICATION_BACKENDS:
            if user == load_backend(backend).get_user(user.pk):
                user.backend = backend
                break
    if hasattr(user, 'backend'):
        return login(request, user)
