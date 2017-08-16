from django import forms
from .models import User, Post, Offer, ItemOffer, MoneyOffer, Message

post_choices = (('all', 'All Types'), ('academic', 'Academic Type'), ('office', 'Office Type'))
post_limit_choices = ((10, '10'), (15, '15'), (20, '20'))

class UserLogin(forms.ModelForm):
    class Meta:
        model = User
        fields = ['user_email', 'user_password']
        
        widgets = {
            'user_email': forms.EmailInput(attrs={'required': True, 'placeholder': 'Account Email'}),
            'user_password': forms.PasswordInput(attrs={'required': True, 'placeholder': 'Account Password'}),
        }

        labels = {
            'user_email': 'Email Address',
            'user_password': 'Password',
        }

class UserRegister(forms.ModelForm):
    class Meta:
        model = User
        fields = ['user_name', 'user_type', 'user_email', 'user_password', 'user_pic']

        widgets = {
            'user_name': forms.TextInput(attrs={'required': True, 'placeholder': 'Full Name...'}),
            'user_email': forms.EmailInput(attrs={'required': True, 'placeholder': 'Account Email...'}),
            'user_password': forms.PasswordInput(attrs={'required': True, 'placeholder': 'Account Password...'}),
        }

        labels = {
            'user_name': 'Full Name',
            'user_type': 'Account Type',
            'user_pic': 'Profile Picture',
            'user_email': 'Email Address',
            'user_password': 'Password',
        }

class PostItem(forms.ModelForm):
    class Meta:
        model = Post
        fields = ['post_name', 'post_description', 'post_price', 'post_type', 'post_course', 'post_tags', 'post_pic']
        help_texts = {
            'post_tags': '',
        }

        widgets = {
            'post_name': forms.TextInput(attrs={'required': True, 'placeholder': 'Item Name'}),
            'post_description': forms.TextInput(attrs={'required': True, 'placeholder': 'Item Description...'}),
            'post_price': forms.NumberInput(attrs={'required': True, 'placeholder': 'Item Price...'}),
            'post_tags': forms.Textarea(attrs={'required': True, 'placeholder': 'Item Tags (separated by commas)...'}),
            'post_pic': forms.ClearableFileInput(attrs={'required': False}),
            'post_course': forms.TextInput(attrs={'required': True, 'placeholder': 'Type N/A if for office use'}),
        }

        labels = {
            'post_name': 'Post Title',
            'post_description': 'Item Description',
            'post_price': 'Item Price (Php.)',
            'post_type': 'Item Type',
            'post_tags': 'Item Tags',
            'post_pic': 'Item Picture',
        }

class SearchPost(forms.ModelForm):
    post_type = forms.CharField(required=True, label="Post Type", widget=forms.Select(choices=post_choices))
    limit = forms.CharField(label="Posts Limit", widget=forms.Select(choices=post_limit_choices, attrs={'required': True}))

    post_tags = forms.CharField(required=False, label='Tag Search', widget=forms.TextInput(attrs={'required': False, 'placeholder': 'Item Tags (separated by space)...'}))
    user = forms.CharField()

    class Meta:
        model = Post
        fields = ['post_tags']

        help_texts ={
            'post_tags': '',
        }
        labels = {
            'post_tags': 'Tag Search'
        }

    def __init__(self, userId=None, *args, **kwargs):
        super(SearchPost, self).__init__(*args, **kwargs)

        if userId is None:
            del self.fields['user']
        else:
            self.fields['user'] = forms.CharField(widget=forms.HiddenInput(attrs={'value': userId}))

class OfferMoney(forms.ModelForm):
    class Meta:
        model = MoneyOffer

        fields = ['money']

        widgets = {
            'money': forms.NumberInput(attrs={'required': True})
        }

        labels = {
            'money': 'Money Offer'
        }

class OfferItem(forms.ModelForm):
    class Meta:
        model = ItemOffer

        fields = ['item']

        labels = {
            'item': 'Item Offer',
        }

    def __init__(self, user, *args, **kwargs):
        super(OfferItem, self).__init__(*args, **kwargs)
        self.fields['item'] = forms.ModelChoiceField(queryset=Post.objects.filter(post_owner_id=user), required=True)
        self.fields['item'].label_from_instance = lambda obj: "%s" % obj.post_name

class SendMessage(forms.ModelForm):
    class Meta:
        model = Message

        fields = ['message']