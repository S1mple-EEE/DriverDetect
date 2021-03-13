from django.contrib import admin
from django.conf.urls import url
from app import views
from django.contrib.staticfiles import views as static_view

urlpatterns = [
    url(r'login/', views.login, name='login'),
    url(r'cleartempimg/', views.cleartempimg, name='cleartempimg'),
    url(r'initialload/', views.initialload, name='initailload'),
    url(r'initialtrain/', views.initialtrain, name='initailtrain'),
    url(r'driverdetect/', views.driverdetect, name='driverdetect'),
    url(r'getVideo/', views.getVideo, name='getVideo'),
    url(r'getFaceVideo/', views.getFaceVideo, name='Face Pose Video'),
    url(r'GazeTrackVideo/',views.GazeTrackVideo,name='GazeTrackVideo'),
    url(r'^static/(?P<path>.*)$', static_view.serve),
    # url(r'',views.welcome),
]
