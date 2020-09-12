user = User.objects.get(pk=request.user.id)
        exist = user.watchlist.all()
        if exact_item in exist:
            remove = user.watchlist.remove(exact_item)
        else:
            add  = user.watchlist.add(exact_item)  
        if 'add' in request.POST:
            if request.user.is_authenticated:
                #select the username
                user = User.objects.get(pk=request.user.id)
                #Check the existence of the item in the user's watchlist page
                existence = user.watchlist.all()
                if exact_item in existence:
                    if "remove" in request.POST:
                        remove = user.watchlist.remove(exact_item)
                    
                    return HttpResponseRedirect(reverse(listing, args=(list_id,)))
                else:
                     add = user.watchlist.add(exact_item)

                     return HttpResponseRedirect(reverse(listing, args=(list_id,)))
                    #return HttpResponse(f"Mr. {user},  this {exact_item} is removed from your watchlist")
                
                print(existence)
                # Add to watchlist
               
            
            return HttpResponseRedirect(reverse(listing, args=(list_id,)))
