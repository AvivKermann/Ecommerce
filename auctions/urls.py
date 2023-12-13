from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("add_listing", views.add_listing, name="add_listing"),
    path("listing/<int:listing_id>", views.listing, name="listing"),
    path("add_watchlist", views.add_watchlist, name="add_watchlist" ),
    path("remove_watchlist", views.remove_watchlist, name="remove_watchlist" ),
    path("close_bid", views.close_bid, name="close_bid"),
    path("add_comment", views.add_comment, name="add_comment"),
    path("watchlist", views.watchlist, name="watchlist"),
    path("category", views.categories, name="categories"),
    path("category/<str:category_name>", views.category_listing, name="category_listing")






]
