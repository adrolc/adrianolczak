from django.shortcuts import render, get_object_or_404
from .models import Post
from django.views.generic import ListView, View
from .forms import EmailPostForm, CommentForm, SearchForm
from django.core.mail import send_mail
from django.core.cache import cache
from django.db.models import Count
from django.contrib.postgres.search import SearchVector, SearchQuery, SearchRank
from datetime import date

# === Post list ===
class PostListView(ListView):
    queryset = Post.published.all()
    context_object_name = 'posts'
    paginate_by = 6
    template_name = 'blog/pages/home.html'

    def get_queryset(self):
        self.list_name = 'Wszystkie posty'
        queryset = super().get_queryset()
        tag_slug = self.kwargs.get('tag_slug')
        query = self.request.GET.get('query')
        if tag_slug:
            queryset = queryset.filter(tags__slug=tag_slug)
            self.list_name = f"Wyniki dla tagu: {tag_slug}"
        if query:
            form = SearchForm(self.request.GET)
            if form.is_valid():
                query = form.cleaned_data['query']
                search_vector = SearchVector('title', weight='A') + SearchVector('body', weight='B')
                search_query = SearchQuery(query)
                queryset = queryset.annotate(rank=SearchRank(search_vector, search_query)).filter(rank__gte=0.1).order_by('-rank')
                self.list_name = f"Wyniki dla '{query}' z tagiem: {tag_slug}" if tag_slug else f"Wyniki dla '{query}'"
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['search_form'] = SearchForm()
        context['list_name'] = self.list_name
        return context

# === Post detail ===
def _can_comment_within_hour(request, limit=5):
    """Check if user can comment.
    Limit means the maximum number of comments per hour
    """
    if not request.user.is_authenticated:
        return False
    
    key = f'comments:{request.user.id}'
    count = cache.get_or_set(key, 0, 3600)
    if count >= limit:
        return False
    
    return True

def _comment_incr(key):
    cache.incr(key)

def post_detail(request, year, month, day, post_slug):
    post = get_object_or_404(Post,
    slug=post_slug,
    status=Post.Status.PUBLISHED,
    publish__date=date(year, month, day)
    )

    comments = post.comments.filter(active=True)
    can_comment = _can_comment_within_hour(request)
    comment_form = None
        
    if can_comment:
        if request.method == 'POST':
            comment_form = CommentForm(data=request.POST)
            if comment_form.is_valid():
                new_comment = comment_form.save(commit=False)
                new_comment.post = post
                new_comment.user = request.user
                new_comment.save()
                _comment_incr(f'comments:{request.user.id}')
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
        'share_form': share_form,
        'share_form_sent': share_form_sent,
    }
    return render(request, 'blog/pages/post_detail.html', context)
