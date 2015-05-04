# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals

from django.core.urlresolvers import reverse
from django.db.models import F
from django.http import HttpResponseRedirect
from django.views.generic import DetailView, RedirectView, TemplateView
from django.views.generic.detail import SingleObjectMixin

from .forms import ShortcutURLForm
from .library import extract_words_from_url
from .models import Shortcut


class HomePageView(TemplateView):
    template_name = 'nihtinyurl/index.html'
    form = ShortcutURLForm

    def get_context_data(self, *args, **kwargs):
        context = super(HomePageView, self).get_context_data(*args, **kwargs)
        context['form'] = self.form()
        return context

    def get_success_url(self, shortcut):
        return HttpResponseRedirect(reverse('shortcut_detail',
                                            kwargs={'keyword': shortcut.keyword}))

    def post(self, request):
        context = self.get_context_data()
        context['form'] = form = self.form(request.POST)
        if form.is_valid():
            target_url = form.cleaned_data['target']
            url_words = extract_words_from_url(target_url)
            # Original task implicitly implied reverse searching order
            url_words = list(reversed(url_words))
            search = Shortcut.objects.filter(keyword__in=url_words, target=None)
            if search:  # some corresponding word is found
                keywords = search.values_list('keyword', flat=True)
                for word in url_words:
                    if word in keywords:
                        shortcut = search.get(keyword=word)
                        shortcut.target = target_url
                        shortcut.save()
                        return self.get_success_url(shortcut)
            # No good matches, let's pick something else:
            shortcut = Shortcut.objects.filter(target=None).first()
            # If there no free space left, let's evict oldest record
            shortcut = shortcut or Shortcut.objects.earliest('updated')
            shortcut.target = target_url
            shortcut.save()
            return self.get_success_url(shortcut)

        return self.render_to_response(context)


class ShortenedURLView(DetailView):
    """Success page with shortened URL."""
    template_name = 'nihtinyurl/shortcut_detail.html'
    queryset = Shortcut.objects.filter(target__isnull=False)
    slug_url_kwarg = slug_field = 'keyword'


class ShortcutRedirectView(SingleObjectMixin, RedirectView):
    """Redirects user to stored URL and counts hits."""
    queryset = Shortcut.objects.filter(target__isnull=False)
    slug_url_kwarg = slug_field = 'keyword'
    permanent = False

    def get_redirect_url(self, *args, **kwargs):
        shortcut = self.get_object()
        shortcut.hits = F('hits') + 1
        shortcut.save()
        return shortcut.target
