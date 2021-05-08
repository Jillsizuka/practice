import urllib.request as request
import json
src = "https://padax.github.io/taipei-day-trip-resources/taipei-attractions.json"
with request.urlopen(src) as res:
    data = json.load(res)  # 取得網站資料
clist = data["result"]["results"]
with open("data.txt", "w", encoding="utf-8") as file:
    for name, longi, latit, picture in zip(clist, clist, clist, clist):
        file.write(name["stitle"]+","+longi["longitude"] + ","+latit["latitude"] +
                   ","+"http://"+picture["file"].split('http://')[1]+"\n")
