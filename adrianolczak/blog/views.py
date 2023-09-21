from django.contrib.postgres.search import SearchQuery, SearchRank, SearchVector
from django.contrib.sites.shortcuts import get_current_site
from django.db.models import Count
from django.views.generic import ListView
from django.views.generic.detail import DetailView

from .forms import SearchForm
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


class PostDetailView(DetailView):
    model = Post
    template_name = "blog/pages/post_detail.html"
    queryset = Post.published.all()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        # Get the post tags
        post_tags_ids = self.object.tags.values_list("id", flat=True)
        # Get posts with the same tags
        similar_posts = Post.published.filter(tags__in=post_tags_ids).exclude(
            id=self.object.id
        )
        # Sort and select the top three
        similar_posts = similar_posts.annotate(same_tags=Count("tags")).order_by(
            "-same_tags", "-publish"
        )[:3]

        context["similar_posts"] = similar_posts
        context["domain"] = get_current_site(self.request).domain

        return context
