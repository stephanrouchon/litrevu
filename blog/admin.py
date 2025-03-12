from django.contrib import admin
from blog.models import Ticket, Review, Photo, UserFollow


# Register your models here.
@admin.register(Ticket)
class TicketAdmin(admin.ModelAdmin):
    list_display = ('title', 'description', 'user')
    search_fields = ('title', )
    list_filter = ('user',)


@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = ('headline', 'user', 'time_created')


@admin.register(Photo)
class PhotoAdmin(admin.ModelAdmin):
    list_display = ('image', 'uploader')


@admin.register(UserFollow)
class UserFollowAdmin(admin.ModelAdmin):
    list_display = ('user', 'followed_user')
