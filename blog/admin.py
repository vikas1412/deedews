from django.contrib import admin
from blog.models import Article, Post_Comment, Blog_visitor, Article_Hindi

admin.site.register((Post_Comment, Article, Blog_visitor, Article_Hindi))