from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from django.db.models import Max
from django.forms import ModelForm

from .models import *
from .forms import *


def index(request):
    listings = Listings.objects.filter(active=True)
    print(len(listings))
    
    
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


def category(request):
    list_of_categories = Category.objects.all()
    return render(request, "auctions/categories.html",{
        "category" : list_of_categories
    })
def list_category(request, category_id):
    category_list = Category.objects.get(pk=category_id)
    print(category_list)
    list = Listings.objects.filter(category=category_list)
    print(list)
    return render(request, "auctions/list_category.html",{
        "list": list
    })



@login_required
def create_listing(request, user_id):
    user = User.objects.get(pk=user_id)

    print(user.id)

    if request.method =="POST":
        listform = ListingsForm(request.POST or None, request.FILES or None)
        if listform.is_valid():
            title = listform.cleaned_data["title"]
            description =listform.cleaned_data["description"]
            active = listform.cleaned_data["active"]
            picture = listform.cleaned_data["picture"]
            category = listform.cleaned_data["category"]
            start_bid = listform.cleaned_data["start_bid"]

            new_listing = Listings(title = title, description = description, active = active, picture = picture, category=category, start_bid = start_bid)
            new_listing.save()
            #new_list = Listings.objects.values_list('id').get(title=title)
            created_by = Created_by(creator = user, listing= new_listing)
            create = Created_by.objects.filter(creator=user)
            created_by.save()
            
            return HttpResponseRedirect(reverse("index"))
                


    else:
        return render(request, "auctions/create_listing.html", {
            "listform" : ListingsForm(),
            "user_id" : user.id
        
        })

@login_required
def listing(request, list_id):
    # Select the list through its id:
    exact_item = Listings.objects.get(pk=list_id)
    
    # Determine who created this listing?
    owner = Created_by.objects.get(listing=exact_item)
    allcomments = Comments.objects.filter(list_comment=exact_item).all()

    signed_user = User.objects.get(pk=request.user.id)
    #print(signed_user)
    ##############
    # Check if the item inside watchlist
    wlcheck = signed_user.watchlist.filter(id=exact_item.id).exists()
    if wlcheck:
        if(request.GET.get('remove')):
            signed_user.watchlist.remove(exact_item)
            #message1= "Removed from watchlist"
            return HttpResponseRedirect(reverse("listing", args=(list_id,)))

            #return HttpResponseRedirect(reverse("listing", args=(list_id,)))
    else:
        if(request.GET.get('add')):
            signed_user.watchlist.add(exact_item)
            #message2 = "Added to watchlist"
            return HttpResponseRedirect(reverse("listing", args=(list_id,)))
            
            
            #return HttpResponse("add")
            # return HttpResponseRedirect(reverse("listing", args=(list_id,)))
        #print("out")
    
    ## Determine if the user is signed in and is the one who created the listing
    if request.user == owner.creator:
        possessor = True
        
    else:
        possessor=False
    if request.GET.get('close'):
        bid_happend = exact_item.list.filter(bid_amount=exact_item.start_bid)
        if not bid_happend:
            return HttpResponse("The auction for this item has not yet started")
        else:
            return HttpResponseRedirect(reverse("closedbid",args=(list_id,)))
            

    if request.method=="POST":
        if 'bid' in request.POST:
            bidform = BidsForm(request.POST or None)
            bidder = User.objects.get(pk=request.user.id)
           

            #Checking form validity 
            if bidform.is_valid():
                current_bid = bidform.cleaned_data["bid_amount"]
                
                #Compare between the bidding value and the current bid
                if exact_item.start_bid < current_bid:
                    exact_item.start_bid = current_bid
                    exact_item.save()
                    # Bid table must be updated
                    bid_update = Bids(bid_amount=current_bid, uid=bidder, listid=exact_item)
                    bid_update.save()
                    print(bid_update)

            return HttpResponseRedirect(reverse("listing", args=(list_id,)))
        
        #Enter a new Comment
        comments = CommentsForm(request.POST or None)
        if comments.is_valid():
            user_comment = User.objects.get(pk=request.user.id)
            comment = comments.cleaned_data["comment"]
            ucomment= Comments(comment=comment, user_comment=user_comment, list_comment=exact_item)
            ucomment.save()
            return HttpResponseRedirect(reverse(listing, args=(list_id,)))




    return render(request, "auctions/listing.html",{
        "list_id" :list_id,
        "item" : exact_item,
        "createdby" : owner,
        "allcomments" : allcomments,
        "comments": CommentsForm(),
        "bidform" : BidsForm(),
        "wlcheck" : wlcheck,
        "possessor" :possessor,
        
    })

@login_required
def watchlist(request, user_id):
    user = User.objects.get(pk=user_id)
    watchlist = user.watchlist.all()
    return render(request, "auctions/watchlist.html",{
        "user": user,
        "watchlist" : watchlist
    })
#def watchlistremove(request, list_id):
 #   list = Listings.objects.get(pk=list_id)
    
def closedlist(request):
    non_active = Listings.objects.filter(active=False)
    
    return render(request, "auctions/closedlist.html",{
        "non_active" : non_active,

    })

def closedbid(request, list_id):
    item = Listings.objects.get(pk=list_id)
    max_bid = item.list.aggregate(Max('bid_amount'))
    winner = item.list.get(bid_amount=max_bid["bid_amount__max"])
    winner = winner.uid
    item.active=False
    item.save()

    return render(request, "auctions/closedbid.html",{
        "winner" : winner
    })

    

    




    #return HttpResponse("The owner is ")

