from django.contrib.auth.models import User
from django.db import models

class Profile(models.Model):
    user=models.OneToOneField(User,on_delete=models.CASCADE)
    name_father=models.CharField(max_length=20)
    meliname=models.CharField(max_length=10)
    image=models.ImageField(upload_to='profile/images',blank=True,null=True)

    def __str__(self):
        return self.user.username

    class Meta:
        verbose_name="حساب کاربری"
        verbose_name_plural='حساب های کاربری'