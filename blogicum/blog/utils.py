from .models import Post


def get_base_posts_query():
    return (
        Post.objects.select_related(
            'author',
            'location',
            'category'
        )
        .prefetch_related('comments')
        .only(
            'title',
            'text',
            'pub_date',
            'author',
            'location',
            'category',
            'image',
            'is_published',
            'category__is_published',
            'category__slug',
            'category__title',
            'location__is_published',
            'location__name',
            'author__username',
        )
    )
