from django.db import models
from . validators import valid_post_type, valid_user_type
from taggit.managers import TaggableManager

user_choices = (('student', 'Student Account'), ('professor', 'Professor Account'))
post_choices = (('academic', 'Academic Use'), ('office', 'Office Use'))

# Create your models here.
class User(models.Model):
    user_name = models.CharField(max_length=50)
    user_email = models.EmailField()
    user_password = models.CharField(max_length=16)
    user_type = models.CharField(max_length=20, choices=user_choices, default='student', validators=[valid_user_type])
    user_pic = models.ImageField(upload_to='img/user/', default='img/user/default.png')

class Post(models.Model):
    post_owner = models.ForeignKey(User, on_delete=models.CASCADE)
    post_name = models.CharField(max_length=30)
    post_description = models.TextField()
    post_price = models.PositiveIntegerField(default=0)
    post_posted = models.DateTimeField(auto_now=True)
    post_type = models.CharField(max_length=20, choices=post_choices, default='academic', validators=[valid_post_type])
    post_course = models.CharField(default="N/A", max_length=15)
    post_pic = models.ImageField(upload_to='img/posts/', default='img/posts/default.jpg')
    post_tags = TaggableManager()

class Message(models.Model):
    message = models.TextField(default="")
    mFrom = models.ForeignKey(User, on_delete=models.CASCADE, related_name="receiver", unique=False)
    mTo = models.ForeignKey(User, on_delete=models.CASCADE, related_name="sender", unique=False)
    dateSent = models.DateTimeField(auto_now=True)

class Offer(models.Model):
    offer_post = models.ForeignKey(Post, on_delete=models.CASCADE)
    offer_user = models.ForeignKey(User, on_delete=models.CASCADE)
    
class ItemOffer(models.Model):
    itemO_offer = models.ForeignKey(Offer, on_delete=models.CASCADE)
    item = models.ForeignKey(Post, on_delete=models.CASCADE)
    
class MoneyOffer(models.Model):
    moneyO_offer = models.ForeignKey(Offer, on_delete=models.CASCADE)
    money = models.PositiveIntegerField(default=0)