from django.db import models
from django.urls import reverse
from django.utils.translation import gettext_lazy as _
from django.utils.text import slugify
from .abstract_models import AbstractBaseModel
from ckeditor.fields import RichTextField


class IpModel(models.Model):
    ip = models.CharField(max_length=100)

    def __str__(self):
        return self.ip


class Blog(AbstractBaseModel):
    author = models.ForeignKey('account.Account', on_delete=models.CASCADE)
    title = models.CharField(
        _('title'),
        max_length=255,
    )
    body = RichTextField(
        verbose_name=_('Body')
    )
    image = models.ImageField(
        _('image'),
        upload_to='blogs/images',
    )
    category = models.ManyToManyField(
        'core.Category',
        verbose_name=_('category'),
        related_name='blogs',
        null=True,
        blank=True,
    )
    slug = models.SlugField(
        _('Slug'),
        max_length=255,
        unique=True,
        blank=True
    )
    likes = models.ManyToManyField(
        IpModel,
        related_name="blog_likes",
        blank=True,
    )

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('blog-detail', kwargs={'slug': self.slug})

    class Meta:
        verbose_name = _('Blog')
        verbose_name_plural = _('Blogs')

    def save(self, *args, **kwargs):
        if not self.id:
            self.slug = slugify(self.title)
        super(Blog, self).save(*args, **kwargs)

    def total_likes(self):
        return self.likes.count()


class Category(AbstractBaseModel):
    title = models.CharField(
        _('title'),
        max_length=255,
        db_index=True,
    )
    ordering = models.PositiveIntegerField(
        _('ordering'),
        default=1,
    )
    slug = models.SlugField(
        _('Slug'),
        max_length=255,
        unique=True,
        blank=True
    )

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        if not self.id:
            self.slug = slugify(self.title)
        super(Category, self).save(*args, **kwargs)

    class Meta:
        verbose_name = _('Category')
        verbose_name_plural = _('Categories')
        ordering = ('ordering',)


class Comment(AbstractBaseModel):
    text = models.TextField(
        _('text'),
    )
    commenter = models.ForeignKey(
        'account.Account',
        verbose_name=_('commenter'),
        related_name='comments',
        on_delete=models.CASCADE
    )
    blog = models.ForeignKey(
        Blog,
        on_delete=models.CASCADE,
        null=True,
    )

    def __str__(self):
        return self.text[:15]

    class Meta:
        verbose_name = _('Comment')
        verbose_name_plural = _('Comments')


class AboutPageModel(models.Model):
    title = models.CharField(
        _('title'),
        max_length=255,
    )
    image = models.FileField(
        _('image'),
        upload_to='about/images',
        null=True,
        blank=True,
    )
    description = RichTextField()

    def __str__(self):
        return self.title


class Contact(AbstractBaseModel):
    full_name = models.CharField(max_length=50)
    email = models.EmailField(max_length=100)
    message = models.TextField()

    def __str__(self):
        return self.full_name

    class Meta:
        verbose_name = _('Message')
        verbose_name_plural = _('Messages')


class ContactPageData(models.Model):
    title = models.CharField(
        _('title'),
        max_length=255,
        default="Bizimlə əlaqə",
    )
    map_src = models.CharField(
        _("Map source"),
        max_length=500,
        blank=True,
        null=True,
    )
    contact = models.TextField(_("contact"), blank=True, null=True)
    phone = models.CharField(_('phone'), max_length=255, blank=True, null=True)
    address = models.TextField(_("address"))
    email = models.TextField(_("email"))

    def __str__(self):
        return self.title
