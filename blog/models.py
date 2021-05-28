from django.db import models

from django.contrib.auth.models import User

from ckeditor.fields import RichTextField
# Create your models here.

class Author(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, null=True, blank=True)
    profile_pic = models.ImageField(null=True, blank=True, default='image/placeholder.png')

    def __str__(self):
        return self.user.username

class Category(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name

class Post(models.Model):
    author = models.ForeignKey(User, null=True, blank=True, on_delete=models.CASCADE)
    title = models.CharField(max_length=150)
    body = RichTextField(null=True, blank=True)
    image = models.ImageField(null=True, blank=True)
    category = models.ManyToManyField(Category)
    date_created = models.DateTimeField(auto_now_add=True, null=True)
    slang = models.CharField(null=True, blank=True, max_length=200)

    def __str__(self):
        return self.title

class Comment(models.Model):
    author = models.ForeignKey(User, null=True, blank=True, on_delete=models.CASCADE)
    post = models.ForeignKey(Post, null=True, blank=True, on_delete=models.CASCADE)
    comment_text = models.CharField(max_length=200)
    like = models.IntegerField(default=0, null=True, blank=True)

    def __str__(self):
        return self.comment_text

    def total_likes(self):
        likes = self.likes_set.all()
        total_likes = likes.count()
        return total_likes

class Likes(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    comment = models.ForeignKey(Comment, on_delete=models.CASCADE)
    like = models.BooleanField(default=False)


