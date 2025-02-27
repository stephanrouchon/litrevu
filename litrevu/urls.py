"""
URL configuration for litrevu project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from django.contrib.auth.views import LoginView
from django.conf import settings
from django.conf.urls.static import static

import authentication.views
import blog.views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', LoginView.as_view(
        template_name='authentication/login.html',
        redirect_authenticated_user = True),
        name='login'
    ),
    path('signup/', authentication.views.signup_page, name='signup'),
    path('logout', authentication.views.logout_user, name='logout'),
    path('home/', blog.views.home, name='home'),
    path('photo/upload/', blog.views.photo_upload, name='photo_upload'),
    path('posts/create', blog.views.ticket_upload, name='ticket_create'),
    path('posts/<int:ticket_id>/edit', blog.views.edit_ticket, name='edit_ticket'),
    path('posts/<int:ticket_id>/', blog.views.view_post, name='view_ticket'),
    path('posts/', blog.views.post, name='posts'),
    path('reviews/create/', blog.views.review_create, name='review_create'),
    path('follow/<int:user_id>', blog.views.follow_user, name='follow_user'),
    path('unfollow/<int:user_id>/', blog.views.unfollow_user, name='unfollow_user'),
    path('subscriptions/',blog.views.subscriptions, name='subscriptions'),
    path('postsandreview/create', blog.views.ticket_and_review, name='ticket_and_review')
]

if settings.DEBUG:
    urlpatterns += static(
        settings.MEDIA_URL, 
        document_root=settings.MEDIA_ROOT
    )