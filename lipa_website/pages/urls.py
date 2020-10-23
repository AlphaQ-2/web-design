from django.urls import path
from . import views

# app_name = 'pages'

urlpatterns = [
    path('', views.ArticleListView.as_view(), name='article_list'),
    path('about/', views.AboutView.as_view(), name='about'),
    path('article/<slug>', views.ArticleDetailView.as_view(),
         name='article_detail'),
    path('article/new/', views.CreateArticleView.as_view(),
         name='article_new'),
    path('article/<slug>/edit/', views.ArticleUpdateView.as_view(),
         name='article_edit'),
    path('drafts/', views.DraftListView.as_view(), name='article_draft_list'),
    path('article/<slug>/remove/', views.ArticleDeleteView.as_view(),
         name='article_remove'),
    path('article/<slug>/publish/', views.article_publish,
         name='article_publish'),
    path('article/<slug>/comment/', views.add_comment_to_article,
         name='add_comment_to_article'),
    path('comment/<slug>/approve/', views.comment_approve,
         name='comment_approve'),
    path('comment/<slug>/remove/', views.comment_remove,
         name='comment_remove'),
]
