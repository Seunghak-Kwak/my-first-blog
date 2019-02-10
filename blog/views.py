from django.shortcuts import render
from django.utils import timezone
from .models import *

# Create your views here.
#
def box_list(request):
    posts = Post.objects.filter(published_date__lte=timezone.now()).order_by('created_date')
    box_pasts = Boxoffice.objects.filter(rank__lte=30).order_by('rank')
    naver_pastboxes = Pastbox.objects.order_by('rank')
    naver_liveboxes = Livebox.objects.order_by('rank')


    context = {
                'posts': posts,
                'box_pasts' : box_pasts,
                'nbox_pasts' : naver_pastboxes,
                'nbox_lives' : naver_liveboxes
            }
    return render(request, 'blog/movie_list.html', context=context)

def href(request):
    return HttpResponse(href)