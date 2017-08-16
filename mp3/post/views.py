import math

from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.http import HttpResponseRedirect
from django.shortcuts import render
from .models import Post, ItemOffer, MoneyOffer, Offer, Message
from .forms import SearchPost, UserLogin, UserRegister, User, PostItem, OfferItem, OfferMoney


# Create your views here.
def viewPosts(request, user=None, page=None):
    initial = {}
    limit = 10
    page = 1
    post = Post.objects.all()
    p = Post

    if 'page' in request.GET:
        page = request.GET['page']

    if 'limit' in request.GET:
        if  request.GET['limit'] is 15:
            limit = 15
        elif request.GET['limit'] is 20:
            limit = 20

    if user is not None:
        try:
            post = post.objects.filter(post_owner_id=user)
        except Post.DoesNotExist:
            post = Post.objects.all()

    if 'post_type' in request.GET:
        if request.GET['post_type'] == 'academic' or request.GET['post_type'] == 'office':
            post = post.filter(post_type=request.GET['post_type'])
        else:
            post = Post.objects.all()

    if 'post_tags' in request.GET:
        if request.GET['post_tags']:
            post = Post.objects.filter(post_tags__name__in=request.GET['post_tags'].split())

    if 'post_type' in request.GET:
        initial['post_type'] = request.GET['post_type']

    if 'limit' in request.GET:
        initial['limit'] = request.GET['limit']

    if 'post_tags' in request.GET:
        initial['post_tags'] = request.GET['post_tags']

    if user is not None:
        searchForm = SearchPost(initial=initial, userId=user)
    else:
        searchForm = SearchPost(initial=initial)

    page = int(page)
    pages = math.ceil(post.count() / limit)
    post = post.order_by('-post_posted')
    paginator = Paginator(post, limit)

    try:
        paginator = paginator.page(page)
    except PageNotAnInteger:
        paginator = paginator.page(1)
    except EmptyPage:
        paginator = paginator.page(paginator.num_pages)

    return render(request, 'posts.html', {'page': page, 'pages': pages, 'data': paginator, 'form': searchForm})

def profile(request, user=None):
    initial = {}
    limit = 10
    page = 1
    post = Post
    searchForm = SearchPost
    account = None

    if 'page' in request.GET:
        page = request.GET['page']

    if 'limit' in request.GET:
        if request.GET['limit'] is 15:
            limit = 15
        elif request.GET['limit'] is 20:
            limit = 20

    if user is not None:
        try:
            post = post.objects.filter(post_owner_id=user)
        except Post.DoesNotExist:
            post = Post.objects.all()
    elif 'user' in request.GET:
        post = post.objects.filter(post_owner_id=request.GET['user'])
    elif 'uid' in request.session:
        post = post.objects.filter(post_owner_id=request.session['uid'])

    if 'post_type' in request.GET:
        if request.GET['post_type'] == 'academic' or request.GET['post_type'] == 'office':
            post = post.objects.filter(post_type=request.GET['post_type'])
        else:
            post = Post.objects.all()

    if 'post_tags' in request.GET:
        if request.GET['post_tags']:
            post = Post.objects.filter(post_tags__name__in=request.GET['post_tags'].split())

    if 'post_type' in request.GET:
        initial['post_type'] = request.GET['post_type']

    if 'limit' in request.GET:
        initial['limit'] = request.GET['limit']

    if 'post_tags' in request.GET:
        initial['post_tags'] = request.GET['post_tags']

    if user is not None:
        account = User.objects.get(id=user)
        searchForm = SearchPost(initial=initial, userId=user)
    elif 'user' in request.GET:
        account = User.objects.get(id=request.GET['user'])
        searchForm = SearchPost(initial=initial, userId=request.GET['user'])
    elif 'uid' in request.session:
        account = User.objects.get(id=request.session['uid'])
        searchForm = SearchPost(initial=initial, userId=request.session['uid'])

    page = int(page)
    pages = math.ceil(post.count() / limit)
    post = post.order_by("-post_posted")
    paginator = Paginator(post, limit)

    try:
        paginator = paginator.page(page)
    except PageNotAnInteger:
        paginator = paginator.page(1)
    except EmptyPage:
        paginator = paginator.page(paginator.num_pages)

    return render(request, 'profile.html', {'page': page, 'pages': pages, 'data': paginator, 'form': searchForm, 'account': account})

def logout(request):
    request.session.flush()
    return HttpResponseRedirect("/")

def post(request):
    form = SearchPost()
    postForm = PostItem()

    if 'uid' not in request.session:
        return HttpResponseRedirect('/')
    else:
        if request.method == 'POST':
            postForm = PostItem(data=request.POST, files=request.FILES)

            if postForm.is_valid():
                post = postForm.save(commit=False)
                post.post_owner = User.objects.get(id=request.session['uid'])
                post.save()
                postForm.save_m2m()

                return profile(request)
            else:
                return render(request, 'post.html',
                              {'form': form, 'post': postForm, 'error': postForm.errors})
        else:
            return render(request, 'post.html', {'form': form, 'post': postForm})


def login(request):
    form = SearchPost()
    loginForm = UserLogin()

    if 'uid' in request.session:
        return HttpResponseRedirect('/profile/')
    else:
        if request.method == 'POST':
            loginForm = UserLogin(data=request.POST, files=request.FILES)

            if loginForm.is_valid():
                try:
                    user = User.objects.get(user_email=loginForm.cleaned_data.get('user_email'))

                    try:
                        user = User.objects.get(user_email=loginForm.cleaned_data.get('user_email'), user_password=loginForm.cleaned_data.get('user_password'))

                        request.session.flush()
                        request.session['uid'] = user.id

                        return HttpResponseRedirect('/profile/')
                    except User.DoesNotExist:
                        return render(request, 'login.html', {'form': form, 'login': loginForm, 'error': 'Password is incorrect'})

                except User.DoesNotExist:
                    return render(request, 'login.html', {'form': form, 'login': loginForm, 'error': 'Account does not exist'})
            else:
                print(loginForm.errors)
                return render(request, 'login.html',
                              {'form': form, 'login': loginForm, 'error': loginForm.errors})
        else:
            return render(request, 'login.html', {'form': form, 'login': loginForm})

def register(request):
    form = SearchPost()
    regisForm = UserRegister()

    if 'uid' in request.session:
        return HttpResponseRedirect('/profile/')
    else:
        if request.method == "POST":
            regisForm = UserRegister(data=request.POST)

            if regisForm.is_valid():
                user = User.objects.filter(user_email=regisForm.cleaned_data.get("user_email"))

                if user.count() <= 0:
                    regisForm.save()

                    return HttpResponseRedirect("/login/")
                else:
                    return render(request, 'register.html',
                                  {'form': form, 'register': regisForm, 'error': 'Email is already used'})
            else:
                return render(request, 'register.html',
                              {'form': form, 'register': regisForm, 'error': 'An error occurred while registering'})
        else:
            return render(request, 'register.html', {'form': form, 'register': regisForm})


def viewItem(request):
    if 'uid' in request.session and 'item' in request.GET:
        post = Post.objects.get(id=request.GET['item'])
        offer = None

        if 'view' in request.GET:
            if request.GET['view'] == 'items':
                offer = ItemOffer.objects.filter(itemO_offer__offer_post=post)

                if offer.count() == 0:
                    offer = None

                return render(request, 'viewItem.html',
                              {'post': post, 'form': SearchPost(), 'item': request.GET['item'], 'displayItem': offer})
            else:
                offer = MoneyOffer.objects.filter(moneyO_offer__offer_post=post)

                if offer.count() == 0:
                    offer = None

                return render(request, 'viewItem.html',
                              {'post': post, 'form': SearchPost(), 'item': request.GET['item'], 'displayMoney': offer})

        try:
            offerU = Offer.objects.get(offer_post_id=request.GET['item'], offer_user_id=request.session['uid'])

            try:
                offer = ItemOffer.objects.get(itemO_offer=offerU)
            except ItemOffer.DoesNotExist:
                try:
                    offer = MoneyOffer.objects.get(moneyO_offer=offerU)
                except MoneyOffer.DoesNotExist:
                    offer = None
        except Offer.DoesNotExist:
            offer = None

        if offer == None:
            if 'itemOffer' in request.POST:
                return render(request, 'viewItem.html', {'post': post, 'form': SearchPost(), 'offer': OfferItem(user=request.session['uid']), 'item': request.GET['item']})
            elif 'moneyOffer' in request.POST:
                return render(request, 'viewItem.html', {'post': post, 'form': SearchPost(), 'offer': OfferMoney(), 'item': request.GET['item']})
            else:
                return render(request, 'viewItem.html',
                                  {'post': post, 'form': SearchPost(), 'item': request.GET['item']})
        elif type(offer) == ItemOffer:
            if 'itemOffer' in request.POST:
                return render(request, 'viewItem.html', {'post': post, 'form': SearchPost(), 'offer': OfferItem(user=request.session['uid']), 'item': request.GET['item']})
            elif 'moneyOffer' in request.POST:
                return render(request, 'viewItem.html', {'post': post, 'form': SearchPost(), 'offer': OfferMoney(), 'item': request.GET['item']})
            else:
                return render(request, 'viewItem.html', {'post': post, 'form': SearchPost(), 'offer': OfferItem(user=request.session['uid'], instance=offer), 'item': request.GET['item']})
        elif type(offer) == MoneyOffer:
            if 'itemOffer' in request.POST:
                return render(request, 'viewItem.html', {'post': post, 'form': SearchPost(), 'offer': OfferItem(user=request.session['uid']), 'item': request.GET['item']})
            elif 'moneyOffer' in request.POST:
                return render(request, 'viewItem.html', {'post': post, 'form': SearchPost(), 'offer': OfferMoney(), 'item': request.GET['item']})
            else:
                return render(request, 'viewItem.html', {'post': post, 'form': SearchPost(), 'offer': OfferMoney(instance=offer), 'item': request.GET['item']})

    else:
        return HttpResponseRedirect('/')


def offer(request):
    if 'type' in request.POST and 'uid' in request.session and 'post' in request.POST:
        user = User.objects.get(id=request.session['uid'])
        post = Post.objects.get(id=request.POST['post'])

        try: # update offer
            offer = Offer.objects.get(offer_user=user, offer_post=post)

            if request.POST['type'] == 'OfferItem': # new offer is an item
                item = Post.objects.get(id=request.POST['item'])
                try: # update existing offer
                    itemOffer = ItemOffer.objects.get(itemO_offer=offer)
                    itemOffer.item = item
                    itemOffer.save()

                    message = Message(
                        message=" has updated his/her offered to <a href='/viewItem/?item=" + str(
                            item.id) + "'>" + item.post_name + "</a>for <a href='/viewItem/?item=" + str(
                            post.id) + "'>" + post.post_name + "</a>",
                        mFrom=user, mTo=post.post_owner)
                    message.save()
                except ItemOffer.DoesNotExist: # change from money to item offer
                    moneyOffer = MoneyOffer.objects.get(moneyO_offer=offer)
                    moneyOffer.delete()

                    itemOffer = ItemOffer(itemO_offer=offer, item=item)
                    itemOffer.save()

                    message = Message(
                        message=" has changed his/her offer to <a href='/viewItem/?item=" + str(
                            item.id) + "'>" + item.post_name + "</a>for <a href='/viewItem/?item=" + str(
                            post.id) + "'>" + post.post_name + "</a>",
                        mFrom=user, mTo=post.post_owner)
                    message.save()
            else: # new offer is money
                try: # update existing offer
                    moneyOffer = MoneyOffer.objects.get(moneyO_offer=offer)
                    moneyOffer.money = request.POST['money']
                    moneyOffer.save()

                    message = Message(
                        message=" has updated his/her offer to Php. " + str(moneyOffer.money) + " for <a href='/viewItem/?item=" + str(
                            post.id) + "'>" + post.post_name + "</a>",
                        mFrom=user, mTo=post.post_owner)
                    message.save()
                except MoneyOffer.DoesNotExist: # change from item to money
                    itemOffer = ItemOffer.objects.get(itemO_offer=offer)
                    itemOffer.delete()

                    moneyOffer = MoneyOffer(moneyO_offer=offer, money=request.POST['money'])
                    moneyOffer.save()
                    message = Message(
                        message=" has changed his/her offer to Php. " + str(moneyOffer.money) + " for <a href='/viewItem/?item=" + str(
                            post.id) + "'>" + post.post_name + "</a>",
                        mFrom=user, mTo=post.post_owner)
                    message.save()

        except Offer.DoesNotExist: # create offer
            offer = Offer(offer_user=user, offer_post=post)
            offer.save()

            if request.POST['type'] == 'OfferItem':
                item = Post.objects.get(id=request.POST['item'])
                itemOffer = ItemOffer(itemO_offer=offer, item=item)
                itemOffer.save()

                message = Message(
                    message=" has offered <a href='/viewItem/?item=" + str(item.id) + "'>" + item.post_name + "</a>for <a href='/viewItem/?item=" + str(
                        post.id) + "'>" + post.post_name + "</a>",
                    mFrom=user, mTo=post.post_owner)
                message.save()
            else:
                moneyOffer = MoneyOffer(moneyO_offer=offer, money=int(request.POST['money']))
                moneyOffer.save()
                message = Message(
                    message=" has offered Php. " + str(moneyOffer.money) + " for <a href='/viewItem/?item=" + str(
                        post.id) + "'>" + post.post_name + "</a>",
                    mFrom=user, mTo=post.post_owner)
                message.save()

        return HttpResponseRedirect('/viewItem/?item=' + str(request.POST['post']))
    else:
        return HttpResponseRedirect('/')


def messages(request):
    if 'uid' in request.session:
        messages = Message.objects.filter(mTo=request.session['uid'])
        messages = messages.order_by('-dateSent')

        if messages.count() == 0:
            messages = None

        return render(request, 'viewMessages.html', {'form': SearchPost(), 'messages': messages})
    else:
        return HttpResponseRedirect("/")


def cancel(request):
    if 'post' in request.POST and 'uid' in request.session:
        try:
            offer = Offer.objects.get(offer_post_id=request.POST['post'], offer_user_id=request.session['uid'])
            offer.delete()

            message = Message(message = " has canceled his/her offer for <a href='/viewItem/?item=" + str(offer.offer_post.id) +"'> " + offer.offer_post.post_name +  " </a>", mFrom=offer.offer_user, mTo=offer.offer_post.post_owner)
            message.save()
            return HttpResponseRedirect("/viewItem/?item=" + str(request.POST['post']))
        except Offer.DoesNotExist:
            return HttpResponseRedirect("/")
    else:
        return HttpResponseRedirect("/")


def accept(request):
    if 'uid' in request.session and 'offer' in request.GET and 'type' in request.GET:
        try:
            if request.GET['type'] == '0':
                item = 0
                try:
                    off = ItemOffer.objects.get(id=request.GET['offer'])
                    message = Message(message=" has accepted your offer for <a href='/viewItem/?item=" + str(
                        off.itemO_offer.offer_post.id) + "'> " + off.itemO_offer.offer_post.post_name + " </a>",
                                      mFrom=off.itemO_offer.offer_post.post_owner,
                                      mTo=off.itemO_offer.offer_user)
                    item = off.itemO_offer.offer_post.id
                except ItemOffer.DoesNotExist:
                    return HttpResponseRedirect('/')
            else:
                try:
                    off = MoneyOffer.objects.get(id=request.GET['offer'])
                    message = Message(message=" has accepted your offer for <a href='/viewItem/?item=" + str(
                        off.moneyO_offer.offer_post.id) + "'> " + off.moneyO_offer.offer_post.post_name + " </a>",
                                      mFrom=off.moneyO_offer.offer_post.post_owner,
                                      mTo=off.moneyO_offer.offer_user)
                    item = off.moneyO_offer.offer_post.id
                except MoneyOffer.DoesNotExist:
                    return HttpResponseRedirect('/')

            message.save()
            if request.GET['type'] == '0':
                off.itemO_offer.delete()
            else:
                off.moneyO_offer.delete()

            return HttpResponseRedirect('/viewItem/?item=' + str(item))
        except Offer.DoesNotExist:
            return HttpResponseRedirect('/')
    else:
        return HttpResponseRedirect('/')


def reject(request):
    if 'uid' in request.session and 'offer' in request.GET and 'type' in request.GET:
        try:
            if request.GET['type'] == '0':
                item = 0
                try:
                    off = ItemOffer.objects.get(id=request.GET['offer'])
                    message = Message(message=" has rejected your offer for <a href='/viewItem/?item=" + str(
                        off.itemO_offer.offer_post.id) + "'> " + off.itemO_offer.offer_post.post_name + " </a>",
                                      mFrom=off.itemO_offer.offer_post.post_owner,
                                      mTo=off.itemO_offer.offer_user)
                    item = off.itemO_offer.offer_post.id
                except ItemOffer.DoesNotExist:
                    return HttpResponseRedirect('/')
            else:
                try:
                    off = MoneyOffer.objects.get(id=request.GET['offer'])
                    message = Message(message=" has rejected your offer for <a href='/viewItem/?item=" + str(
                        off.moneyO_offer.offer_post.id) + "'> " + off.moneyO_offer.offer_post.post_name + " </a>",
                                      mFrom=off.moneyO_offer.offer_post.post_owner,
                                      mTo=off.moneyO_offer.offer_user)
                    item = off.moneyO_offer.offer_post.id
                except MoneyOffer.DoesNotExist:
                    return HttpResponseRedirect('/')

            message.save()
            if request.GET['type'] == '0':
                off.itemO_offer.delete()
            else:
                off.moneyO_offer.delete()

            return HttpResponseRedirect('/viewItem/?item=' + str(item))
        except Offer.DoesNotExist:
            return HttpResponseRedirect('/')
    else:
        return HttpResponseRedirect('/')