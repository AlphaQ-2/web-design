from django import forms
from .models import Article, Comment
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import get_user_model


class UserCreateForm(UserCreationForm):

    class Meta:
        fields = ('username', 'email', 'password1', 'password2')
        model = get_user_model()

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['username'].label = 'Display Name'
        # Setting the label of the Username Field in the Form
        self.fields['email'].label = 'Email Address'


class ArticleForm(forms.ModelForm):

    class Meta:
        model = Article
        fields = ('title', 'body_text',)

        widgets = {
            'title': forms.TextInput(attrs={'class': 'textinputclass'}),
            'body_text': forms.Textarea(attrs={'class': 'editable medium-editor-textarea articlecontent'}),
        }


class CommentForm(forms.ModelForm):

    class Meta:
        model = Comment
        fields = ('body_text',)

        widgets = {
            'body_text': forms.Textarea(attrs={'class': 'editable medium-editor-textarea'}),
        }
