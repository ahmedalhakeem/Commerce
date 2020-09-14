from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("category", views.category, name="category"),
    path("list_category/<category_id>", views.list_category, name="list_category"),
    path("create_listing/<user_id>", views.create_listing, name="create_listing"),
    path("listing/<list_id>", views.listing, name="listing"),
    path("watchlist/<user_id>", views.watchlist, name="watchlist"),
    path("closedlist", views.closedlist, name="closedlist"),
    path("closedbid/<list_id>", views.closedbid, name="closedbid")
    #path("closebid/<int:list_id>", views.closebid, name="closebid")
    #path("closebid/<exact_item>", views.closebid, name="closebid")
]
