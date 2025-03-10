from django import template
from blog.models import Post

register = template.Library()

@register.inclusion_tag('blog/sidebar_latest_posts.html')
def latest_posts_sidebar(count=5):
    """
    Retrieves the latest posts for display in the sidebar.
    By Default, it returns 5 posts. You can override the number by passing a count.
    """
    latest_posts = Post.objects.all().order_by('-date_posted')[:count]
    return {'latest_posts': latest_posts}