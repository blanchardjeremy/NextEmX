from django.conf.urls.defaults import *
from groups.views import *

urlpatterns = patterns('',
    url(r'^groups/create/',                 GroupCreateView.as_view(),  name='group_create'),
    url(r'^groups/(?P<shortname>[\w-]+)/$',    GroupDetailView.as_view(),  name='group_detail'),
)