from collections import Counter

from django.contrib import messages
from django.contrib.auth.models import User
from django.core.paginator import Paginator
from django.db.models import Q
from django.http import HttpResponse
from django.shortcuts import render, redirect

# for current date, year, day
from datetime import date

from blog.models import Article, Blog_visitor, Article_Hindi

current_date = date.today()




def common():
    popular = Article.objects.filter(have_image="yes").order_by('-views')[:4]
    recent = Article.objects.filter(have_image="yes").order_by('-timestamp')[:4]

    stories = Article_Hindi.objects.filter(category_english="Stories").order_by('-timestamp')[:3]
    analysis = Article.objects.filter(category="Analysis").order_by('-timestamp')[:3]


    filter_all_by_category = Article.objects.values_list('category', flat=True)
    total_category = dict(Counter(filter_all_by_category))

    return [popular, recent, total_category, [stories, analysis]]

def error(request):
    return render(request, 'homepage/error.html')

def get_ip(request):
    address = request.META.get('HTTP_X_FORWARDED_FOR')
    if address:
        ip = address.split(',')[-1].strip()
    else:
        ip = request.META.get('REMOTE_ADDR')
    return ip



def homepage(request):
    filter_all_by_category = Article.objects.values_list('category', flat=True)
    total_category = dict(Counter(filter_all_by_category))

    india = Article.objects.filter(category='India')
    technology = Article.objects.filter(category='Technology')
    lifestyle = Article.objects.filter(category='Lifestyle')
    education = Article.objects.filter(category='Education')
    analysis = Article.objects.filter(category='Analysis')


    articles_by_time = Article.objects.all().order_by('timestamp')[:5]
    paginator = Paginator(articles_by_time, 1)
    page = request.GET.get('page')
    # ?page=2
    posts_contents = paginator.get_page(page)

    carousal_post = Article.objects.filter(have_image="yes").order_by('-views')[:8]


    params = {
        'carousal_post': carousal_post,
        'total_category': total_category,
        'india': india,
        'lifestyle': lifestyle,
        'education': education,
        'technology': technology,
        'analysis': analysis,

        'all_articles_by_time': posts_contents,
        'common': common,

    }

    return render(request, 'blog/english/homepage-e.html', params)


def articles_by_category(request, category=None):

    by_category = Article.objects.filter(category=category)
    paginator = Paginator(by_category, 7)
    page = request.GET.get('page')
    # ?page=2
    posts_content_by_category = paginator.get_page(page)

    filter_all_by_category = Article.objects.values_list('category', flat=True)
    total_category = dict(Counter(filter_all_by_category))
    recent_post = Article.objects.all().order_by('-timestamp')[:13]

    filter_all_by_category = Article.objects.values_list('category', flat=True)
    total_category = dict(Counter(filter_all_by_category))

    post_by_category = []
    for x in total_category:
        by_cat = Article.objects.filter(category=x)
        post_by_category.append(by_cat)

    params = {
        'post_by_category': post_by_category,
        'content_by_category': posts_content_by_category,
        'this_category': category,
        'total_category': total_category,
        'recent_post': recent_post,
        'common': common,
    }
    return render(request, 'blog/english/article-by-category.html', params)

def get_single_article(request, category=None, slug=None):

    temp_get_id = Article.objects.get(slug=slug)
    real_by_id = Article.objects.get(id=temp_get_id.id)

    views_ip = get_ip(request)

    ip_user = Blog_visitor(user=views_ip, article_name=real_by_id)

    result =Blog_visitor.objects.filter(Q(user__icontains=ip_user), article_name=real_by_id)

    total_views = Blog_visitor.objects.filter(article_name=real_by_id).count()
    if len(result) == 1:
        print("IP Address already exists")
    elif len(result) > 1:
        print("User exist")
    else:
        real_by_id.views = total_views+1
        ip_user.save()

    total_views = Blog_visitor.objects.filter(article_name=real_by_id).count()

    if category == '' or slug== '':
        return HttpResponse("No category")

    single_article = Article.objects.get(slug=slug)

    params = {
        'single_article': single_article,
        'views': total_views,
        'common': common,
    }

    return render(request, 'blog/english/single-article.html', params)

def new_article(request):
    if request.method == 'POST':
        title = request.POST['title']
        content = request.POST['content']
        tags = request.POST['tags']
        category = request.POST['category']
        toc = request.POST['toc']

        user = User.objects.get(username=request.user.username)

        if len(request.FILES):
            post_image = request.FILES['post_image']
            new_article = Article(
                title=title, have_image='yes', category=category, tags=tags, content=content, post_image=post_image,
                year=current_date.year, month=current_date.month, day=current_date.day, table_of_content=toc,
                user=user)
            new_article.save()
        else:
            new_article = Article(title=title, have_image='no', category=category, tags=tags, content=content,
                                  year=current_date.year, month=current_date.month, day=current_date.day,
                                  username=request.user.username)
            new_article.save()

        messages.success(request, "Your article was successfully posted and sent to your newsletters.")

    params = {}

    return redirect('homepage', params)
