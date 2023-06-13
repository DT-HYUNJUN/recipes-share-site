from django.conf import settings
from django.db import models
from django.contrib.auth.models import AbstractUser
from imagekit.models import ProcessedImageField
from imagekit.processors import ResizeToFill
from recipes.models import Ingredient, Recipe
from PIL import Image


class UserIngredient(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    ingredient = models.ForeignKey(Ingredient, on_delete=models.CASCADE)

    def __str__(self):
        return self.user.nickname + self.ingredient.name


class User(AbstractUser):
    email = models.EmailField("이메일", blank=False)
    nickname = models.CharField("닉네임", max_length=8, blank=False, null=True)
    followers = models.ManyToManyField(
        "self", related_name="followings", symmetrical=False
    )
    profile_image = ProcessedImageField(
        upload_to="profile/",
        processors=[ResizeToFill(300, 300)],
        format="JPEG",
        options={"quality": 80},
        null=True,
        blank=True,
    )
    fridge = models.ManyToManyField(
        Ingredient, through="UserIngredient", related_name="fridge_users", blank=True
    )
    birthdate = models.DateField("생년월일", null=True, blank=True)
    viewed_recipes = models.ManyToManyField(
        Recipe, related_name="viewed_users", blank=True
    )

    def fix_image_rotation(image_path):
        image = Image.open(image_path)
        # 이미지 회전을 위한 Exif 정보를 확인하고 회전시킴
        if hasattr(image, "_getexif") and image._getexif() is not None:
            exif = dict(image._getexif().items())
            orientation = exif.get(0x0112)
            if orientation == 3:
                image = image.rotate(180, expand=True)
            elif orientation == 6:
                image = image.rotate(270, expand=True)
            elif orientation == 8:
                image = image.rotate(90, expand=True)
        # 회전된 이미지를 저장하거나 처리에 사용할 수 있음
        image.save(image_path)
