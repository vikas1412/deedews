from collections import Counter

from django.contrib import messages
from django.contrib.auth.models import User
from django.core.paginator import Paginator
from django.db.models import Q
from django.http import HttpResponse
from django.shortcuts import render, redirect

# for current date, year, day
from datetime import date

from blog.models import Blog_visitor, Article_Hindi, Blog_visitor_hindi_blog

current_date = date.today()




def common():
    popular = Article_Hindi.objects.filter(have_image="yes").order_by('-views')[:4]
    recent = Article_Hindi.objects.filter(have_image="yes").order_by('-timestamp')[:4]

    filter_all_by_category = Article_Hindi.objects.values_list('category', flat=True)
    total_category = dict(Counter(filter_all_by_category))

    return [popular, recent, total_category]


def get_ip(request):
    address = request.META.get('HTTP_X_FORWARDED_FOR')
    if address:
        ip = address.split(',')[-1].strip()
    else:
        ip = request.META.get('REMOTE_ADDR')
    return ip

def homepage_hindi(request):
    filter_all_by_category = Article_Hindi.objects.values_list('category', flat=True)
    total_category = dict(Counter(filter_all_by_category))

    stories = Article_Hindi.objects.filter(category='स्टोरीज')[:5]

    analysis = Article_Hindi.objects.filter(category='एनालिसिस')

    lifestyle = Article_Hindi.objects.filter(category='लाइफस्टाइल')
    other = Article_Hindi.objects.filter(category='अन्य')


    articles_by_time = Article_Hindi.objects.all().order_by('timestamp')[:]
    paginator = Paginator(articles_by_time, 1)
    page = request.GET.get('page')
    # ?page=2
    posts_contents = paginator.get_page(page)

    carousal_post = Article_Hindi.objects.filter(have_image="yes").order_by('-views')[:8]


    params = {
        'carousal_post': carousal_post,
        'total_category': total_category,
        'stories': stories,
        'analysis': analysis,
        'lifestyle': lifestyle,
        'other': other,

        'all_articles_by_time': posts_contents,
        'common': common,
    }

    return render(request, 'blog/hindi/homepage-h.html', params)




def articles_by_category_h(request, category=None):
    category = category.capitalize()
    english_category = ''
    if category == 'स्टोरीज':
        english_category = 'Stories'
    if category == 'एनालिसिस':
        english_category = 'Analysis'
    if category == 'लाइफस्टाइल':
        english_category = 'Lifestyle'
    if category == 'अन्य':
        english_category = 'Other'
    by_category = Article_Hindi.objects.filter(category_english=english_category)

    paginator = Paginator(by_category, 7)
    page = request.GET.get('page')
    # ?page=2
    posts_content_by_category = paginator.get_page(page)

    recent_post = Article_Hindi.objects.all().order_by('-timestamp')[:13]

    filter_all_by_category = Article_Hindi.objects.values_list('category', flat=True)
    total_category = dict(Counter(filter_all_by_category))


    post_by_category = []
    for x in total_category:
        by_cat = Article_Hindi.objects.filter(category=x)
        post_by_category.append(by_cat)

    params = {
        'post_by_category': post_by_category,
        'content_by_category': posts_content_by_category,
        'this_category': category,
        'total_category': total_category,
        'recent_post': recent_post,
        'common': common,
    }
    return render(request, 'blog/hindi/article-by-category-h.html', params)

def get_single_article_h(request, category=None, slug=None):

    temp_get_id = Article_Hindi.objects.get(slug=slug)
    real_by_id = Article_Hindi.objects.get(id=temp_get_id.id)

    views_ip = get_ip(request)

    ip_user = Blog_visitor_hindi_blog(user=views_ip, article_name=real_by_id)

    result =Blog_visitor_hindi_blog.objects.filter(Q(user__icontains=ip_user), article_name=real_by_id)

    total_views = Blog_visitor_hindi_blog.objects.filter(article_name=real_by_id).count()
    if len(result) == 1:
        print("IP Address already exists")
    elif len(result) > 1:
        print("User exist")
    else:
        real_by_id.views = total_views+1
        ip_user.save()

    total_views = Blog_visitor_hindi_blog.objects.filter(article_name=real_by_id).count()

    single_article = Article_Hindi.objects.get(slug=slug)

    params = {
        'single_article': single_article,
        'views': total_views,
        'common': common,
    }

    return render(request, 'blog/hindi/single-article-h.html', params)

def new_article_h(request):
    if request.user.is_staff:
        if request.method == 'POST':
            title_hindi = request.POST['title_hindi']
            title = request.POST['title_english']
            content = request.POST['content']
            tags = request.POST['tags']
            category = request.POST['category']

            category_english = ''
            if category == 'स्टोरीज':
                category_english = 'Stories'
            elif category == 'एनालिसिस':
                category_english = 'Analysis'
            elif category == 'लाइफस्टाइल':
                category_english = 'Lifestyle'
            elif category == 'अन्य':
                category_english = 'Other'

            toc = request.POST['toc']

            user = User.objects.get(username=request.user.username)

            if len(request.FILES):
                post_image = request.FILES['post_image']
                new_article = Article_Hindi(
                    title=title, title_hindi=title_hindi, have_image='yes', category_english=category_english, category=category, tags=tags, content=content, post_image=post_image,
                    year=current_date.year, month=current_date.month, day=current_date.day, table_of_content=toc,
                    user=user)
                new_article.save()
            else:
                new_article = Article_Hindi(title=title, title_hindi=title_hindi, have_image='no', category_english=category_english, category=category, tags=tags, content=content,
                                      year=current_date.year, month=current_date.month, day=current_date.day,
                                      username=request.user.username)
                new_article.save()

            messages.success(request, "आपके आर्टिकल को पोस्ट कर दिया गया है और आपके नूस्लेटर्स को भी भेज दिए गया है !")

            return redirect('homepage-h')
    else:
        return redirect('error')