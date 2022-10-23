from .models import Category


def subject_renderer(request):
    context = {
        'categories': Category.objects.all()
    }
    return context
