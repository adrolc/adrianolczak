from django.contrib.postgres.search import SearchQuery, SearchRank, SearchVector
from django.contrib.sites.shortcuts import get_current_site
from django.core.mail import send_mail
from django.db.models import Count
from django.shortcuts import get_object_or_404, render
from django.views.generic import DetailView, ListView, View

from .forms import EmailPostForm, SearchForm
from .models import Post


class PostListView(ListView):
    queryset = Post.published.all()
    context_object_name = "posts"
    paginate_by = 6
    template_name = "blog/pages/home.html"

    def get_queryset(self):
        self.list_name = "All posts"
        queryset = super().get_queryset()
        tag_slug = self.kwargs.get("tag_slug")
        query = self.request.GET.get("query")
        if tag_slug:
            queryset = queryset.filter(tags__slug=tag_slug)
            self.list_name = f"Results for tag: {tag_slug}"
        if query:
            form = SearchForm(self.request.GET)
            if form.is_valid():
                query = form.cleaned_data["query"]
                search_vector = SearchVector("title", weight="A") + SearchVector(
                    "body", weight="B"
                )
                search_query = SearchQuery(query)
                queryset = (
                    queryset.annotate(rank=SearchRank(search_vector, search_query))
                    .filter(rank__gte=0.1)
                    .order_by("-rank")
                )
                self.list_name = (
                    f"Results for '{query}' with tag: {tag_slug}"
                    if tag_slug
                    else f"Results for '{query}'"
                )
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["search_form"] = SearchForm()
        context["list_name"] = self.list_name
        return context


def post_detail(request, post_slug):
    post = get_object_or_404(Post, slug=post_slug, status=Post.Status.PUBLISHED)

    # List of similar posts
    # similar_posts = post.tags.similar_objects()[:3]
    post_tags_ids = post.tags.values_list("id", flat=True)
    similar_posts = Post.published.filter(tags__in=post_tags_ids).exclude(id=post.id)
    similar_posts = similar_posts.annotate(same_tags=Count("tags")).order_by(
        "-same_tags", "-publish"
    )[:3]

    context = {
        "post": post,
        "similar_posts": similar_posts,
        "domain": get_current_site(request).domain,
    }
    return render(request, "blog/pages/post_detail.html", context)
