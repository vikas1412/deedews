from PIL import Image
from ckeditor_uploader.fields import RichTextUploadingField
from ckeditor.fields import RichTextField
from django.contrib.auth.models import User
from django.db import models
from django.db.models.signals import pre_save
from django.urls import reverse

from deedews.utils import unique_slug_generator

def user_directory_path(instance, filename):
    # file will be uploaded to MEDIA_ROOT/user_<id>/<filename>
    return 'posts-media/posted_by_{0}_at_{1}/{2}'.format(instance.username, instance.timestamp, filename)


def english_post_image_path(instance, filename):
    # file will be uploaded to MEDIA_ROOT/user_<id>/<filename>
    return 'Post/English-posts/{0}/{1}/{2}'.format(instance.category, instance.title, filename)


def hindi_post_image_path(instance, filename):
    # file will be uploaded to MEDIA_ROOT/user_<id>/<filename>
    return 'Post/Hindi-posts/{0}/{1}/{2}'.format(instance.category_english, instance.slug, filename)


class Article_Hindi(models.Model):
    category = [
        ('स्टोरीज', 'स्टोरीज'),
        ('एनालिसिस', 'एनालिसिस'),
        ('लाइफस्टाइल', 'लाइफस्टाइल'),
        ('अन्य', 'अन्य'),
    ]

    category_english = [
        ('Stories', 'Stories'),
        ('Analysis', 'Analysis'),
        ('Lifestyle', 'Lifestyle'),
        ('Other', 'Other'),
    ]

    have_image = [
        ('yes', 'Yes'),
        ('no', 'No'),
        ('not_sure', 'Not Sure')
    ]
    title_hindi = models.CharField(default='', blank=True, null=True, max_length=500, help_text="Title for article")
    title = models.CharField(default='', blank=True, null=True, max_length=500, help_text="Title in English for article")
    category = models.CharField(max_length=95, default='अन्य', choices=category, blank=True, help_text="Category for article")
    category_english = models.CharField(max_length=95, default='अन्य', choices=category_english, blank=True, help_text="Category for article")
    post_image = models.ImageField(upload_to=hindi_post_image_path, blank=True, null=True)
    slug = models.SlugField(max_length=200, null=True, blank=True, help_text="Slug will be generated automatically from the title of the post")
    content = models.TextField(default="", null=True, blank=True)
    have_image = models.CharField(max_length=95, default='not_sure', choices=have_image, blank=True, help_text="Does this article have image or not?")
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    # username = models.CharField(max_length=129, default='Anonymous', blank=True, help_text="Article written by")
    views = models.IntegerField(blank=False, null=False, default=0)
    tags = models.CharField(default='', blank=True, null=True, max_length=300, help_text="One word tags")
    # content = RichTextField(blank=True, null=True, max_length=10000)
    table_of_content = RichTextUploadingField(default="", null=True, blank=True)
    timestamp = models.DateTimeField(auto_now_add=True, blank=True, null=True)
    year = models.IntegerField(default="0000", help_text="Year of article published")
    month = models.IntegerField(default="00", help_text="Month of article published")
    day = models.IntegerField(default="00", help_text="Day of article published")

    def __str__(self):
        return self.title[:20] + ' --- ' + str(self.category_english)

    def get_absolute_url(self):
        return reverse('articles-home', args=[str(self.title)])

    def save(self):
        super().save()
        try:
            size_for_thumb = (800, 800)
            reduced_image = Image.open(self.post_image.path)
            reduced_image.thumbnail(size_for_thumb)
            reduced_image.save(self.post_image.path)
        except:
            pass


def hindi_slug_generator(sender, instance, *args, **kwargs):
    if not instance.slug:
        instance.slug = unique_slug_generator(instance)
pre_save.connect(hindi_slug_generator, sender=Article_Hindi)




class Article(models.Model):
    category = [
        ('India', 'India'),
        ('Technology', 'Technology'),
        ('Lifestyle', 'Lifestyle'),
        ('Education', 'Education'),
        ('Analysis', 'Analysis'),
    ]

    have_image = [
        ('yes', 'Yes'),
        ('no', 'No'),
        ('not_sure', 'Not Sure')
    ]
    title = models.CharField(default='', blank=True, null=True, max_length=500, help_text="Title for article")
    have_image = models.CharField(max_length=95, default='not_sure', choices=have_image, blank=True, help_text="Does this article have image or not?")
    post_image = models.ImageField(upload_to=english_post_image_path, blank=True, null=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    # username = models.CharField(max_length=129, default='Anonymous', blank=True, help_text="Article written by")
    views = models.IntegerField(blank=False, null=False, default=0)
    category = models.CharField(max_length=95, default='Un-categorised', choices=category, blank=True, help_text="Category for article")
    tags = models.CharField(default='', blank=True, null=True, max_length=300, help_text="One word tags")
    # content = RichTextField(blank=True, null=True, max_length=10000)
    slug = models.SlugField(max_length=200, null=True, blank=True, help_text="Slug will be generated automatically from the title of the post")
    content = RichTextUploadingField(default="", null=True, blank=True)
    table_of_content = RichTextUploadingField(default="", null=True, blank=True)
    timestamp = models.DateTimeField(auto_now_add=True, blank=True, null=True)
    year = models.IntegerField(default="0000", help_text="Year of article published")
    month = models.IntegerField(default="00", help_text="Month of article published")
    day = models.IntegerField(default="00", help_text="Day of article published")

    def __str__(self):
        return self.title[:20] + str(self.timestamp)

    def get_absolute_url(self):
        return reverse('articles-home', args=[str(self.title)])

    def save(self):
        super().save()
        try:
            size_for_thumb = (800, 800)
            reduced_image = Image.open(self.post_image.path)
            reduced_image.thumbnail(size_for_thumb)
            reduced_image.save(self.post_image.path)
        except:
            pass


def slug_generator_for_article(sender, instance, *args, **kwargs):
    if not instance.slug:
        instance.slug = unique_slug_generator(instance)
pre_save.connect(slug_generator_for_article, sender=Article)


class Blog_visitor_hindi_blog(models.Model):
    user = models.TextField(default=None)
    article_name = models.ForeignKey(Article_Hindi, on_delete=models.CASCADE)

    def __str__(self):
        return self.user

class Blog_visitor(models.Model):
    user = models.TextField(default=None)
    article_name = models.ForeignKey(Article, on_delete=models.CASCADE)

    def __str__(self):
        return self.user


class Post_Comment(models.Model):
    sno = models.AutoField(primary_key=True)
    comment = models.CharField(max_length=400, null=True, blank=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    post = models.ForeignKey(Article, on_delete=models.CASCADE)
    parent = models.ForeignKey('self', on_delete=models.CASCADE, null=True)
    timestamp = models.DateTimeField(auto_now_add=True, blank=True)

    def __str__(self):
        return self.user.username.upper() + " commented '" + self.comment[:30] + "'...."
