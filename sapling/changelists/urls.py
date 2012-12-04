from django.conf.urls.defaults import *

from views import ChangeListsView

urlpatterns = patterns('',
    url(r'^(?i)Change_Lists/*$', ChangeListsView.as_view(),
        name="changelists"),
)
