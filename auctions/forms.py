from django import forms
from auctions.models import *

class ListingsForm(forms.Form):
    title = forms.CharField(label ="Title", required = True)
    description = forms.CharField(label = "description")
    active = forms.BooleanField(label = "active", required=True)
    picture = forms.ImageField(label = "upload image", required=False)
    category = forms.ModelChoiceField(queryset=Category.objects.all())
    start_bid = forms.IntegerField(label="Start Price", required=True)

class BidsForm(forms.Form):
    bid_amount = forms.IntegerField(label="enter bid")
    #uid = forms.ModelChoiceField(queryset=User.objects.all())
    #listid = forms.ModelChoiceField(queryset=Listings.objects.all())

class CommentsForm(forms.Form):
    comment = forms.CharField(label="Comment", widget=forms.Textarea)
    user_comment = forms.ModelChoiceField(queryset=User.objects.all())
    list_comment = forms.ModelChoiceField(queryset=Listings.objects.all())


