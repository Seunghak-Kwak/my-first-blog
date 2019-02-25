strls = ["텅 커터스: 어린이 <b>극한 직업</b>", "<b>극한 직업</b>의 비니 존스", "<b>극한직업</b>"]

import operator
target = [{"title": "텅 커터스: 어린이 <b>극한 직업</b>", "pubdate":"2010"},{"title": "<b>극한 직업</b>의 비니 존스", "pubdate":"5"},
          {"title": "<b>극한직업</b>", "pubdate":"1999"},{"title": "극한직업", "pubdate":"1"}, {"title": "비", "pubdate":"3"}]
text = "극한직업"

for i in target:
    i["compare"] = i["title"]

for i in target:
    i["compare"] = i['title'].replace(" ", "").replace("<b>","").replace("</b>","")
    if not text in i["compare"]:
        i["compare"] = i["compare"] + "you are the last one"


newlist = sorted(target, key=lambda k: (len(k['compare']), -int(k['pubdate']) )) 

print(newlist)

k = "9.11"
a = float(k)
print(a)

