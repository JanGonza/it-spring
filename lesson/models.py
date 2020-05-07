from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
from django.urls import reverse

from django.conf import settings
# Create your models here.


class TheoryManager(models.Manager):
    def get_queryset(self):
        return super(TheoryManager, self).get_queryset().filter(material_type='theory')


class Material(models.Model):
    MATERIAL_TYPE = (
        ('theory', 'Theoretical material'),
        ('practice', 'Practical')
    )
    title = models.CharField(max_length=250)
    slug = models.SlugField(max_length=250,
                            unique_for_date='publish')
    body = models.TextField()
    publish = models.DateTimeField(default=timezone.now)

    updated = models.DateTimeField(auto_now=True)
    created = models.DateTimeField(auto_now_add=True)
    author = models.ForeignKey(User,
                               on_delete=models.CASCADE,
                               related_name='user_materials')
    material_type = models.CharField(max_length=20,
                                     choices=MATERIAL_TYPE,
                                     default='theory')
    objects = models.Manager()
    theory = TheoryManager()

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('lesson:material_details',
                       args=[self.publish.year,
                             self.publish.month,
                             self.publish.day,
                             self.slug])


class Comment(models.Model):
    material = models.ForeignKey(Material,
                                 on_delete=models.CASCADE,
                                 related_name='comments')
    name = models.CharField(max_length=79)
    body = models.TextField()
    created = models.DateTimeField(auto_now_add=True)
    email = models.EmailField()


class Profile(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    birth = models.DateTimeField(blank=True, null=True)
    photo = models.ImageField(upload_to="user/%Y/%m/%d/", blank=True)

    def __str__(self):
        return "{username} profile.".format(username=self.user.username)


class Lesson(models.Model):
    title = models.CharField(max_length=200)
    slug = models.SlugField(max_length=200,
                            unique=True)
    materials = models.ManyToManyField(Material,
                                       related_name='lessons')
    notes = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('lesson:lesson_details',
                       args=[self.slug])
