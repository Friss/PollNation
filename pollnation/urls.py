from django.conf.urls import patterns, include, url
from polls import views
# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'mysite.'polls.views.home'', name='home'),
    # url(r'^mysite/', include('mysite.foo.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    url(r'^polls/', include('polls.urls', namespace="polls")),
    #url(r'^admin/', include(admin.site.urls)),
      url(r'^$', 'polls.views.IndexView', name='index'),
                       url(r'^(?P<poll_id>\d+)/$', 'polls.views.DetailsView', name='detail'), #view details

                       url(r'^(?P<poll_id>\d+)/vote/$', 'polls.views.vote', name='vote'), #process vote
                       url(r'^login$', 'polls.views.login_view', name='login'), # process login
                       url(r'^logout$', 'polls.views.logout_view', name='logout'), # process logout
                       url(r'^signup$', 'polls.views.signup', name='signup'), # process signup
                       url(r'^register$', 'polls.views.register', name='register'), # register account
                       url(r'^create$', 'polls.views.create', name='create'), # create a poll
                       url(r'^account$', 'polls.views.account', name='account'), # view account
                       url(r'^comment$', 'polls.views.comment', name='comment'), # create comment
                       url(r'^directory$', 'polls.views.directory', name='directory'), # view directory of tags
                       url(r'^search$', 'polls.views.search', name='search'), # search polls/tags
                       url(r'^(?P<poll_id>\d+)/delete/$', 'polls.views.delete', name='delete'), #process vote



)
