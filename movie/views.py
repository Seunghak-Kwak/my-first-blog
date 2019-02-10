from django.shortcuts import render

# Create your views here.

from .models import Movie
import urllib.request
import json

def finder(request):

    if request.method == 'GET':

        client_id = "NoHVR5ThgDN1eT1UmJ7A"
        client_secret = "SSFpLneQTO"

        q = request.GET.get('q')
        if q == "":
            encText = "None"
        else:
            encText = urllib.parse.quote("{}".format(q))
        if encText == "None":
            encText = "kwakseunghak"
        url = "https://openapi.naver.com/v1/search/movie?query=" + encText + "&display=30"  # json 결과
        movie_api_request = urllib.request.Request(url)
        movie_api_request.add_header("X-Naver-Client-Id", client_id)
        movie_api_request.add_header("X-Naver-Client-Secret", client_secret)
        response = urllib.request.urlopen(movie_api_request)
        rescode = response.getcode()
        if (rescode == 200):
            response_body = response.read()
            result = json.loads(response_body.decode('utf-8'))
            items = result.get('items')
            total = result.get('total')
            print(result)  # request를 예쁘게 출력해볼 수 있다.
            print(items)
            print(total)

            context = {
                'total': total,
                'items': items
            }
        else:
            print("Error Code:" + rescode)

    return render(request, 'movie/finder.html', context=context)
        