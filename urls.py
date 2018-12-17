
from django.urls import path
from django.conf.urls import url

from . import views



urlpatterns = [
    url('^$', views.index),
    path('new-registration/', views.signup.as_view(), name='signup'),
    path('user-login/', views.mylogin, name='meralogin'),
    path('userlogout/', views.mylogout, name='meralogout'),
    path('user-panel', views.userpanel, name='userpanel'),
    path('new-blog-entry/', views.newblog, name='newblog'),
    path('blog-success/', views.blogsuccess, name='blogsuccess'),
    path('blog-list/', views.fetchblog, name='bloglist'),
    path('update-blog/<int:pk>', views.updateblog.as_view(), name='updateblog'),
    path('delete-blog/<int:pk>', views.deleteblog, name='deleteblog'),
    path('change-password/', views.changepass, name='changepassword'),
    path('contact-us/', views.contactus, name='contactus'),
]

