from django.shortcuts import render, get_object_or_404
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from .models import Post, Comment
from django.views.generic import ListView, View
from .forms import EmailPostForm, CommentForm
from django.core.mail import send_mail
from django.core.cache import cache
from django.db.models import Count

class PostListView(ListView):
    queryset = Post.published.all()
    context_object_name = 'posts'
    paginate_by = 6
    template_name = 'blog/pages/home.html'

    def get_queryset(self):
        queryset = super().get_queryset()
        tag_slug = self.kwargs.get('tag_slug')
        if tag_slug:
            queryset = queryset.filter(tags__slug=tag_slug)
        return queryset

def _can_comment(request, limit=5):
    "Comment limit per hour"
    user_ip = request.META['REMOTE_ADDR']
    comment_count = cache.get(user_ip, 0) + 1
    if comment_count <= limit:
        cache.set(user_ip, comment_count, 3600)
        return True
    return False

def post_detail(request, year, month, day, post_slug):
    post = get_object_or_404(Post,
    slug=post_slug,
    status=Post.Status.PUBLISHED,
    publish__year=year,
    publish__month=month,
    publish__day=day)

    comments = post.comments.filter(active=True)
    can_comment = _can_comment(request)
    comment_form = None
    if request.method == 'POST' and request.user.is_authenticated:
        if can_comment:
            comment_form = CommentForm(data=request.POST)
            if comment_form.is_valid():
                new_comment = comment_form.save(commit=False)
                new_comment.post = post
                new_comment.user = request.user
                new_comment.save()
                comment_form = CommentForm()

    if can_comment:
            comment_form = CommentForm()

    # Share post via email
    share_form = EmailPostForm()
    share_form_sent = 'false'
    if request.method == 'POST':
        share_form = EmailPostForm(request.POST)
        if share_form.is_valid():
            cd = share_form.cleaned_data
            post_url = request.build_absolute_uri(post.get_absolute_url())
            subject = f"{cd['name']} recommends you read " \
                    f"{post.title}"
            message = f"Read {post.title} at {post_url}\n\n" \
                    f"{cd['name']}\'s comments: {cd['comments']}"
            send_mail(subject, message, 'your_account@gmail.com', [cd['to']])
            share_form_sent ='true'

    # List of similar posts
    # similar_posts = post.tags.similar_objects()[:3]
    post_tags_ids = post.tags.values_list('id', flat=True)
    similar_posts = Post.published.filter(tags__in=post_tags_ids).exclude(id=post.id)
    similar_posts = similar_posts.annotate(same_tags=Count('tags')).order_by('-same_tags','-publish')[:3]

    context = {
        'post': post,
        'similar_posts': similar_posts,
        'comments': comments,
        'comment_form': comment_form,
        'can_comment': can_comment,
        'share_form': share_form,
        'share_form_sent': share_form_sent,
    }
    return render(request, 'blog/pages/post_detail.html', context)
