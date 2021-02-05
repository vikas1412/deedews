from django.db import models
from PIL import Image
from ckeditor.fields import RichTextField



def user_directory_path(instance, filename):
    # file will be uploaded to MEDIA_ROOT/user_<id>/<filename>
    return 'profile-picture/user_{0}_{1}/{2}'.format(instance.username, instance.timestamp, filename)


class Profile(models.Model):
    GENDER_CF = [
        ('Male', 'Male'),
        ('Female', 'Female'),
        ('Custom', 'Custom')
    ]

    timestamp = models.DateField(auto_now_add=True, blank=True)
    fullname = models.CharField(max_length=213)

    username = models.CharField(max_length=60)
    profile_photo = models.ImageField(upload_to=user_directory_path,  default='profile/default.png')

    dob = models.CharField(max_length=213, blank=True,  null=True)

    # dob = models.DateTimeField(blank=True, null=True)
    # user = models.OneToOneField(User, on_delete=models.CASCADE, blank=True)
    gender = models.CharField(max_length=15, null=True, choices=GENDER_CF, blank=True)
    number = models.CharField(max_length=213, default="", blank=True, null=True)
    bio = models.TextField(max_length=513, blank=True, default="", null=True)

    def __str__(self):
        return str(self.fullname) + ' as ' + str(self.username)

    def save(self):
        super().save()
        size_for_thumb = (300, 300)
        pic_for_thumb = Image.open(self.profile_photo.path)
        pic_for_thumb.thumbnail(size_for_thumb)
        pic_for_thumb.save(self.profile_photo.path)


