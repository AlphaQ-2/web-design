from django import forms
from .models import Article, Comment, Job
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
        fields = ('title', 'body_text', 'category', 'hero_image')

        widgets = {
            'title': forms.TextInput(attrs={'class': 'textinputclass container-fluid form-control'}),
            'body_text': forms.Textarea(attrs={'class': 'editable medium-editor-textarea articlecontent'}),
            'category': forms.Select(attrs={'class': 'form-control'}),
        }


class CommentForm(forms.ModelForm):

    class Meta:
        model = Comment
        fields = ('body_text',)

        widgets = {
            'body_text': forms.Textarea(attrs={
                            'class': 'form-control',
                            'rows': 3}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["body_text"].label = ''


class JobForm(forms.ModelForm):

    class Meta:
        model = Job
        fields = ('title', 'company', 'link', 'is_open',)

        widgets = {
            'title': forms.TextInput(attrs={'class': 'textinputclass container-fluid form-control'}),
            'company': forms.TextInput(attrs={'class': 'textinputclass container-fluid form-control'}),
            'link': forms.TextInput(attrs={'class': 'textinputclass container-fluid form-control'}),
        }
