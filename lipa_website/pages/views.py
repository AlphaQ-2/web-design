from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.utils import timezone
from .models import Article, Comment
from .forms import ArticleForm, CommentForm

from django.views.generic import (TemplateView, ListView,
                                  DetailView, CreateView,
                                  UpdateView, DeleteView)

from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin
from . import forms

# Create your views here.


class HomePage(TemplateView):
    template_name = 'index.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['page_title'] = 'Home'
        return context


class ThanksPage(TemplateView):
    template_name = 'thanks.html'


class LoggedInPage(TemplateView):
    template_name = 'loggedin.html'


class SignUp(CreateView):
    form_class = forms.UserCreateForm
    success_url = reverse_lazy('login')
    template_name = 'signup.html'


class AboutView(TemplateView):
    template_name = 'pages/about.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['page_title'] = 'About'
        return context


class ArticleListView(ListView):
    model = Article

    def get_queryset(self):
        return Article.objects.filter(published_date__lte=timezone.now()) \
                .order_by('-published_date')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['page_title'] = 'Articles'
        return context


class ArticleDetailView(DetailView):
    model = Article

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        article = get_object_or_404(Article, slug=self.kwargs['slug'])
        context['page_title'] = article.title
        return context


class CreateArticleView(LoginRequiredMixin, CreateView):
    login_url = '/login/'
    redirect_field_name = 'pages/article_detail.html'

    form_class = ArticleForm

    model = Article

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['page_title'] = 'Create Article'
        return context


class ArticleUpdateView(LoginRequiredMixin, UpdateView):
    login_url = '/login/'
    redirect_field_name = 'pages/article_detail.html'

    form_class = ArticleForm

    model = Article

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        article = get_object_or_404(Article, slug=self.kwargs['slug'])
        context['page_title'] = f'Update {article.title}'
        return context


class ArticleDeleteView(LoginRequiredMixin, DeleteView):
    model = Article
    success_url = reverse_lazy('article_list')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        article = get_object_or_404(Article, slug=self.kwargs['slug'])
        context['page_title'] = f'Delete {article.title}'
        return context


class DraftListView(LoginRequiredMixin, ListView):
    login_url = '/login/'
    redirect_field_name = 'pages/article_draft_list.html'

    model = Article

    def get_queryset(self):
        return Article.objects.filter(published_date__isnull=True) \
                .order_by('created_date')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['page_title'] = 'Draft Article'
        return context


#######################################
# Functions that require a slug match ###
#######################################

@login_required
def article_publish(request, slug):
    article = get_object_or_404(Article, slug=slug)
    article.publish()
    return redirect('article_detail', slug=slug)


@login_required
def add_comment_to_article(request, slug):
    article = get_object_or_404(Article, slug=slug)
    if request.method == "POST":
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.article = article
            comment.author = request.user
            comment.save()
            return redirect('article_detail', slug=article.slug)
    else:
        form = CommentForm()
    return render(request, 'pages/comment_form.html', {'form': form})


@login_required
def comment_approve(request, slug):
    comment = get_object_or_404(Comment, slug=slug)
    comment.approve()
    return redirect('article_detail', slug=comment.article.slug)


@login_required
def comment_remove(request, slug):
    comment = get_object_or_404(Comment, slug=slug)
    article_slug = comment.article.slug
    comment.delete()
    return redirect('article_detail', slug=article_slug)
