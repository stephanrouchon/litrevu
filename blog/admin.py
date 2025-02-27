from django.contrib import admin
from blog.models import Ticket, Review, Photo, UserFollow
# Register your models here.
admin.site.register(Ticket)
admin.site.register(Review)
admin.site.register(Photo)
admin.site.register(UserFollow)