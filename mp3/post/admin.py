from django.contrib import admin
from .models import User, ItemOffer, MoneyOffer, Message, Post, Offer

admin.site.register(Post)
admin.site.register(User)
admin.site.register(Message)
admin.site.register(Offer)
admin.site.register(ItemOffer)
admin.site.register(MoneyOffer)