from django.contrib.auth.models import AbstractUser
from django.db import models
from django.forms import ModelForm 

class User(AbstractUser):
    pass

class Category(models.Model):
    category_name = models.CharField(max_length=64)


    def __str__(self):
        return f"{self.category_name}"

class Listings(models.Model):
    title = models.CharField(blank=False, max_length=30)
    description = models.CharField(blank=True, max_length=100)
    active = models.BooleanField(null=False)
    picture = models.ImageField(upload_to='media/', null=True, blank= True)
    category = models.ForeignKey(Category, on_delete = models.CASCADE)
    start_bid = models.IntegerField(blank=False, default=1)
    watchlist = models.ManyToManyField(User, blank=True, related_name="watchlist")
    
    

    def __str__(self):
        return f" {self.id}, {self.title} {self.description}, {self.category}, {self.start_bid}, {self.picture}, {self.watchlist}"

class Bids(models.Model):
    bid_amount = models.IntegerField()
    uid = models.ForeignKey(User, on_delete=models.CASCADE, related_name="bidder")
    listid=models.ForeignKey(Listings, on_delete=models.CASCADE, related_name="list")

    def __str__(self):
        return f"{self.bid_amount} by {self.uid} on {self.listid}"


class Created_by(models.Model):
    creator = models.ForeignKey(User, on_delete= models.CASCADE, related_name="creator")
    listing = models.ForeignKey(Listings, on_delete=models.CASCADE, related_name="listing")

    def __str__(self):
        return f"{self.creator} {self.listing}"


class Comments(models.Model):
    comment = models.TextField(max_length=255, null=True, blank=True)
    user_comment = models.ForeignKey(User, on_delete=models.CASCADE)
    list_comment = models.ForeignKey(Listings, on_delete=models.CASCADE)

# Create a modelform for each model
class CategoryForm(ModelForm):
    class meta:
        model = Category
        fields = ['category_name']
class ListingsForm(ModelForm):
    class meta:
        model = Listings
        fields = ['title', 'description', 'active', 'picture', 'category', 'start_bid']
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


