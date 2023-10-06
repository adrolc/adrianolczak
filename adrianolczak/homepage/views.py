from blog.models import Post
from django.shortcuts import render


# Create your views here.
def homepage(request):
    latest_posts = Post.published.all()[:3]
    context = {
        "latest_posts": latest_posts,
    }
    return render(request, "homepage/index.html", context)
