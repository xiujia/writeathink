from django.conf.urls import url
from . import views


app_name = 'comments'
urlpatterns = [
    url(r'^(?P<year>\d{4})/(?P<month>\d{1,2})/(?P<day>\d{1,2})/(?P<post>[-\w]+)/comment/$',
        views.post_comment, name='post_comment')
]
