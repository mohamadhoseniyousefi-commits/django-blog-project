from django.contrib import messages
from django.shortcuts import render,redirect
from django.urls import reverse_lazy
from chronicle.models import Post, Category, Comment, Messages, Likes
from .forms import Message_form
from django.views.generic import ListView, DetailView, FormView
from .mixin import CustomLoginMixin


def like(request, slug, pk):
    try:
        like = Likes.objects.get(post__slug=slug, user_id=request.user.id)
        like.delete()
    except:
        Likes.objects.create(post_id=pk, user_id=request.user.id)

    return redirect('chronicle:detail', slug)

# ___________________________________________________________________________________________________________
class PostDetailView(DetailView):
    model = Post
    template_name = 'chronicle/chronicle_detail.html'
    context_object_name = 'post'

    def post(self, request, *args, **kwargs):
        post = self.get_object()

        if not request.user.is_authenticated:
            return redirect('account:login')

        parent_id = request.POST.get('parent_id')
        body = request.POST.get('body')

        Comment.objects.create(user=request.user,post=post,body=body,parent_id=parent_id)

        return redirect(post.get_absolute_url())


    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        context['is_like'] = self.request.user.like.filter(
            post__slug=self.object.slug,
            user_id=self.request.user.id
        ).exists()

        return context

# __________________________________________________________________________________________________________

class PostListView(CustomLoginMixin,ListView):
    model = Post
    template_name = 'chronicle/chronicle_list.html'
    paginate_by = 2


# __________________________________________________________________________________________________________


class CategoryDetailView(ListView):
    model = Post
    template_name = 'chronicle/chronicle_list.html'



    def get_queryset(self):
        return Post.objects.filter(category=self.kwargs['pk'])


# __________________________________________________________________________________________________________

class SearchPostView(ListView):
    model = Post
    template_name = 'chronicle/chronicle_search.html'
    context_object_name = 'post'
    paginate_by = 2

    def get_queryset(self):
        search = self.request.GET.get('search')
        return Post.objects.filter(title__icontains=search)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['search'] = self.request.GET.get('search')
        return context



# __________________________________________________________________________________________________________


class ContactView(FormView):
    template_name = 'chronicle/chronicle_contactus.html'
    form_class = Message_form
    success_url = reverse_lazy('chronicle:contact')

    def form_valid(self, form):
        form_data=form.cleaned_data
        Messages.objects.create(**form_data)
        messages.success(self.request,"Your message has been sent successfully!")
        return super().form_valid(form)


# __________________________________________________________________________________________________________

def about(request):
    return render(request, 'chronicle/about.html')


















