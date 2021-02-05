from django.db import models


class Contact_User(models.Model):
    name = models.CharField(max_length=213)
    email = models.CharField(max_length=213)
    subject = models.CharField(max_length=213)
    matter = models.CharField(max_length=513)
    timestamp = models.DateTimeField(auto_now_add=True, blank=True)

    def __str__(self):
        return self.email


class Newsletter(models.Model):
    timestamp = models.DateTimeField(auto_now_add=True, blank=True, null=True)
    email = models.CharField(max_length=213, null=True, default="", blank=True)
    name = models.CharField(max_length=213, null=True, default="", blank=True)
    sno = models.AutoField(primary_key=True)

    def __str__(self):
        return self.email


class IP_visitors(models.Model):
    user = models.TextField(default=None)
    # for_post = models.TextField(default='', null=True, blank=True)
    # for_post = models.ForeignKey(News, on_delete=models.CASCADE)
    timestamp = models.DateTimeField(auto_now_add=True, blank=True)

    def __str__(self):
        return self.user
