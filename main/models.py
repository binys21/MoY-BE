from django.db import models
from accounts.models import User
from django.utils import timezone
from django.core.validators import MaxValueValidator, MinValueValidator


# Create your models here.
class Black(models.Model):
    CATEGORY_CHOICES = [
    ('영화','영화'),
    ('음악','음악'),
    ('책','책'),
    ('유튜브','유튜브'),
    ('OTT','OTT'),
    ('공연','공연')
    ]

    FRAME_CHOICES = [
        ('TREE','TREE'),
        ('SNOW','SNOW'),
        ('HAT','HAT'),
        ('YEAR','YEAR'),
        ('MAN','MAN'),
        ('STAR','STAR'),
    ]
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    category = models.CharField(choices=CATEGORY_CHOICES, max_length=5)
    name = models.TextField()
    description = models.TextField(blank=True, null=True)
    information = models.TextField()
    img = models.TextField()
    color = models.PositiveIntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(24)])
    frame = models.CharField(choices=FRAME_CHOICES, max_length=5)

class White(models.Model):
    CATEGORY_CHOICES = [
    ('여행지','여행지'),
    ('음식','음식'),
    ('밈','밈'),
    ('사진','사진'),
    ('아이템','아이템'),
    ('룩','룩'),
    ('어플','어플'),
    ('스포츠','스포츠'),
    ]

    FRAME_CHOICES = [
        ('TREE','TREE'),
        ('SNOW','SNOW'),
        ('HAT','HAT'),
        ('YEAR','YEAR'),
        ('MAN','MAN'),
        ('STAR','STAR'),
    ]
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    category = models.CharField(choices=CATEGORY_CHOICES, max_length=5)
    name = models.TextField()
    description = models.TextField(blank=True, null=True)
    img = models.TextField()
    color = models.PositiveIntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(24)])
    frame = models.CharField(choices=FRAME_CHOICES, max_length=5)
