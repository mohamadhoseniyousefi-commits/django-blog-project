from django.shortcuts import render,redirect,HttpResponse
from django.views.generic.base import View

import chronicle
from chronicle.models import Post
from django.urls import reverse

def home(request):
    posts=Post.objects.all()
    
    return render(request,'home/index.html',context={'posts':posts})










   
