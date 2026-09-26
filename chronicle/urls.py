from django.urls import path
from . import views

app_name = 'chronicle'
urlpatterns = [
    path('detail/<slug:slug>',views.PostDetailView.as_view(),name='detail'),
    path('list',views.PostListView.as_view(),name='list'),
    path('category/<int:pk>',views.CategoryDetailView.as_view(),name='category'),
    path('search/',views.SearchPostView.as_view(),name='search'),
    path('contact/',views.ContactView.as_view(),name='contact'),
    path('about',views.about,name='about'),
    path('like/<slug:slug>/<int:pk>',views.like,name='like'),







]
