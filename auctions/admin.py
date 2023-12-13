from django.contrib import admin
from .models import User, Listing, Bid, Comment

# Register your models here.
class UserAdmin(admin.ModelAdmin):
    list_display = ("id", "username", "email", "password")

class ListingAdmin(admin.ModelAdmin):
    list_display = ("id", "title", "description", "starting_bid","winning_bid","current_price","image_url","date","is_active","user", "winner")

class BidAdmin(admin.ModelAdmin):
    list_display = ("id", "amount", "user", "listing" )

class CommentAdmin(admin.ModelAdmin):
    list_display = ("id", "content", "user", "listing")



admin.site.register(User, UserAdmin)
admin.site.register(Listing, ListingAdmin)
admin.site.register(Bid, BidAdmin)
admin.site.register(Comment, CommentAdmin)




