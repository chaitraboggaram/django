from django.contrib import admin
from django.urls import path, include
from bokeh_django import autoload, static_extensions
from django.apps import apps
from django.contrib.staticfiles.urls import staticfiles_urlpatterns

import tvt.pn_app as tvt_app

pn_app_config = apps.get_app_config("bokeh_django")

urlpatterns = [
	path("admin/", admin.site.urls),
	path("", include("tvt.urls")),
]

bokeh_apps = [
	autoload("traces", tvt_app.traces),
]

urlpatterns += static_extensions()
urlpatterns += staticfiles_urlpatterns()