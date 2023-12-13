from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponseRedirect
from django.contrib import messages
from django.shortcuts import render
from django.urls import reverse
from django.db.models import Max, Value
from django.db.models.functions import Coalesce
from .models import User, Listing, Bid, Comment


def index(request):
    listings = Listing.objects.filter(is_active = True)
    for listing in listings:
        highest_bid = Bid.objects.filter(listing=listing).aggregate(max_bid=Coalesce(Max('amount'), Value(listing.starting_bid)))['max_bid']
        listing.current_price = highest_bid
        listing.save()

    return render(request, "auctions/index.html", {
        "listings" : listings
    
    })

def login_view(request):
    if request.method == "POST":

        # Attempt to sign user in
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)

        # Check if authentication successful
        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse("index"))
        else:
            return render(request, "auctions/login.html", {
                "message": "Invalid username and/or password."
            })
    else:
        return render(request, "auctions/login.html")


def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("index"))


def register(request):
    if request.method == "POST":
        username = request.POST["username"]
        email = request.POST["email"]

        # Ensure password matches confirmation
        password = request.POST["password"]
        confirmation = request.POST["confirmation"]
        if password != confirmation:
            return render(request, "auctions/register.html", {
                "message": "Passwords must match."
            })

        # Attempt to create new user
        try:
            user = User.objects.create_user(username, email, password)
            user.save()
        except IntegrityError:
            return render(request, "auctions/register.html", {
                "message": "Username already taken."
            })
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "auctions/register.html")
    
def add_listing(request):
    if not request.user.is_authenticated:
        return render(request, 'auctions/login.html', {
            "message" : "Must be logged in to create new listing"
        }) 
    
    else:
        if request.method == "POST":

            title = request.POST["title"]
            description = request.POST["description"]
            starting_bid = int(request.POST["starting_bid"])
            image_url = request.POST["image_url"]
            category = request.POST["category"]
            seller = User.objects.get(pk=request.user.id)

            listing = Listing(title=title, description=description,category=category, starting_bid=starting_bid, image_url=image_url, user=seller)
            listing.save(force_insert=True)
            

            return HttpResponseRedirect(reverse("index"))
            
        else:    
            return render(request,"auctions/add_listing.html")
        
def listing(request, listing_id):

    comments = Comment.objects.filter(listing__pk=listing_id)
    listing = Listing.objects.get(pk=listing_id)

    # is watchlist turnes to a bool response for html template.
    is_watchlist = request.user in listing.watchlist.all()
    if request.method == "POST":

        if not request.user.is_authenticated:
            return HttpResponseRedirect(reverse("login"))

        user = User.objects.get(pk=request.user.id)
        user_bid = int(request.POST["user_bid"])
        if user_bid > listing.current_price:
            listing.current_price = user_bid
            new_bid = Bid(amount=user_bid,listing=listing, user=user)
            new_bid.save(force_insert=True)
            listing.save()

            return render(request, "auctions/listing.html", {
            "listing" : listing,
            "bid" : user_bid,
            "is_watchlist" : is_watchlist,
            "comments" : comments
        })

        else:
            messages.warning(request, "Please insert a higher bid then current price.")
            return HttpResponseRedirect(reverse('listing', args=(listing.id, )))


    else:

        return render(request, "auctions/listing.html", {
            "listing" : listing,
            "is_watchlist" : is_watchlist,
            "comments" : comments

            
        })          


def watchlist(request):
    if not request.user.is_authenticated:
        return render(request, 'auctions/login.html', {
            "message" : "Must be logged in to view watchlist"
        })
    
    listings = Listing.objects.filter(watchlist=request.user)

    return render(request, "auctions/watchlist.html", {
        "listings" : listings
    })

def add_watchlist(request):
    listing_info = Listing.objects.get(pk=request.POST["listing_id"])
    user = request.user
    listing_info.watchlist.add(user)
    return HttpResponseRedirect(reverse(listing, args=(listing_info.id, )))

def remove_watchlist(request):
    listing_info = Listing.objects.get(pk=request.POST["listing_id"])
    user = request.user
    listing_info.watchlist.remove(user)
    return HttpResponseRedirect(reverse(listing, args=(listing_info.id, )))


def close_bid(request):

    listing = Listing.objects.get(pk=request.POST["listing_id"])
    bid_exist = Bid.objects.filter(listing=listing).exists()
    listing.is_active = False

    if bid_exist is not False:
        listing.winning_bid = listing.current_price
        listing.winner = request.user
    else:
        listing.winning_bid = None

    listing.save()
    
    return HttpResponseRedirect(reverse("index"))

def add_comment(request):
    user = User.objects.get(pk=request.user.id)
    listing = Listing.objects.get(pk=request.POST["listing_id"])
    new_comment = request.POST["comment"]
    comment = Comment.objects.create(content=new_comment, user=user, listing=listing)
    return HttpResponseRedirect(reverse("listing", args=(listing.id, )))

    
def categories(request):
    categories = Listing.objects.values('category').distinct()
    return render (request, "auctions/categories.html", {
        "categories" : categories
    })

def category_listing(request, category_name):
    listing = Listing.objects.filter(category=category_name, is_active=True)
    return render(request, f"auctions/category_listing.html",{
        "listings" : listing,
        "category_name": category_name
    } )








