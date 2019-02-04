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

from movie.models import Boxoffice

def parse_boxoffice():

    boxList = []

    req = requests.get('http://www.kobis.or.kr/kobis/business/stat/boxs/findFormerBoxOfficeList.do?loadEnd=0&searchType=search&sMultiMovieYn=&sRepNationCd=&sWideAreaCd=')

    header = req.headers

    status = req.status_code #200 is well.

    is_ok = req.ok #boolean

    if (status == 200):
        html = req.text
        soup = BeautifulSoup(html, 'html.parser')
        rows = soup.select( '.listArea > table > tbody > tr')

        for row in rows:
            cols = row.find_all('td')
            obj = temp_boxC(
                        int(cols[0].text.strip()),
                        cols[1].text.strip(),
                        cols[2].text.strip(),
                        int(cols[3].text.strip().replace(',','')),
                        int(cols[4].text.strip().replace(',','')),
                        int(cols[5].text.strip().replace(',','')),
                        int(cols[6].text.strip().replace(',',''))   
                        )

            boxList.append(obj)
            
    else:
        print("error!! req status is")
        print(status)

    return boxList

class temp_boxC:
    rank = 0
    title = ''
    pubDate = ''
    sales = 0
    attendance = 0
    screen = 0
    playcounts = 0

    def __init__(self, rank, title, pubDate, sales, attendance, screen, playcounts):
        self.rank = rank
        self.title = title
        self.pubDate = pubDate
        self.sales = sales
        self.attendance = attendance
        self.screen = screen
        self.playcounts = playcounts

if __name__ =='__main__':
    boxOffice_data = parse_boxoffice()
    for tempClass in boxOffice_data:
        Boxoffice(rank =tempClass.rank,
            title = tempClass.title,
            pubDate = tempClass.pubDate,
            sales = tempClass.sales,
            attendance = tempClass.attendance,
            screen = tempClass.screen,
            playcounts = tempClass.playcounts).save()

