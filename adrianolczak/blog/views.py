from django.contrib.postgres.search import SearchQuery, SearchRank, SearchVector
from django.contrib.sites.shortcuts import get_current_site
from django.db.models import Count
from django.views.generic import ListView
from django.views.generic.detail import DetailView

from .forms import SearchForm
from .models import Post


class PostListView(ListView):
    context_object_name = "posts"
    paginate_by = 6
    template_name = "blog/pages/home.html"
    list_name = "All posts"

    def filter_by_tag(self, queryset, tag_slug):
        """
        Filter the queryset based on the given tag_slug
        """
        queryset = queryset.filter(tags__slug=tag_slug)
        return queryset, f"Results for tag: {tag_slug}"

    def filter_by_query(self, queryset, query):
        """
        Filter the queryset based on the given search query
        """
        form = SearchForm({"query": query})
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
            return queryset, f"Results for '{query}'"
        return queryset, "Incorrect query"

    def get_queryset(self):
        queryset = Post.published.all()
        tag_slug = self.kwargs.get("slug")
        query = self.request.GET.get("query")

        if tag_slug:
            queryset, self.list_name = self.filter_by_tag(queryset, tag_slug)

        if query:
            queryset, self.list_name = self.filter_by_query(queryset, query)

        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["list_name"] = self.list_name
        return context


class PostDetailView(DetailView):
    model = Post
    template_name = "blog/pages/post_detail.html"
    queryset = Post.published.all()

    def get_similar_posts(self):
        """
        Retrieves posts that have the same tags as the current post object. The posts are
        sorted by the number of matching tags and their publish date.
        """
        # Get the current post tags
        post_tags_ids = self.object.tags.values_list("id", flat=True)
        # Get posts with the same tags
        similar_posts = Post.published.filter(tags__in=post_tags_ids).exclude(
            id=self.object.id
        )
        # Sort and choose top 2
        similar_posts = similar_posts.annotate(same_tags=Count("tags")).order_by(
            "-same_tags", "-publish"
        )[:2]

        return similar_posts

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["similar_posts"] = self.get_similar_posts()
        context["domain"] = get_current_site(self.request).domain

        return context
