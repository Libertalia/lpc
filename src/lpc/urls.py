# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.conf import settings
from django.conf.urls.static import static
from django.conf.urls import url, patterns, include
from django.conf.urls.i18n import i18n_patterns
from django.contrib import admin
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from shop.views.auth import PasswordResetConfirm
from cms.sitemaps import CMSSitemap
from cms.models.pagemodel import Page


def render_robots(request):
    permission = 'noindex' in settings.ROBOTS_META_TAGS and 'Disallow' or 'Allow'
    return HttpResponse('User-Agent: *\n%s: /\n' % permission, content_type='text/plain')

i18n_urls = (
    url(r'^admin/', include(admin.site.urls)),
    url(r'^password-reset-confirm/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/$',
        PasswordResetConfirm.as_view(template_name='lpcshop/pages/password-reset-confirm.html'),
        name='password_reset_confirm'),
    url(r'^', include('cms.urls')),
)
urlpatterns = patterns('',
    url(r'^robots\.txt$', render_robots),
    url(r'^sitemap\.xml$', 'django.contrib.sitemaps.views.sitemap',
        {'sitemaps': {'cmspages': CMSSitemap}}, name='sitemap'),
    url(r'^shop/', include('shop.urls', namespace='shop')),
)

urlpatterns += i18n_patterns('', *i18n_urls)

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
