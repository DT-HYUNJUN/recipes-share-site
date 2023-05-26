from django.db import models
from django.contrib.auth.models import AbstractUser
from imagekit.models import ProcessedImageField
from imagekit.processors import ResizeToFill
from recipes.models import Ingredient
# Create your models here.


class User(AbstractUser):
    nickname = models.CharField(max_length=8, blank=True, null=False)
    followers = models.ManyToManyField('self', related_name='followings', symmetrical=False)
    profile_image = ProcessedImageField(upload_to='profile/', processors=[ResizeToFill(300, 300)], format='JPEG', options={'quality': 80}, null=True, blank=True)
    fridge = models.ManyToManyField(Ingredient, related_name='fridge_users', blank=True)