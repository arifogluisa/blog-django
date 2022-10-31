from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.http import HttpResponseRedirect
from django.urls import reverse_lazy
from django.views import generic
from django.views.generic import DetailView, CreateView, UpdateView
from django.views.generic.edit import FormView
from django.shortcuts import reverse
from django.contrib.messages.views import SuccessMessageMixin
from django.utils.translation import gettext_lazy as _

from .forms import CommentForm, ContactForm
from .models import Blog, Category, IpModel, Comment, AboutPageModel, ContactPageData


def get_client_ip(request):
    if x_forwarded_for := request.META.get('HTTP_X_FORWARDED_FOR'):
        return x_forwarded_for.split(',')[0]
    return request.META.get('REMOTE_ADDR')


class BaseIndexView(generic.TemplateView):
    """
    Home Page View
    """

    template_name = "index.html"

    def get_context_data(self, **kwargs):
        context = super(BaseIndexView, self).get_context_data(**kwargs)
        context['blogs'] = Blog.objects.all().order_by('-created_at')[1:]
        context['last_blog'] = Blog.objects.last()
        return context


class BlogDetailView(DetailView):
    model = Blog
    template_name = 'blog/blog_detail.html'
    context_object_name = 'blog'

    def get_context_data(self, **kwargs):
        context = super(BlogDetailView, self).get_context_data(**kwargs)
        ip = get_client_ip(self.request)
        like_status = False
        if ip_model := IpModel.objects.filter(ip=ip).first():
            like_status = bool(self.object.likes.filter(id=ip_model.id).first())
        context['like_status'] = like_status
        context['like_count'] = self.object.likes.count()
        context['comment_form'] = CommentForm()
        context['comments'] = Comment.objects.filter(
            blog__slug=self.kwargs.get('slug')
        ).order_by('-created_at')
        return context

    def post(self, request, *args, **kwargs):
        view = CommentAddView.as_view()
        return view(request, *args, **kwargs)


class CommentAddView(LoginRequiredMixin, CreateView):
    model = Comment
    form_class = CommentForm
    template_name = 'blog/blog_detail.html'

    def form_valid(self, form):
        form.instance.commenter = self.request.user
        form.instance.blog = Blog.objects.get(slug=self.kwargs.get('slug'))
        return super().form_valid(form)

    def get_success_url(self):
        return reverse('blog-detail', kwargs={'slug': self.kwargs.get('slug')})


class BlogCreateView(LoginRequiredMixin, CreateView):
    model = Blog
    template_name = 'blog/blog_create.html'
    fields = ['title', 'body', 'image']

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)


class BlogUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Blog
    template_name = 'blog/blog_create.html'
    fields = ['title', 'body', 'image']

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)

    def test_func(self):
        blog = self.get_object()
        return self.request.user == blog.author


class BlogCategoryView(DetailView):
    model = Category
    template_name = 'blog/blogs_by_category.html'
    context_object_name = 'blog_category'

    def get_context_data(self, **kwargs):
        context = super(BlogCategoryView, self).get_context_data(**kwargs)
        context['blogs'] = Blog.objects.filter(category=self.object)
        return context


class MyBlogsView(LoginRequiredMixin, generic.ListView):
    model = Blog
    template_name = 'blog/my_blogs.html'

    def get_context_data(self, **kwargs):
        context = super(MyBlogsView, self).get_context_data(**kwargs)
        context['blogs'] = Blog.objects.filter(author=self.request.user)
        return context


class AboutView(generic.TemplateView):
    """
    About Page View
    """

    template_name = "about.html"

    def get_context_data(self, **kwargs):
        context = super(AboutView, self).get_context_data(**kwargs)
        context["object"] = AboutPageModel.objects.last()
        return context


class ContactView(SuccessMessageMixin, FormView):
    template_name = 'contact.html'
    form_class = ContactForm
    success_url = reverse_lazy('contact')
    success_message = _('Mesajınız uğurla göndərildi, tezliklə sizinlə əlaqə saxlanılacaq')

    def form_valid(self, form):
        form.save()
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super(ContactView, self).get_context_data(**kwargs)
        context["object"] = ContactPageData.objects.last()
        return context


class SearchView(generic.ListView):
    template_name = "blog/search.html"
    model = Blog
    queryset = Blog.objects.all()

    def get_queryset(self):
        queryset = super(SearchView, self).get_queryset()
        if "search" in self.request.GET and self.request.GET["search"]:
            if search := self.request.GET["search"]:
                queryset = queryset.filter(title__icontains=search)
        return queryset


def post_like(request, pk):
    blog_id = request.POST.get('blog-id')
    post = Blog.objects.get(pk=blog_id)
    ip = get_client_ip(request)
    if not IpModel.objects.filter(ip=ip).exists():
        IpModel.objects.create(ip=ip)
    if post.likes.filter(id=IpModel.objects.get(ip=ip).id).exists():
        post.likes.remove(IpModel.objects.get(ip=ip))
    else:
        post.likes.add(IpModel.objects.get(ip=ip))
    return HttpResponseRedirect(reverse('blog-detail', args=[post.slug]))


class ManifestView(generic.TemplateView):
    template_name = "manifest/manifest.json"


class PushwooshServiceWorkerView(generic.TemplateView):
    template_name = "manifest/pushwoosh-service-worker.js"
