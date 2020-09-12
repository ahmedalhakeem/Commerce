@login_required
def listing(request, list_id):
    # Select the list through its id:
    exact_item = Listings.objects.get(pk=list_id)
    ###$ Display all Comments
    allcomments = Comments.objects.filter(list_comment=exact_item).all()
    

    # Check the existence of the listing inside the user watchlist
    user = User.objects.get(pk=request.user.id)
    check_watchlist = user.watchlist.filter(id=exact_item.id).exists()

    print(check_watchlist)
    
    if check_watchlist:
        if(request.GET.get('remove')):
            user.watchlist.remove(exact_item)
            
            return HttpResponseRedirect(reverse("listing", args=(list_id,)))
    
    else:
        if(request.GET.get('add')):     
            user.watchlist.add(exact_item)
        

            return HttpResponseRedirect(reverse("listing", args=(list_id,)))
        


    #Recognize who created the listing:
    created = Created_by.objects.get(listing=exact_item)
    
    #Close Auctions
    if request.user == created.creator:
        owner = True
        
    else:
        owner = False
    
    if (request.GET.get('close')):
        exact_item.active=False
        exact_item.save()
        max_bid = exact_item.list.aggregate(Max('bid_amount'))
        winner = exact_item.list.get(bid_amount=max_bid["bid_amount__max"])
        winner = winner.uid

        return render(request, "auctions/listing.html",{
                "item": exact_item,
                "list_id":list_id,
                "created_by" : created,
                "form" : BidsForm(),
                "comments": CommentsForm(),
                "all_comments": allcomments,
                "owner" : owner,
                "winner" : winner,
                        
            })


    print(f"The one who created the listing is: {created.creator}")

        
         
        
        
    #check if the user submits the form
    if request.method=="POST":

        #Check to see if user clicks on bid button
        if 'bid' in request.POST:
            form = BidsForm(request.POST or None)
            bidder = User.objects.get(pk=request.user.id)
            print(f"Last bid came from  :{bidder}")

                
            
            #Checking form validity 
            if form.is_valid():
                current_bid = form.cleaned_data["bid_amount"]

                #Compare between the bidding value and the current bid 
                if exact_item.start_bid < current_bid:
                    exact_item.start_bid = current_bid
                    exact_item.save()
                    # Bid table must be updated
                    bid_update = Bids(bid_amount=current_bid, uid=bidder, listid=exact_item)

                    bid_update.save()

                    print(bid_update)

                    
                else:
                    return HttpResponse("The amount you are bidding is less than the current bid")

            return HttpResponseRedirect(reverse("listing", args=(list_id,)))
        ####################
        
        #Comments 
        comments = CommentsForm(request.POST or None)

      
        if comments.is_valid():
            commentator = User.objects.get(pk=request.user.id)
            print(commentator)
            comment = comments.cleaned_data["comment"]
            ucomment= Comments(comment=comment, user_comment=commentator, list_comment=exact_item)
            ucomment.save()


            return HttpResponseRedirect(reverse(listing, args=(list_id,)))

        ##if 'close' in request.POST:
          #  exact_item.active = False
           # exact_item.save()
            
            #max_bid = exact_item.list.aggregate(Max('bid_amount'))
            #print(max_bid)
    
          #  winner = exact_item.list.get(bid_amount=max_bid["bid_amount__max"])
           # winner = winner.uid
            
            
           
            

                     
        
    return render(request, "auctions/listing.html",{
     "item": exact_item,
     "list_id":list_id,
     "created_by" : created,
     "form" : BidsForm(),
     "comments": CommentsForm(),
     "all_comments": allcomments,
     "owner" : owner,
     "check" : check_watchlist,
     "user" : user
      
     
     
     
     
    })
