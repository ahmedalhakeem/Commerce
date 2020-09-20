from django import forms
from auctions.models import *


class CategoryForm(ModelForm):
    class meta:
        model = Category
        fields = ['category_name']
class ListingsForm(ModelForm):
   
    class meta:
        model = Listings
        fields = ['title', 'description', 'active', 'picture', 'category', 'start_bid',]
        #widgets = {
         #   'title' : forms.TextInput(attrs={'class': 'form-control'}),
          #  'description' : forms.TextInput(attrs={'class': 'form-control'}), 
           # 'active' : forms.CheckboxInput(attrs={'class': 'form-control'}),
            #'picture' : forms.FileInput(attrs={'class': 'form-control'}), 
            #'category' : forms.Select(attrs={'class': 'form-control'}),
            #'start_bid' : forms.TextInput(attrs={'class': 'form-control'}), 
        #}

class BidsForm(ModelForm):
    class meta:
        model = Bids
        fields = ['bid_amount', 'uid', 'listid']
class Created_byForm(ModelForm):
    model = Created_by
    fields = ['creator', 'listing']
    
class CommentsForm(ModelForm):
    class meta:
        model = Comments
        fields = ['comment', 'user_comment', 'list_comment']

## Forms 
class ListingsForm(forms.Form):
    title = forms.CharField(required = True,widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder' : 'Title',}))
    description = forms.CharField(required = True, widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder' : 'Description',}))
    active = forms.BooleanField(label = "active", required=False, widget=forms.CheckboxInput(attrs={'class': 'form-check-label'}))
    picture = forms.ImageField(label = "upload image", required=False, widget=forms.FileInput(attrs={'class' : 'form-control-file'}))
    category = forms.ModelChoiceField(queryset=Category.objects.all(), widget=forms.Select(attrs={'class': 'form-control'}))
    start_bid = forms.IntegerField(label="Start Price", required=True, widget=forms.TextInput(attrs={'class' : 'form-control'}))

class BidsForm(forms.Form):
    bid_amount = forms.IntegerField(required=False, widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder' : 'Enter Bid' }))
    #uid = forms.ModelChoiceField(queryset=User.objects.all())
    #listid = forms.ModelChoiceField(queryset=Listings.objects.all())

class CommentsForm(forms.Form):
    comment = forms.CharField(label="Comment", widget=forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'Enter your comment', 'cols': 4, 'rows': 10}))
    #user_comment = forms.ModelChoiceField(queryset=User.objects.all(), required=False)
    #list_comment = forms.ModelChoiceField(queryset=Listings.objects.all(), required=False)

class WatchlistForm(forms.Form):
    watchlist = forms.CharField(widget= forms.HiddenInput(), required=False)
    


