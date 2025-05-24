from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.auth.models import User
from django.views.generic import (
    ListView,
    DetailView,
    CreateView,
    UpdateView,
    DeleteView
)
from .models import Post, Subscription


def home(request):
    context = {
        'posts': Post.objects.all()
    }
    return render(request, 'blog/home.html', context)


class PostListView(ListView):
    model = Post
    template_name = 'blog/home.html' # <app>/<model>_<viewtype>.html
    context_object_name = 'posts'
    ordering = ['-date_posted']
    paginate_by = 5


class UserPostListView(ListView):
    model = Post
    template_name = 'blog/user_posts.html' # <app>/<model>_<viewtype>.html
    context_object_name = 'posts'
    ordering = ['-date_posted']
    paginate_by = 5

    def get_queryset(self):
        user = get_object_or_404(User, username=self.kwargs.get('username'))
        return Post.objects.filter(author=user).order_by('-date_posted')


class PostDetailView(DetailView):
    model = Post


class PostCreateView(LoginRequiredMixin, CreateView):
    model = Post
    fields = ['title', 'content']

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)
    

class PostUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Post
    fields = ['title', 'content']

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)
    
    def test_func(self):
        post = self.get_object()
        if self.request.user == post.author:
            return True
        return False
    

class PostDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Post
    success_url = '/'

    def test_func(self):
        post = self.get_object()
        if self.request.user == post.author:
            return True
        return False


def about(request):
    """Render the about page with detailed platform information, team data, and technical specifications."""
    about_data = {
        'meta': {
            'title': 'About Django Blog | Modern Blogging Platform',
            'description': 'Discover Django Blog - a feature-rich blogging platform built with Python/Django. Learn about our mission, technology stack, and development team.'
        },
        'hero': {
            'heading': 'Empowering Content Creators Worldwide',
            'subheading': 'A Modern Django-Powered Blogging Platform',
            'image_url': 'blog/images/about-hero.jpg',  # Update path as needed
            'cta_text': 'Start Blogging Today'
        },
        'platform': {
            'stats': [
                {'value': '10K+', 'label': 'Monthly Readers'},
                {'value': '95%', 'label': 'User Satisfaction'},
                {'value': '24/7', 'label': 'Uptime'},
                {'value': '100%', 'label': 'Open Source'}
            ],
            'features': [
                {
                    'title': 'Modern Architecture',
                    'description': 'Built with Django REST Framework and PostgreSQL',
                    'icon': 'fas fa-server'
                },
                {
                    'title': 'Responsive Design',
                    'description': 'Mobile-first approach with Bootstrap 5',
                    'icon': 'fas fa-mobile-alt'
                },
                {
                    'title': 'Secure Platform',
                    'description': 'HTTPS enforcement and XSS protection',
                    'icon': 'fas fa-shield-alt'
                },
                {
                    'title': 'SEO Optimized',
                    'description': 'Schema markup and meta tags management',
                    'icon': 'fas fa-search'
                }
            ]
        },
        'team': [
            {
                'name': 'Alex Chen',
                'role': 'Lead Developer',
                'bio': 'Full-stack developer with 8+ years experience in Django',
                'image': 'blog/team/alex.jpg',
                'social': {
                    'github': '#',
                    'linkedin': '#'
                }
            },
            {
                'name': 'Maria Gonzalez',
                'role': 'UX Designer',
                'bio': 'Specialist in user-centered design systems',
                'image': 'blog/team/maria.jpg',
                'social': {
                    'dribbble': '#',
                    'twitter': '#'
                }
            }
        ],
        'technology': {
            'stack': [
                {'name': 'Django 4.2', 'logo': 'blog/tech/django.png'},
                {'name': 'Python 3.11', 'logo': 'blog/tech/python.png'},
                {'name': 'Bootstrap 5', 'logo': 'blog/tech/bootstrap.png'},
                {'name': 'PostgreSQL', 'logo': 'blog/tech/postgresql.png'}
            ],
            'github_url': 'https://github.com/yourorg/djangoblog'
        }
    }
    return render(request, 'blog/about.html', {'about': about_data})



def subscribe(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        # Basic Validation
        if email and '@' in email:
            # Save to database
            Subscription.objects.get_or_create(email=email)
            messages.success(request, 'Thanks for subscribing!')
        else:
            messages.error(request, 'Please enter a valid email address.')
    return redirect('blog-home')