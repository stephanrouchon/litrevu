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


from blog.views import follow_user, block_user, photo_upload, unblock_user, UserPostViews, TicketCreateView
from blog.views import TicketDetailView, TicketUpdateView, TicketDeleteView,  FollowDeleteView, SubscriptionsView
from blog.views import ReviewCreateView, ReviewDetailView, ReviewDeleteView, ReviewUpdateView, TicketAndReviewCreateView
from blog.views import FluxView, BlockUserView, UnblockUserView
from blog.views import search_users

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', LoginView.as_view(
        template_name= 'authentication/login.html',
        redirect_authenticated_user= True),
        name='login'
    ),
    path('signup/', authentication.views.signup_page, name='signup'),
    path('logout', authentication.views.logout_user, name='logout'),
    path('home/', FluxView.as_view(), name='home'),
    path('photo/upload/', photo_upload, name='photo_upload'),
    path('tickets/create', TicketCreateView.as_view(), name='ticket_create'),
    path('tickets/<int:pk>/edit', TicketUpdateView.as_view(), name='edit_ticket'),
    path('tickets/<int:pk>/', TicketDetailView.as_view(), name='view_ticket'),
    path('tickets/<int:pk>/delete', TicketDeleteView.as_view(), name='ticket_delete'),
    path('reviews/<int:pk>/create/', ReviewCreateView.as_view(), name='review_create'),
    path('reviews/<int:pk>/', ReviewDetailView.as_view(), name='view_reviews'),
    path('reviews/<int:pk>/delete', ReviewDeleteView.as_view(), name='review_delete'),
    path('reviews/<int:pk>/edit', ReviewUpdateView.as_view(), name='review_edit'),
    path('follow/<int:user_id>', follow_user, name='follow_user'),
    path('unfollow/<int:pk>/', FollowDeleteView.as_view(), name='unfollow_user'),
    path('subscriptions/', SubscriptionsView.as_view(), name='subscriptions'),
    path('ticketsandreviews/create', TicketAndReviewCreateView.as_view(), name='ticket_and_review'),
    path('posts/', UserPostViews.as_view(), name='posts'),
    path("search/", search_users, name="search_users"),
    path('block/<int:pk>', BlockUserView.as_view(), name='block_user'),
    path('unblock/<int:pk>', UnblockUserView.as_view(), name='unblock_user')
]

if settings.DEBUG:
    urlpatterns += static(
        settings.MEDIA_URL, 
        document_root=settings.MEDIA_ROOT
    )