
#from .models import Post
from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import Tweet


class SignUpForm(UserCreationForm):
    first_name = forms.CharField(max_length=30, required=False,widget=forms.TextInput(attrs={'class':'form-control'}))
    last_name = forms.CharField(max_length=30, required=False,widget=forms.TextInput(attrs={'class':'form-control'}))
    email = forms.EmailField(max_length=254,required=True,widget=forms.TextInput(attrs={'class':'form-control'}))

    def __init__(self, *args, **kwargs):
        super(SignUpForm, self).__init__(*args, **kwargs)
        for fieldname in ['username', 'password1', 'password2']:
            self.fields[fieldname].help_text = None
            self.fields[fieldname].widget.attrs.update({'class': 'form-control'})

    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name', 'email', 'password1', 'password2', )


class twitter(forms.ModelForm):

    class Meta:
        model=Tweet
        fields=('text',)


class UserFollower(forms.Form):
    username = forms.CharField(max_length=30)
    method = forms.CharField(max_length=30)