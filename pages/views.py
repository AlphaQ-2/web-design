from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.utils import timezone
from .models import Article, Comment, Category, Job, Message, ArticleImage, \
                    Service
from .forms import ArticleForm, CommentForm, JobForm, MessageForm, \
                   ServiceForm, MessageForm2

from django.views.generic import (TemplateView, ListView,
                                  DetailView, CreateView,
                                  UpdateView, DeleteView,
                                  RedirectView)

from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin
from . import forms
from django.urls import reverse
from django.db import IntegrityError
from django.contrib import messages
from django.db.models import Q

# Create your views here.


class HomePage(TemplateView):
    template_name = 'index.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        form = MessageForm2()
        context['form'] = form
        context['page_title'] = 'Home'
        return context

    def post(self, request, *args, **kwargs):
        form = MessageForm2(request.POST)
        try:
            if form.is_valid():
                data = form.cleaned_data
                Message.objects.create(name=data['name'],
                                       email=data['email'],
                                       subject=data['subject'],
                                       body_text=data['body_text'])

        except IntegrityError:
            messages.warning(self.request, (
                            "Warning, can't send message right now."
                            ))

        else:
            messages.success(self.request, "Comment posted")

        return super().get(request, *args, **kwargs)


class ThanksPage(TemplateView):
    template_name = 'thanks.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['page_title'] = 'Thank you'
        return context


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
        context['page_title'] = 'Who We Are'
        return context


class ArticleListView(ListView):
    model = Article

    def get_queryset(self):
        category = self.request.GET.get('category')
        search = self.request.GET.get('search')
        articles = Article.objects.filter(published_date__lte=timezone.now()) \
            .order_by('-published_date')

        if category:
            articles = articles.filter(category__title=category)

        if search:
            articles = articles.filter(
                Q(title__icontains=search) | Q(body_text__icontains=search)
                | Q(category__title__icontains=search)
            )

        return articles

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        categories = Category.objects.all()[:10]
        jobs = Job.objects.filter(
                Q(created_date__lte=timezone.now()) & Q(is_open=True)
                ).order_by('-created_date')[:10]
        context['jobs'] = jobs
        context['categories'] = categories
        context['page_title'] = 'Articles'
        return context


class ArticleDetailView(DetailView):
    model = Article

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        article = get_object_or_404(Article, slug=self.kwargs['slug'])
        article_images = ArticleImage.objects.filter(
            article=article
        )
        categories = Category.objects.all()[:10]
        jobs = Job.objects.filter(
                Q(created_date__lte=timezone.now()) & Q(is_open=True)
                ).order_by('-created_date')[:10]
        context['article_images'] = article_images
        context['jobs'] = jobs
        context['categories'] = categories
        context['page_title'] = article.title
        context['form'] = CommentForm()
        return context

    def post(self, request, *args, **kwargs):
        article = get_object_or_404(Article, slug=self.kwargs.get("slug"))
        form = CommentForm(request.POST)
        try:
            if form.is_valid():
                text = form.cleaned_data['body_text']
                Comment.objects.create(author=request.user,
                                       article=article,
                                       body_text=text)  # fix

        except IntegrityError:
            messages.warning(self.request, (
                            "Warning, can't comment on {}".format(article.title)
                            ))

        else:
            messages.success(self.request, "Comment posted")

        return super().get(request, *args, **kwargs)


class CreateArticleView(LoginRequiredMixin, CreateView):
    login_url = '/login/'
    redirect_field_name = 'pages/article_detail.html'

    form_class = ArticleForm

    model = Article

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['page_title'] = 'Create Article'
        return context

    def form_valid(self, form, request):
        self.object = form.save(commit=False)
        self.object.author = request.user
        self.object.save()
        return super().form_valid(form)

    def post(self, request, *args, **kwargs):
        form = self.get_form()
        if form.is_valid():
            return self.form_valid(form, request)
        else:
            return self.form_invalid(form)


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


class CreateJobView(LoginRequiredMixin, CreateView):
    login_url = '/login/'
    redirect_field_name = 'pages/article_list.html'

    form_class = JobForm

    model = Job

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['page_title'] = 'Create Job'
        return context


class CreateMessageView(CreateView):
    redirect_field_name = 'pages/contact.html'

    form_class = MessageForm

    model = Message

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['page_title'] = 'Send a message'
        return context


class CreateServiceView(LoginRequiredMixin, CreateView):
    login_url = '/login/'
    redirect_field_name = 'pages/service_list.html'

    form_class = ServiceForm

    model = Service

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['page_title'] = 'Create a Service'
        return context


class ServicesListView(ListView):
    model = Service

    def get_queryset(self):
        return Service.objects.all().order_by('name')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['page_title'] = 'What We Do'
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
