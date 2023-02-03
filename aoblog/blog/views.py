from django.shortcuts import render, get_object_or_404
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from .models import Post, Comment
from django.views.generic import ListView, View
from .forms import EmailPostForm, CommentForm
from django.core.mail import send_mail
from django.core.cache import cache

class PostListView(ListView):
    """
    Alternative post list view
    """
    queryset = Post.published.all()
    context_object_name = 'posts'
    paginate_by = 6
    template_name = 'blog/pages/home.html'

def post_detail(request, year, month, day, post_slug):
    post = get_object_or_404(Post,
    slug=post_slug,
    status=Post.Status.PUBLISHED,
    publish__year=year,
    publish__month=month,
    publish__day=day)

    comments = post.comments.filter(active=True)
    cannot_comment = False
    comment_form = None
    if request.method == 'POST' and request.user.is_authenticated:
        user_ip = request.META['REMOTE_ADDR']
        comment_count = cache.get(user_ip, 0) + 1
        if comment_count <= 5:
            cache.set(user_ip, comment_count, 3600)
            comment_form = CommentForm(data=request.POST)
            if comment_form.is_valid():
                new_comment = comment_form.save(commit=False)
                new_comment.post = post
                new_comment.user = request.user
                new_comment.save()
        else:
            cannot_comment = True
    else:
        comment_form = CommentForm()

    context = {
        'post': post,
        'comments': comments,
        'comment_form': comment_form,
        'cannot_comment': cannot_comment,
    }
    return render(request, 'blog/pages/post_detail.html', context)

class PostShareView(View):
    def get(self, request, post_id):
        post = get_object_or_404(Post, id=post_id, status=Post.Status.PUBLISHED)
        form = EmailPostForm()
        return render(request, 'blog/pages/post_share.html', {'post': post, 'form': form})
    
    def post(self, request, post_id):
            post = get_object_or_404(Post, id=post_id, status=Post.Status.PUBLISHED)
            form = EmailPostForm(request.POST)
            sent = False
            if form.is_valid():
                cd = form.cleaned_data
                post_url = request.build_absolute_uri(post.get_absolute_url())
                subject = f"{cd['name']} recommends you read " \
                        f"{post.title}"
                message = f"Read {post.title} at {post_url}\n\n" \
                        f"{cd['name']}\'s comments: {cd['comments']}"
                send_mail(subject, message, 'your_account@gmail.com', [cd['to']])
                sent = True

            return render(request, 'blog/pages/post_share.html', {'post': post, 'form': form, 'sent': sent})
