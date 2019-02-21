from django.shortcuts import render
from django.utils import timezone
from .models import *
import requests
from bs4 import BeautifulSoup

# Create your views here.

def box_list(request):
    posts = Post.objects.filter(published_date__lte=timezone.now()).order_by('created_date')
    box_pasts = Boxoffice.objects.filter(rank__lte=30).order_by('rank')
    naver_pastboxes = Pastbox.objects.order_by('rank')
    naver_liveboxes = Livebox.objects.order_by('rank')
    update_time = Update_time.objects.all()[:1].get().time

    context = {
                'posts': posts,
                'box_pasts' : box_pasts,
                'nbox_pasts' : naver_pastboxes,
                'nbox_lives' : naver_liveboxes,
                'update_time' : update_time,
            }

    return render(request, 'blog/movie_list.html', context=context)

def contact(request):
    context = {}
    return render(request, 'blog/contact.html', context=context)

def reco(request):

    boxList = []

    title = request.POST.get("title", "")

    req = requests.get('https://search.naver.com/search.naver?sm=top_hty&fbm=1&ie=utf8&query=' + title)
    header = req.headers

    status = req.status_code #200 is well.

    is_ok = req.ok #boolean

    if (status == 200):
        html = req.text
        soup = BeautifulSoup(html, 'html.parser')
        movies = soup.select('#_movie_tab_content_aitems > .series > ul > li')

        box = []

        for movie in movies:
            info = {}
            href = movie.find('a', href=True)['href']
            img = movie.find('img')['src']
            img = img.replace("size=66x93","size=264x372")
            
            info['href'] = href
            info['img'] = img
            check = []

            data = movie.find_all(string=True)
            for i in data:
                if not (i.isspace() or i.strip() == ","):
                    check.append(i.strip())

            info['title'] = check[0]
            check[1] = check[1].replace("외","").strip()
            if check[2].isdigit():
                info['details'] = [check[1],check[2],check[3]]
                del check[0:5]
            else:
                info['details'] = [check[1],check[2]]
                del check[0:4]

            temp = []
            for count, i in enumerate(check):
                if i =="출연":
                    info['director'] = temp
                    del check[0:count+1]
                    break
                temp.append(i)
            temp2 = []
            for i in check:
                temp2.append(i)
            info['actor'] = temp2

            box.append(info)
    else:
        print("error!! req status is")
        print(status)
    print(img)

    context = {'title' : title ,
               'box' : box
    }

    return render(request,'blog/movie_reco.html',context=context)

def reset_data(request):
    status = request.POST.get("reset", "")
    time = request.POST.get("update", "")
    update_time = Update_time.objects.all()[:1].get()
    update_time.time = time
    update_time.save()

    if status == "yes":  
        Pastbox.objects.all().delete()
        Livebox.objects.all().delete()
        
        box_past()
        box_live()
        context = {}
    return render(request, 'blog/reset.html', context=context)

# crawling def
def box_past():

    boxList = []

    req = requests.get('https://search.naver.com/search.naver?sm=tab_hty.top&where=nexearch&query=%EC%97%AD%EB%8C%80%EC%98%81%ED%99%94%EC%88%9C%EC%9C%84&oquery=%EC%97%AD%EB%8C%80%EC%98%81%ED%99%94%EC%88%9C%EC%9C%84&tqi=UaIvywpySERsscz2EbKsssssskh-469582')

    header = req.headers

    status = req.status_code #200 is well.

    is_ok = req.ok #boolean

    if (status == 200):
        html = req.text
        soup = BeautifulSoup(html, 'html.parser')
        movies = soup.select('._content > ul > li')
        for movie in movies:
            info = []
            a = movie.find('a', href=True)
            href = 'search.naver.com/search.naver' + a['href']
            img = movie.find('img')['src']
            img = img.replace("size=117x164","size=351x492")
            
            info.append(href)
            info.append(img)

            data = movie.find_all(string=True)
            for i in data:
                if not i.isspace():
                    info.append(i.strip())

            boxList.append(info)

        for i in boxList:
            Pastbox(href=i[0],img=i[1],rank=int(i[3]),title=i[4],pubDate=i[6],attendance=i[8]).save()

    else:
        print("error!! req status is")
        print(status)

def box_live():

    boxList = []

    req = requests.get('https://search.naver.com/search.naver?sm=tab_hty.top&where=nexearch&query=%EC%98%81%ED%99%94%EC%88%9C%EC%9C%84&oquery=%EC%98%81%ED%99%94%EC%88%9C%EC%9C%84&tqi=UaIjtdpVuE4ssZe4ZzKssssssKl-487250')
  
    header = req.headers

    status = req.status_code #200 is well.

    is_ok = req.ok #boolean

    if (status == 200):
        html = req.text
        soup = BeautifulSoup(html, 'html.parser')
        movies = soup.select('._content > ul > li')

        for movie in movies:
            info = []

            img = movie.find('img')['src']
            img = img.replace("size=117x164","size=351x492")
            a = movie.find('a', href=True)
            if a is None:
                href = ''
                img = 'error'
            else:
                href = 'search.naver.com/search.naver' + a['href']
            
            info.append(href)
            info.append(img)

            data = movie.find_all(string=True)
            for i in data:
                if not i.isspace():
                    if not i in ["전체 관람가","15세 관람가","12세 관람가","청소년 관람불가","다운로드","예매","예고편"]:
                        info.append(i.strip())

            boxList.append(info)

        for i in boxList:
            if len(i) == 10:
                Livebox(href=i[0],img=i[1],rank=int(i[2]),title=i[3],pubDate=i[5],attendance=i[9],daily_attendance=i[7]).save()
            else:
                Livebox(href=i[0],img=i[1],rank=int(i[2]),title=i[3],pubDate="",attendance=i[7],daily_attendance=i[5]).save()


    else:
        print("error!! req status is")
        print(status)
