# -*- coding: utf-8 -*-
"""
@author: KwakSeunghak
"""
import requests
from bs4 import BeautifulSoup

import os

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "mysite.settings")

import django
django.setup()

from blog.models import Pastbox
from blog.models import Livebox

Pastbox.objects.all().delete()
Livebox.objects.all().delete()

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

if __name__ =='__main__':
    box_past()
    box_live()

