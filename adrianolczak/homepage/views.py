from django.shortcuts import render
from blog.models import Post

# Create your views here.
def homepage(request):
    latest_posts = Post.published.all()[:3]
    context = {
        'latest_posts': latest_posts,
    }
    return render(request, 'homepage/index.html', context)