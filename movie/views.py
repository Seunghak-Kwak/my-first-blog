from django.shortcuts import render
from django_user_agents.utils import get_user_agent
# Create your views here.

from .models import Movie
import urllib.request
import json

def finder(request):

    if request.method == 'GET':

        client_id = "NoHVR5ThgDN1eT1UmJ7A"
        client_secret = "SSFpLneQTO"

        genre = request.GET.get('genre')
        nation = request.GET.get('nation')
        startyear = request.GET.get('startyear')
        endyear = request.GET.get('endyear')

        if nation is None:
            nation = ""
            startyear = ""
            endyear = ""
            genre = ""

        genre = str(genre)

        query_filter ="&yearfrom=" +startyear + "&yearto=" + endyear  + "&country=" + nation + "&genre=" + genre

        q = request.GET.get('q')
        if q == "":
            encText = "None"
        else:
            encText = urllib.parse.quote("{}".format(q))
        if encText == "None":
            encText = "kwakseunghak"
        url = "https://openapi.naver.com/v1/search/movie?query=" + encText + "&display=100" + query_filter  # json 결과
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

            #item을 정렬작업하는 함수 호출!
            items = sorting(items,q)

            context = {
                'total': total,
                'items': items,
                'range': range(1920,2021),
                'search_text' : q
            }

        else:
            print("Error Code:" + rescode)

        user_agent = get_user_agent(request)
        if user_agent.is_mobile:
            return render(request, 'movie/mobile/finder.html', context=context)
        elif user_agent.is_tablet:
            return render(request, 'movie/mobile/finder.html', context=context)
        else :
            return render(request, 'movie/finder.html', context=context)


def sorting(target,text):
    if text is None:
        text = ""


    text = text.replace(" ","").replace(",","")

    for i in target:
        i["compare"] = i['title'].replace(" ", "").replace("<b>","").replace("</b>","").replace(",","")
        if not text in i["compare"]:
            i["compare"] = i["compare"] + "you are the last one"

    sortlist = sorted(target, key=lambda k: (len(k['compare']), -float(k['userRating'])  ,-int(k['pubDate']) )) 

    return sortlist