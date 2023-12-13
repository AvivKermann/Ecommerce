from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    pass

class Listing(models.Model):
    title = models.CharField(max_length=64)
    description = models.CharField(max_length=200)
    category = models.CharField(max_length=64, null=True)
    starting_bid = models.IntegerField(max_length=10000, default=0)
    winning_bid = models.IntegerField(max_length=10000, null=True, blank=True, )    
    current_price = models.IntegerField(max_length=10000, null=True, blank=True)
    image_url = models.URLField(blank=True)
    date = models.DateTimeField(auto_now_add=True)
    is_active = models.BooleanField(default=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="seller")
    watchlist= models.ManyToManyField(User, blank=True, null=True, related_name="on_watchlist")
    winner = models.ForeignKey(User,blank=True, null=True, default=None, on_delete=models.CASCADE)

class Bid(models.Model):
    amount = models.IntegerField(max_length=100000, null=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="buyer")
    listing = models.ForeignKey(Listing, on_delete=models.CASCADE)

class Comment(models.Model):
    content = models.CharField(max_length=100)
    date = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    listing = models.ForeignKey(Listing, on_delete=models.CASCADE)





