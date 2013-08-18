from django.conf.urls import patterns, url

from polls import views


urlpatterns = patterns('',
                       url(r'^$', views.IndexView, name='index'),
                       url(r'^(?P<poll_id>\d+)/$', views.DetailsView, name='detail'), #view details

                       url(r'^(?P<poll_id>\d+)/vote/$', views.vote, name='vote'), #process vote
                       url(r'^login$', views.login_view, name='login'), # process login
                       url(r'^logout$', views.logout_view, name='logout'), # process logout
                       url(r'^signup$', views.signup, name='signup'), # process signup
                       url(r'^register$', views.register, name='register'), # register account
                       url(r'^create$', views.create, name='create'), # create a poll
                       url(r'^account$', views.account, name='account'), # view account
                       url(r'^comment$', views.comment, name='comment'), # create comment
                       url(r'^directory$', views.directory, name='directory'), # view directory of tags
                       url(r'^search$', views.search, name='search'), # search polls/tags
                       url(r'^(?P<poll_id>\d+)/delete/$', views.delete, name='delete'), #process vote

)
