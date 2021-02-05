from django.urls import path, include
from . import views, views_hindi

urlpatterns = [
    # path('fitness-tips/', views.blog_single_page, name="single-blog"),

    path('blog/<str:category>/<str:slug>/', views.get_single_article, name="single-article"),

    path('blog/new-publication/', views.new_article, name="new-article"),

    path('', views.homepage, name="homepage"),

    path('blog/<str:category>/', views.articles_by_category, name="article-by-category"),

    path('pageNotFound-404/', views.error, name='error'),

    # HINDI ARTICLES
    path('blog-h/', views_hindi.homepage_hindi, name="homepage-h"),
    path('blog-h/new-publication/', views_hindi.new_article_h, name="new-article-in-hindi"),
    path('blog-h/<str:category>/', views_hindi.articles_by_category_h, name="hindi-article-by-category"),
    path('blog-h/<str:category>/<str:slug>/', views_hindi.get_single_article_h, name="single-article-hindi"),
]
