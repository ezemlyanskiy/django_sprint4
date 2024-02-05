from .models import Post


def get_base_posts_query():
    return (
        Post.objects
        .select_related('category', 'location', 'author')
        .prefetch_related('author')
    )
