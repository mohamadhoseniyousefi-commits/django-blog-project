from django.contrib import admin
from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse
from django.utils.html import format_html
from django.utils.text import slugify


class Meta:
    ordering = ['-created_at']


class Category(models.Model):
    name = models.CharField(max_length=60, verbose_name='نام دسته بندی')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.name}"

    class Meta:
        verbose_name = 'دسته بندی'
        verbose_name_plural = 'دسته بندی ها'


class Post(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='posts', verbose_name='نویسنده')
    category = models.ManyToManyField(Category, related_name='posts', verbose_name='نام دسته بندی')
    title = models.CharField(max_length=60, verbose_name='عنوان')
    body = models.TextField(verbose_name='متن')
    image = models.ImageField(upload_to='images/post',null=True,blank=True, verbose_name='عکس')
    status = models.BooleanField(default=True, verbose_name='وضعیت')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    slug = models.SlugField(blank=True, null=True, unique=True)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        super().save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse('chronicle:detail', kwargs={'slug': self.slug})

    def __str__(self):
        return f"{self.title} - {self.body[:30]}"

    @admin.display(description='عکس مقاله')
    def get_image(self):
        if self.image:
            return format_html(
                '<img src="{}" width="50px" height="50px">',
                self.image.url
            )
        return 'تصویر ندارد'



    class Meta:
        verbose_name = 'مقاله'
        verbose_name_plural = 'مقاله ها'


class Comment(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='comments', verbose_name='مقاله')
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='comments', verbose_name='کاربر')

    parent = models.ForeignKey('self', on_delete=models.CASCADE, null=True, blank=True, related_name='replies',
                               verbose_name='پاسخ به کامنت')

    body = models.TextField(verbose_name='متن')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.post.title} - {self.body[:30]}"

    class Meta:
        verbose_name = 'کامنت'
        verbose_name_plural = 'کامنت ها'


class Messages(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True, verbose_name='کاربر')
    title = models.CharField(max_length=60, verbose_name='عنوان پیام')
    text = models.TextField(verbose_name='متن پیام')
    email = models.EmailField(verbose_name='ایمیل')
    created_at = models.DateTimeField(auto_now_add=True, null=True)

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'پیام'
        verbose_name_plural = 'پیام ها'


class Likes(models.Model):
    user = models.ForeignKey(User, models.CASCADE, related_name='like', verbose_name='کاربر')
    post = models.ForeignKey(Post, models.CASCADE, related_name='like', verbose_name='مقاله')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} - {self.post.title}"

    class Meta:
        verbose_name = 'لایک'
        verbose_name_plural = 'لایک ها'
