from django.shortcuts import render
from django.db.models import Avg, Count, Sum, Q
from django.core.paginator import Paginator
from .models import Short


def index(request):
    short_list = Short.objects.filter(rating__gte=3)
    paginator = Paginator(short_list, 10)
    page = request.GET.get('page')
    shorts = paginator.get_page(page)
    return render(request, 'shortcomment/index.html', locals())

def search(request):
    q = request.GET.get('q')

    if not q:
        shorts = []
        return render(request, 'shortcomment/result_search.html', locals())
    
    short_list = Short.objects.filter(Q(title__icontains=q) | Q(shorttext__icontains=q))
    paginator = Paginator(short_list, 10)
    page = request.GET.get('page')
    shorts = paginator.get_page(page)
    return render(request, 'shortcomment/result_search.html', locals())
